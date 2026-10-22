"""FR-10 / NFR-04 tests for allow-list validation before dispatch."""

from __future__ import annotations

import pytest

from voice_assistant.commands import Command
from voice_assistant.errors import UnsupportedCommandError
from voice_assistant.processor import COMMAND_ROUTES, process_command
from voice_assistant.recognition import RecognitionResult, recognize_command


EXPECTED_ROUTES = {
    Command.PLAY: "play_media",
    Command.PAUSE: "pause_media",
    Command.RESUME: "resume_media",
    Command.VOLUME_UP: "increase_volume",
    Command.VOLUME_DOWN: "decrease_volume",
    Command.NEXT: "next_media",
    Command.PREVIOUS: "previous_media",
}


class RecordingController:
    """A controller double that records calls without touching a player."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __getattr__(self, operation: str):
        if operation not in set(EXPECTED_ROUTES.values()):
            raise AttributeError(operation)

        def record_operation() -> str:
            self.calls.append(operation)
            return operation

        return record_operation


@pytest.mark.parametrize(
    ("transcript", "command"),
    [
        ("  PLAY! ", Command.PLAY),
        ("Pause.", Command.PAUSE),
        ("RESUME", Command.RESUME),
        ("Volume   Up!", Command.VOLUME_UP),
        ("volume down?", Command.VOLUME_DOWN),
        (" NEXT ", Command.NEXT),
        ("Previous.", Command.PREVIOUS),
    ],
)
def test_normalized_supported_transcript_dispatches_exactly_one_allowlisted_operation(
    transcript: str, command: Command
) -> None:
    controller = RecordingController()
    candidate = recognize_command(transcript)

    assert candidate.command is command
    assert COMMAND_ROUTES[command] == EXPECTED_ROUTES[command]
    assert process_command(candidate, controller) == EXPECTED_ROUTES[command]
    assert controller.calls == [EXPECTED_ROUTES[command]]


@pytest.mark.parametrize(
    "candidate",
    [
        None,
        "play",
        ["play"],
        100,
        RecognitionResult(transcript="shuffle everything", command=None),
    ],
)
def test_invalid_candidate_is_rejected_without_any_controller_call(candidate) -> None:
    controller = RecordingController()

    with pytest.raises(UnsupportedCommandError):
        process_command(candidate, controller)  # type: ignore[arg-type]

    assert controller.calls == []
