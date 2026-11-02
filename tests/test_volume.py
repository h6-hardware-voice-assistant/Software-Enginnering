"""FR-06 / FR-07, TC-05 / TC-06: volume commands (story #16)."""

from unittest.mock import Mock

import pytest

from tests.conftest import ScriptedSpeechSource
from voice_assistant.assistant import Status, VoiceAssistant
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import InMemoryPlayer, MediaPlayerBackend, PAUSED, PLAYING, STOPPED


@pytest.mark.parametrize(
    ("phrase", "operation", "expected_volume", "message"),
    [
        ("Volume Up", "volume_up", 60, "Volume increased."),
        ("Volume Down", "volume_down", 40, "Volume decreased."),
    ],
)
@pytest.mark.parametrize("state", [STOPPED, PLAYING, PAUSED])
def test_volume_command_changes_only_volume(
    phrase: str, operation: str, expected_volume: int, message: str, state: str
) -> None:
    player = InMemoryPlayer()
    player.index = 1
    if state in (PLAYING, PAUSED):
        player.play()
    if state == PAUSED:
        player.pause()
    player.calls.clear()
    selected = player.current_item

    outcome = VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PERFORMED
    assert outcome.operation == operation
    assert outcome.message == message
    assert player.volume == expected_volume
    assert player.calls == [operation]
    assert player.state == state
    assert player.current_item == selected
    assert player.is_open


@pytest.mark.parametrize(
    ("method", "initial", "expected", "operation"),
    [
        ("increase_volume", 95, 100, "volume_up"),
        ("increase_volume", 100, 100, "volume_up"),
        ("decrease_volume", 5, 0, "volume_down"),
        ("decrease_volume", 0, 0, "volume_down"),
    ],
)
def test_volume_limits_are_safe(
    method: str, initial: int, expected: int, operation: str
) -> None:
    player = InMemoryPlayer(volume=initial)

    assert getattr(MultimediaController(player), method)() == operation

    assert player.volume == expected
    assert player.calls == [operation]


def test_repeated_adjustments_stop_at_limits() -> None:
    player = InMemoryPlayer()
    controller = MultimediaController(player)
    for _ in range(20):
        controller.increase_volume()
    assert player.volume == 100
    for _ in range(20):
        controller.decrease_volume()
    assert player.volume == 0


@pytest.mark.parametrize(
    ("phrase", "operation"),
    [("Volume Up", "volume_up"), ("Volume Down", "volume_down")],
)
@pytest.mark.parametrize("error", [PlayerOperationError("volume"), OSError("device unavailable")])
def test_backend_failure_is_reported_without_retry_or_another_action(
    phrase: str, operation: str, error: Exception
) -> None:
    backend = Mock(spec=MediaPlayerBackend)
    getattr(backend, operation).side_effect = error

    outcome = VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(backend)
    ).handle_once()

    assert outcome.status is Status.PLAYER_ERROR
    assert not outcome.performed
    assert outcome.operation is None
    assert outcome.message == "The media player could not complete that operation."
    assert backend.method_calls == [(operation, (), {})]


@pytest.mark.parametrize(
    ("phrase", "operation"),
    [("Volume Up", "volume_up"), ("Volume Down", "volume_down")],
)
def test_failed_adjustment_preserves_volume(phrase: str, operation: str) -> None:
    player = InMemoryPlayer(volume=50, fail_on={operation})

    outcome = VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PLAYER_ERROR
    assert player.volume == 50
    assert player.state == STOPPED
    assert player.calls == [operation]


@pytest.mark.parametrize(
    "phrase", ["louder", "volume up please", "volume up volume down", ""]
)
def test_invalid_volume_input_performs_no_action(phrase: str) -> None:
    player = InMemoryPlayer(volume=50)

    outcome = VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.UNSUPPORTED_COMMAND
    assert player.volume == 50
    assert player.calls == []
