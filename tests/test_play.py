"""FR-03 / TC-02: a validated Play starts the selected media (story #9)."""

from unittest.mock import Mock

import pytest

from voice_assistant.assistant import Status, VoiceAssistant
from voice_assistant.commands import Command
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import PAUSED, PLAYING, STOPPED, InMemoryPlayer, MediaPlayerBackend
from tests.conftest import ScriptedSpeechSource


def test_play_starts_selected_media_without_other_changes(player: InMemoryPlayer) -> None:
    player.index = 1
    selected = player.current_item
    volume = player.volume

    assert MultimediaController(player).play_media() == "play"

    assert player.state == PLAYING
    assert player.current_item == selected
    assert player.volume == volume
    assert player.is_open
    assert player.calls == ["play"]


@pytest.mark.parametrize("transcript", ["Play", "PLAY", " play ", "Play!"])
def test_valid_play_reaches_backend_once(player: InMemoryPlayer, transcript: str) -> None:
    outcome = VoiceAssistant(
        ScriptedSpeechSource(transcript), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PERFORMED
    assert outcome.command is Command.PLAY
    assert outcome.operation == "play"
    assert player.state == PLAYING
    assert player.calls == ["play"]


@pytest.mark.parametrize("transcript", ["", " ", "replay", "play something else", "stop", "play pause"])
def test_invalid_input_never_starts_media(player: InMemoryPlayer, transcript: str) -> None:
    outcome = VoiceAssistant(
        ScriptedSpeechSource(transcript), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.UNSUPPORTED_COMMAND
    assert not outcome.performed
    assert outcome.operation is None
    assert player.calls == []
    assert player.state == STOPPED


def test_repeated_play_does_not_pause_or_skip(playing_player: InMemoryPlayer) -> None:
    controller = MultimediaController(playing_player)
    selected = playing_player.current_item

    controller.play_media()
    controller.play_media()

    assert playing_player.state == PLAYING
    assert playing_player.current_item == selected
    assert playing_player.calls == ["play", "play"]


@pytest.mark.parametrize("state", [STOPPED, PAUSED])
def test_backend_that_does_not_start_is_not_reported_as_success(state: str) -> None:
    backend = Mock(spec=MediaPlayerBackend)
    backend.state = state

    with pytest.raises(PlayerOperationError, match="did not start"):
        MultimediaController(backend).play_media()

    assert backend.method_calls == [("play", (), {})]


@pytest.mark.parametrize("error", [PlayerOperationError("play", "no media selected"), OSError("device unavailable")])
def test_play_failure_is_reported_without_retry_or_other_actions(error: Exception) -> None:
    backend = Mock(spec=MediaPlayerBackend)
    backend.state = STOPPED
    backend.play.side_effect = error
    outcome = VoiceAssistant(
        ScriptedSpeechSource("Play"), MultimediaController(backend)
    ).handle_once()

    assert outcome.status is Status.PLAYER_ERROR
    assert not outcome.performed
    assert outcome.command is Command.PLAY
    assert outcome.operation is None
    assert backend.method_calls == [("play", (), {})]
