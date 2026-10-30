"""FR-08 — Move to next media item (story #17)."""

import pytest

from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import InMemoryPlayer


def test_next_moves_to_next_media_item():
    player = InMemoryPlayer(["track-1", "track-2"])
    controller = MultimediaController(player)

    assert controller.next_media() == "next"
    assert player.current_item == "track-2"
    assert player.calls == ["next_item"]


def test_next_when_no_next_item_raises_error():
    player = InMemoryPlayer(["track-1"])
    controller = MultimediaController(player)

    with pytest.raises(PlayerOperationError):
        controller.next_media()

    assert player.current_item == "track-1"
    assert player.calls == ["next_item"]


def test_next_player_failure_is_reported():
    player = InMemoryPlayer(["track-1", "track-2"], fail_on={"next_item"})
    controller = MultimediaController(player)

    with pytest.raises(PlayerOperationError):
        controller.next_media()

    assert player.current_item == "track-1"
    assert player.calls == ["next_item"]
