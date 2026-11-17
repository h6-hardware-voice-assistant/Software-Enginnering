#!/usr/bin/env python3
"""H6 Raspberry Pi live microphone demo and evidence recorder.

Uses the existing voice_assistant modules. Playback is IN-MEMORY (no audible output).
Usage: python h6_live_demo.py --url http://PHONE_IP:8080/audio.wav
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from voice_assistant.assistant import VoiceAssistant
from voice_assistant.commands import normalize
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import UnsupportedCommandError
from voice_assistant.ip_webcam import IPWebcamSpeechSource, normalize_webcam_url
from voice_assistant.player import InMemoryPlayer
from voice_assistant.mpv_player import MpvPlayer


# Sprint 1 exposed the foundational playback controls. Sprint 2 added volume
# and navigation. The current application code supports the cumulative set;
# these limits apply ONLY to the educational Sprint 1 playback demonstration.
SPRINT_1_COMMANDS = frozenset({"play", "pause", "resume"})
SPRINT_2_ADDITIONS = frozenset({"volume up", "volume down", "next", "previous"})


class DemoSpeechSource:
    """Existing live IP Webcam adapter with a narrow wake-phrase convenience."""
    def __init__(self, url, sprint="1"):
        if sprint not in ("1", "2"):
            raise ValueError("Sprint must be 1 or 2")
        self.sprint = sprint
        self.input = IPWebcamSpeechSource(url=url)
        self.last_heard = None
        self.last_command = None

    def listen(self):
        print('Listening for ~8 seconds. Speak now...', flush=True)
        heard = self.input.listen()
        self.last_heard = heard
        phrase = normalize(heard)
        # The core project only accepts exact vocabulary. Remove a known prefix
        # for the demo, without allowing arbitrary partial/unsafe matches.
        for prefix in ('hello assistant ', 'hey assistant ', 'assistant '):
            if phrase.startswith(prefix):
                phrase = phrase[len(prefix):]
                break
        if phrase == 'play music':
            phrase = 'play'
        elif phrase == 'pause music':
            phrase = 'pause'
        elif phrase == 'resume music':
            phrase = 'resume'
        elif phrase == 'next track':
            phrase = 'next'
        elif phrase == 'previous track':
            phrase = 'previous'
        elif phrase == 'increase volume':
            phrase = 'volume up'
        elif phrase == 'decrease volume':
            phrase = 'volume down'
        self.last_command = phrase
        print(f'HEARD: {heard}', flush=True)
        print(f'NORMALIZED COMMAND: {phrase}', flush=True)
        if self.sprint == '1' and phrase in SPRINT_2_ADDITIONS:
            # Block Sprint-2-only operations before the production dispatcher.
            # Their presence on main does not make them Sprint 1 deliverables.
            raise UnsupportedCommandError(
                phrase,
                user_message=(
                    f"'{phrase}' was introduced in Sprint 2 and is not "
                    "enabled in the Sprint 1 demonstration."
                ),
            )
        return phrase


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default=None, help='Optional IP Webcam URL; skips interactive prompt')
    parser.add_argument('--log', default='h6_demo_evidence.jsonl', help='Append-only evidence log')
    parser.add_argument('--sprint', choices=['1', '2'], default='1', help='Select Sprint 1 feature scope or Sprint 2 cumulative scope')
    parser.add_argument('--real-audio', action='store_true', help='Play actual audio through mpv instead of simulating')
    parser.add_argument('--music-dir', default='demo_music', help='Folder containing .mp3/.wav/.flac/.ogg tracks for --real-audio')
    args = parser.parse_args()

    # Always request the live phone address at startup unless --url was supplied.
    # The phone's IP can change after reconnecting to Wi-Fi or a hotspot.
    if args.url is None:
        print("\nH6 — Connect the Redmi phone microphone")
        print("Start IP Webcam on your phone and enter the address it displays.")
        print("Example: http://192.168.1.50:8080 (or just 192.168.1.50)")
        while True:
            try:
                entered = input("Phone IP Webcam address: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nDemo cancelled before microphone setup.")
                return
            address = normalize_webcam_url(entered)
            if address:
                break
            print("Invalid address. Enter the full IP Webcam URL or phone IP.")
    else:
        address = normalize_webcam_url(args.url)
        if not address:
            parser.error("Invalid --url. Use an IP address or http://PHONE_IP:8080")

    print(f"Microphone audio endpoint: {address}", flush=True)
    source = DemoSpeechSource(address, sprint=args.sprint)
    if args.real_audio:
        music_dir = Path(args.music_dir).expanduser()
        tracks = sorted(
            p for p in music_dir.iterdir()
            if p.is_file() and p.suffix.lower() in {'.mp3', '.wav', '.flac', '.ogg', '.m4a'}
        ) if music_dir.is_dir() else []
        if not tracks:
            parser.error(f"No audio files in {music_dir}. Add .mp3 or .wav files before using --real-audio.")
        try:
            player = MpvPlayer(tracks)
        except (OSError, RuntimeError, ValueError) as exc:
            parser.error(f"Real audio unavailable: {exc}")
    else:
        player = InMemoryPlayer()
    assistant = VoiceAssistant(source, MultimediaController(player))
    log = Path(args.log)
    print('\nH6 LIVE VOICE ASSISTANT DEMO')
    print('INPUT: Redmi phone / IP Webcam -> Raspberry Pi -> SpeechRecognition')
    print('BACKEND: mpv (REAL AUDIO to Pi output)' if args.real_audio else
          'BACKEND: InMemoryPlayer (simulated operations; NO audible playback)')
    if args.sprint == '1':
        print('SPRINT 1 | PLAYBACK FOUNDATION')
        print('AVAILABLE IN THIS DEMO: play, pause, resume')
        print('ADDED IN SPRINT 2 (not enabled here): volume up/down, next, previous')
        print('SUGGESTED LIVE SEQUENCE: play -> pause -> resume')
    else:
        print('SPRINT 2 | VOLUME, TRACK NAVIGATION, REGRESSION')
        print('NEW IN SPRINT 2: volume up, volume down, next, previous')
        print('CARRIED FORWARD FROM SPRINT 1: play, pause, resume')
        print('SUGGESTED LIVE SEQUENCE: play -> volume up -> volume down -> next -> previous -> pause')
    print('NOTE: Both demo modes use the latest code; Sprint 1 mode limits feature scope for comparison.')
    print('OPTIONAL WAKE PHRASES: hello assistant play music / next track / previous track')
    print(f'SPRINT: {args.sprint} | EVIDENCE LOG: {log.resolve()}')
    print('Press Enter for each voice capture; type q then Enter to quit.\n')

    attempt = 0
    while True:
        try:
            action = input('Enter = listen | q = quit: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print('\nDemo ended.')
            break
        if action in ('q', 'quit', 'exit'):
            break
        if action:
            print('Unknown menu option; press Enter to listen.')
            continue
        attempt += 1
        source.last_heard = None
        source.last_command = None
        before = len(player.calls)
        outcome = assistant.handle_once()
        record = {
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'sprint': args.sprint,
            'attempt': attempt,
            'heard': source.last_heard,
            'normalized_command': source.last_command,
            'status': outcome.status.value,
            'message': outcome.message,
            'operation': outcome.operation,
            'player_calls_this_attempt': player.calls[before:],
            'player_state': player.state,
            'current_item': player.current_item,
            'volume': player.volume,
            'backend': 'MpvPlayer (actual audio)' if args.real_audio else 'InMemoryPlayer (simulation, no audible playback)',
        }
        print(f"STATUS: {record['status']} | MESSAGE: {record['message']}")
        print(f"OPERATION: {record['operation']} | PLAYER CALLS: {record['player_calls_this_attempt']}")
        print(f"STATE: {player.state} | TRACK: {player.current_item} | VOLUME: {player.volume}")
        with log.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f'Logged attempt #{attempt}\n', flush=True)
    if args.real_audio:
        player.close()
    print(f'Evidence saved: {log.resolve()}')


if __name__ == '__main__':
    main()