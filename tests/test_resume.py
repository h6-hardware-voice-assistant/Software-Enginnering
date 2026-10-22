
"""FR-05 — Resume paused media (story #11)."""

import pytest

from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import PAUSED, PLAYING, InMemoryPlayer


def test_resume_continues_paused_media(playing_player: InMemoryPlayer) -> None:
    controller = MultimediaController(playing_player)
    controller.pause_media()

    assert controller.resume_media() == "resume"
    assert playing_player.state == PLAYING
    assert playing_player.calls == ["pause", "resume"]


def test_resume_when_not_paused_fails_without_resuming(
    playing_player: InMemoryPlayer,
) -> None:
    controller = MultimediaController(playing_player)

    with pytest.raises(PlayerOperationError):
        controller.resume_media()

    assert playing_player.calls == []
    assert playing_player.state == PLAYING


def test_resume_keeps_the_current_media_item(
    playing_player: InMemoryPlayer,
) -> None:
    controller = MultimediaController(playing_player)
    current_item = playing_player.current_item
    controller.pause_media()

    controller.resume_media()

    assert playing_player.current_item == current_item


def test_resume_player_failure_is_reported(
    playing_player: InMemoryPlayer,
) -> None:
    controller = MultimediaController(playing_player)
    controller.pause_media()
    playing_player.fail_on.add("resume")

    with pytest.raises(PlayerOperationError):
        controller.resume_media()

    assert playing_player.state == PAUSED
    assert playing_player.calls == ["pause", "resume"]
