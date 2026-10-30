"""FR-09 — Move to previous media item (story #18)."""

import pytest

from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import InMemoryPlayer


def test_previous_moves_to_previous_media_item():
    player = InMemoryPlayer(["track-1", "track-2"])
    player.index = 1
    controller = MultimediaController(player)

    assert controller.previous_media() == "previous"
    assert player.current_item == "track-1"
    assert player.calls == ["previous_item"]


def test_previous_when_no_previous_item_raises_error():
    player = InMemoryPlayer(["track-1"])
    controller = MultimediaController(player)

    with pytest.raises(PlayerOperationError):
        controller.previous_media()

    assert player.current_item == "track-1"
    assert player.calls == ["previous_item"]


def test_previous_player_failure_is_reported():
    player = InMemoryPlayer(
        ["track-1", "track-2"],
        fail_on={"previous_item"},
    )
    player.index = 1
    controller = MultimediaController(player)

    with pytest.raises(PlayerOperationError):
        controller.previous_media()

    assert player.current_item == "track-2"
    assert player.calls == ["previous_item"]
