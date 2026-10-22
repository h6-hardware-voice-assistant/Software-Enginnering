"""Transcript-only walkthrough for story #15; no microphone or audio output."""

import argparse
from dataclasses import dataclass
import logging

from voice_assistant.assistant import VoiceAssistant
from voice_assistant.commands import supported_phrases
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import NoSpeechDetectedError
from voice_assistant.player import InMemoryPlayer


@dataclass
class TranscriptSource:
    transcript: str = ""

    def listen(self) -> str:
        if not self.transcript.strip():
            raise NoSpeechDetectedError()
        return self.transcript


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-play", action="store_true", help="simulate a failed Play request")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.CRITICAL)

    player = InMemoryPlayer(fail_on={"play"} if args.fail_play else set())
    source = TranscriptSource()
    assistant = VoiceAssistant(source, MultimediaController(player))
    print("Transcript demo: simulated player, no microphone capture or audio output.")
    print("Try Play, then Pause. Unavailable operations give feedback.")
    print("Enter help for command phrases or quit to exit.")

    while True:
        try:
            transcript = input("Command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nDemo ended.")
            return
        if transcript.strip().lower() == "quit":
            print("Demo ended.")
            return
        if transcript.strip().lower() == "help":
            print("Command phrases: " + ", ".join(supported_phrases()) + ".")
            continue
        source.transcript = transcript
        print(assistant.handle_once().message)
        print(f"Player state: {player.state}")


if __name__ == "__main__":
    main()
