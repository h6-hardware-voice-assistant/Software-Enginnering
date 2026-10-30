"""NFR-01 — Measure command response time (issue #14)."""

import time

from voice_assistant.commands import Command
from voice_assistant.processor import process_command

from test_command_allowlist import RecordingController


def test_command_response_time_is_measured():
    controller = RecordingController()

    start_time = time.perf_counter()
    result = process_command(Command.PLAY, controller)
    elapsed_seconds = time.perf_counter() - start_time

    assert result == "play_media"
    assert controller.calls == ["play_media"]
    assert elapsed_seconds >= 0

    print(f"\nCommand response time: {elapsed_seconds * 1000:.3f} ms")
