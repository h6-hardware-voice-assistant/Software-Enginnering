"""NFR-03 — Verify correct operation and repeatability (issue #19)."""

import pytest

from voice_assistant.commands import Command
from voice_assistant.errors import PlayerOperationError
from voice_assistant.processor import process_command
from voice_assistant.controller import MultimediaController
from voice_assistant.player import InMemoryPlayer


@pytest.mark.parametrize(
    ("command", "expected_operation"),
    [
        (Command.PLAY, "play"),
        (Command.NEXT, "next_item"),
        (Command.PREVIOUS, "previous_item"),
    ],
)
def test_repeated_commands_call_only_the_intended_operation(
    command: Command, expected_operation: str
) -> None:
    player = InMemoryPlayer(["track-1", "track-2", "track-3"])
    controller = MultimediaController(player)

    if command is Command.PREVIOUS:
        player.index = 2
    process_command(command, controller)
    process_command(command, controller)

    assert player.calls == [expected_operation, expected_operation]


def test_repeated_next_commands_never_call_another_operation() -> None:
    player = InMemoryPlayer(["track-1", "track-2"])
    controller = MultimediaController(player)

    process_command(Command.NEXT, controller)

    with pytest.raises(PlayerOperationError):
        process_command(Command.NEXT, controller)

    assert player.calls == ["next_item", "next_item"]
    assert player.current_item == "track-2"
