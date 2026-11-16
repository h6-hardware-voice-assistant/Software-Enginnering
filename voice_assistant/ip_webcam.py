"""Raspberry Pi speech source for a phone running IP Webcam.

The phone's address can change between Wi-Fi/hotspot/Tailscale sessions.
This adapter probes configured/saved addresses, then discovers a reachable
/audio.wav stream among local network neighbors, Tailscale peers and the local
IPv4 subnet. Discovery never depends on the cloud speech-recognition service.

The application keeps using the usual SpeechSource.listen() interface.
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener

from voice_assistant.errors import (
    MicrophoneUnavailableError,
    UnrecognizedSpeechError,
    VoiceAssistantError,
)

PORT = 8080
PROBE_TIMEOUT = 0.75
CONFIG_FILE = Path.home() / ".config" / "h6-voice-assistant" / "ip-webcam-url.txt"


def normalize_webcam_url(value: str | None) -> str | None:
    """Accept an IP Webcam base URL, host:port, or full audio.wav URL."""
    value = (value or "").strip()
    if not value:
        return None
    if "://" not in value:
        value = "http://" + value
    parts = urlsplit(value)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        return None
    try:
        port = parts.port
    except ValueError:
        return None
    if parts.username or parts.password:
        return None
    host = parts.hostname
    if ":" in host:
        host = f"[{host}]"
    # The path is always the IP Webcam audio endpoint, not an arbitrary URL.
    return f"{parts.scheme}://{host}:{port or PORT}/audio.wav"


def _probe(url: str) -> bool:
    """Accept only a live WAV response, never an HTML page or an open port."""
    try:
        req = Request(url, headers={"User-Agent": "H6-VoiceAssistant/1.0"})
        # Explicitly avoid HTTP proxy settings when connecting to a LAN peer.
        with build_opener(ProxyHandler({})).open(req, timeout=PROBE_TIMEOUT) as response:
            if response.status != 200:
                return False
            header = response.read(12)
            return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WAVE"
    except (OSError, ValueError, TimeoutError):
        return False


def _run(args: list[str], timeout: float = 2.0) -> str:
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, check=True, timeout=timeout
        )
        return result.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def _saved_url() -> str | None:
    try:
        return normalize_webcam_url(CONFIG_FILE.read_text(encoding="utf-8"))
    except OSError:
        return None


def _save_url(url: str) -> None:
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(url + "\n", encoding="utf-8")
    except OSError:
        # Discovery must still work on a read-only or unusual filesystem.
        pass


def _peer_urls() -> list[str]:
    """Probe recently observed LAN hosts and named Tailscale peers first."""
    hosts: set[str] = set()

    for line in _run(["ip", "neigh", "show"]).splitlines():
        candidate = line.split(maxsplit=1)[0].strip() if line.strip() else ""
        try:
            addr = ipaddress.ip_address(candidate)
            if isinstance(addr, ipaddress.IPv4Address):
                hosts.add(str(addr))
        except ValueError:
            continue

    status = _run(["tailscale", "status", "--json"], timeout=3.0)
    if status:
        try:
            peers = json.loads(status).get("Peer") or {}
            for peer in peers.values():
                for value in peer.get("TailscaleIPs", []):
                    addr = ipaddress.ip_address(value)
                    if isinstance(addr, ipaddress.IPv4Address):
                        hosts.add(str(addr))
        except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
            pass

    return sorted(f"http://{host}:{PORT}/audio.wav" for host in hosts)


def _lan_urls() -> list[str]:
    """Scan only the Pi's attached private IPv4 /24 (or smaller) networks."""
    networks: set[ipaddress.IPv4Network] = set()
    output = _run(["ip", "-o", "-4", "addr", "show", "scope", "global"])
    for address, prefix in re.findall(r"\binet (\d+\.\d+\.\d+\.\d+)/(\d+)\b", output):
        try:
            ip = ipaddress.IPv4Address(address)
            if not ip.is_private or ip.is_loopback or ip.is_link_local:
                continue
            mask = max(int(prefix), 24)
            networks.add(ipaddress.ip_network(f"{address}/{mask}", strict=False))
        except ValueError:
            continue
    # Do not scan the entire Tailscale 100.64/10 network: use named peers instead.
    hosts: set[str] = set()
    for network in networks:
        for ip in network.hosts():
            hosts.add(str(ip))
    return sorted(f"http://{host}:{PORT}/audio.wav" for host in hosts)


