"""Real Raspberry Pi audio playback using mpv's JSON IPC socket.

Use only for --real-audio live demonstrations. The existing InMemoryPlayer
remains the default backend for all automated tests and transcript demos.
"""

from __future__ import annotations

import json
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path

from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import STOPPED, PLAYING, PAUSED


class MpvPlayer:
    """MediaPlayerBackend implementation with actual audible local-file playback."""

    def __init__(self, tracks: list[str | Path], *, volume: int = 50) -> None:
        self.playlist = [str(Path(p).expanduser().resolve()) for p in tracks]
        if not self.playlist:
            raise ValueError("No tracks found. Put .mp3 or .wav files in demo_music.")
        if not shutil.which("mpv"):
            raise RuntimeError("mpv is missing. Install it with: sudo apt install -y mpv")
        for track in self.playlist:
            if not Path(track).is_file():
                raise FileNotFoundError(track)
        self.index = 0
        self.volume = max(0, min(100, volume))
        self.calls: list[str] = []
        self._state = STOPPED
        self.is_open = True
        self._tmp = tempfile.TemporaryDirectory(prefix="h6-mpv-")
        self._socket = str(Path(self._tmp.name) / "mpv.sock")
        self._request_id = 0
        self._proc = subprocess.Popen(
            [
                "mpv", "--no-config", "--no-terminal", "--no-video",
                "--idle=yes", "--force-window=no", "--loop-file=inf",
                f"--volume={self.volume}", f"--input-ipc-server={self._socket}"
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(50):
            if Path(self._socket).exists():
                break
            if self._proc.poll() is not None:
                self.close()
                raise RuntimeError("mpv could not start. Check audio/device setup.")
            time.sleep(0.06)
        if not Path(self._socket).exists():
            self.close()
            raise RuntimeError("mpv control socket did not start.")
        print("REAL AUDIO BACKEND READY: mpv", flush=True)

    @property
    def state(self) -> str:
        return self._state

    @property
    def current_item(self) -> str:
        return Path(self.playlist[self.index]).name

    def _command(self, operation: str, *args: object) -> None:
        self._request_id += 1
        packet = json.dumps(
            {"command": list(args), "request_id": self._request_id}
        ).encode() + b"\n"
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(5.0)
                s.connect(self._socket)
                s.sendall(packet)
                buf = b""
                while True:
                    block = s.recv(4096)
                    if not block:
                        raise OSError("mpv closed control connection")
                    buf += block
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        reply = json.loads(line)
                        if reply.get("request_id") != self._request_id:
                            continue
                        if reply.get("error") != "success":
                            raise PlayerOperationError(
                                operation, str(reply.get("error", "unknown mpv failure"))
                            )
                        return
        except (OSError, ValueError) as exc:
            raise PlayerOperationError(operation, f"mpv unavailable: {exc}") from exc

    def _load(self) -> None:
        self._command("loadfile", "loadfile", self.playlist[self.index], "replace")
        self._command("unpause", "set_property", "pause", False)

    def play(self) -> None:
        self._load()
        self.calls.append("play")
        self._state = PLAYING

    def pause(self) -> None:
        if self._state != PLAYING:
            raise PlayerOperationError("pause", "Nothing is playing")
        self._command("pause", "set_property", "pause", True)
        self.calls.append("pause")
        self._state = PAUSED

    def resume(self) -> None:
        if self._state != PAUSED:
            raise PlayerOperationError("resume", "Nothing is paused")
        self._command("resume", "set_property", "pause", False)
        self.calls.append("resume")
        self._state = PLAYING

    def volume_up(self) -> None:
        new_volume = min(100, self.volume + 10)
        self._command("volume_up", "set_property", "volume", new_volume)
        self.volume = new_volume
        self.calls.append("volume_up")

    def volume_down(self) -> None:
        new_volume = max(0, self.volume - 10)
        self._command("volume_down", "set_property", "volume", new_volume)
        self.volume = new_volume
        self.calls.append("volume_down")

    def next_item(self) -> None:
        if self.index >= len(self.playlist) - 1:
            raise PlayerOperationError("next_item", "No next track")
        new_index = self.index + 1
        self._command("next_item", "loadfile", self.playlist[new_index], "replace")
        self.index = new_index
        self.calls.append("next_item")
        self._state = PLAYING

    def previous_item(self) -> None:
        if self.index <= 0:
            raise PlayerOperationError("previous_item", "No previous track")
        new_index = self.index - 1
        self._command("previous_item", "loadfile", self.playlist[new_index], "replace")
        self.index = new_index
        self.calls.append("previous_item")
        self._state = PLAYING

    def close(self) -> None:
        if not self.is_open:
            return
        self.is_open = False
        if self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait()
        self._tmp.cleanup()
        self._state = STOPPED