def discover_webcam_url(
    preferred: str | None = None, *, exclude: set[str] | None = None
) -> str | None:
    """Discover a working IP Webcam audio feed, preferring known addresses.

    If more than one auto-discovered microphone responds, refuse to guess.
    This avoids accidentally recording from another IP Webcam on shared Wi-Fi.
    """
    excluded = exclude or set()
    hints = [
        preferred,
        os.environ.get("IP_WEBCAM_AUDIO_URL"),
        _saved_url(),
    ]
    checked: set[str] = set(excluded)
    for hint in hints:
        url = normalize_webcam_url(hint)
        if url and url not in checked:
            checked.add(url)
            if _probe(url):
                _save_url(url)
                return url

    # Check likely candidates before scanning a whole local subnet.
    peer_matches: list[str] = []
    for url in _peer_urls():
        if url not in checked:
            checked.add(url)
            if _probe(url):
                peer_matches.append(url)
    if len(peer_matches) == 1:
        _save_url(peer_matches[0])
        return peer_matches[0]
    if len(peer_matches) > 1:
        raise MicrophoneUnavailableError(
            "Multiple IP Webcam microphones detected: "
            + ", ".join(peer_matches)
            + ". Select the phone with --url."
        )

    candidates = [url for url in _lan_urls() if url not in checked]
    if not candidates:
        return None
    matches: list[str] = []
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(_probe, url): url for url in candidates}
        for future in as_completed(futures):
            if future.result():
                matches.append(futures[future])
    if len(matches) == 1:
        _save_url(matches[0])
        return matches[0]
    if len(matches) > 1:
        raise MicrophoneUnavailableError(
            "Multiple IP Webcam microphones detected: "
            + ", ".join(sorted(matches))
            + ". Select the phone with --url."
        )
    return None


class IPWebcamSpeechSource:
    """Live speech source with address discovery and one reconnect attempt."""

    def __init__(self, url: str | None = None, language: str = "en-IN") -> None:
        self.url = normalize_webcam_url(url)
        self.language = language
        self._resolved = False
        self._recognizer = None

    def _ensure_url(self, *, exclude: set[str] | None = None) -> str:
        if self._resolved and self.url and not exclude:
            return self.url

        print("Checking IP Webcam microphone connection...", flush=True)
        chosen = discover_webcam_url(self.url, exclude=exclude)
        if not chosen and sys.stdin.isatty():
            print(
                "Could not automatically find IP Webcam. "
                "Enter the address displayed by the phone once (or press Enter to cancel).",
                flush=True,
            )
            manual = normalize_webcam_url(input("Phone IP Webcam address: "))
            if manual and _probe(manual):
                chosen = manual
                _save_url(chosen)
        if not chosen:
            raise MicrophoneUnavailableError(
                "IP Webcam microphone not found. Start IP Webcam on your phone, "
                "ensure the Pi can reach it, or pass --url http://PHONE_IP:8080."
            )
        if chosen != self.url:
            print(f"IP Webcam microphone discovered: {chosen}", flush=True)
        self.url = chosen
        self._resolved = True
        return chosen

    def listen(self) -> str:
        try:
            import speech_recognition as sr
        except ImportError as exc:
            raise MicrophoneUnavailableError(
                "SpeechRecognition is not installed. Activate .venv and run: "
                "python -m pip install -r requirements-hardware.txt"
            ) from exc

        if self._recognizer is None:
            self._recognizer = sr.Recognizer()
        url = self._ensure_url()

        with tempfile.TemporaryDirectory() as directory:
            audio_file = Path(directory) / "voice.wav"

            def capture(current_url: str) -> None:
                command = [
                    "ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel",
                    "error", "-re", "-i", current_url, "-t", "8",
                    "-ac", "1", "-ar", "16000", str(audio_file),
                ]
                subprocess.run(command, check=True, timeout=25, capture_output=True)

            try:
                capture(url)
            except (subprocess.SubprocessError, OSError):
                # A different phone IP can become active after the demo starts.
                self._resolved = False
                print("Microphone disconnected; checking for its new address...", flush=True)
                try:
                    capture(self._ensure_url(exclude={url}))
                except (subprocess.SubprocessError, OSError) as exc:
                    raise MicrophoneUnavailableError(
                        "IP Webcam audio capture failed after reconnect: " + str(exc)
                    ) from exc

            try:
                with sr.AudioFile(str(audio_file)) as source:
                    audio = self._recognizer.record(source)
                transcript = self._recognizer.recognize_google(
                    audio, language=self.language
                )
            except sr.UnknownValueError as exc:
                raise UnrecognizedSpeechError(
                    "Speech was captured but not understood."
                ) from exc
            except sr.RequestError as exc:
                raise VoiceAssistantError(
                    f"Speech recognition service failed: {exc}"
                ) from exc
            return transcript.strip()
