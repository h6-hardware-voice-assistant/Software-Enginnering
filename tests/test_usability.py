"""NFR-02: clear feedback and a repeatable transcript walkthrough (story #15)."""

from unittest.mock import Mock

import pytest

from voice_assistant import demo
from voice_assistant.assistant import Status, VoiceAssistant
from voice_assistant.commands import Command, supported_phrases
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import (
    HardwareInterfaceError,
    MicrophoneUnavailableError,
    NoSpeechDetectedError,
    UnrecognizedSpeechError,
)
from voice_assistant.player import InMemoryPlayer
from tests.conftest import ScriptedSpeechSource


def test_play_and_pause_report_results_in_plain_language(player: InMemoryPlayer) -> None:
    assistant = VoiceAssistant(ScriptedSpeechSource("Play", "Pause"), MultimediaController(player))

    assert [outcome.message for outcome in assistant.run(2)] == [
        "Playback started.", "Playback paused."
    ]
    assert player.calls == ["play", "pause"]


@pytest.mark.parametrize("command", list(Command))
def test_success_feedback_does_not_expose_method_names(command: Command) -> None:
    controller = Mock(spec=MultimediaController)
    outcome = VoiceAssistant(
        ScriptedSpeechSource(command.value.replace("_", " ")), controller
    ).handle_once()

    assert outcome.performed
    assert outcome.message.endswith(".")
    assert "_" not in outcome.message
    assert "Performed" not in outcome.message


def test_unsupported_feedback_lists_the_allowed_phrases(player: InMemoryPlayer) -> None:
    outcome = VoiceAssistant(
        ScriptedSpeechSource("shuffle everything"), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.UNSUPPORTED_COMMAND
    for phrase in supported_phrases():
        assert phrase in outcome.message.lower()
    assert player.calls == []


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (NoSpeechDetectedError(), "No speech was detected. Please say a command."),
        (UnrecognizedSpeechError(), "The speech could not be recognized. Please repeat the command."),
        (MicrophoneUnavailableError(), "Voice input is unavailable: the microphone could not be used."),
        (HardwareInterfaceError(), "The hardware interface is unavailable. No action was performed."),
    ],
)
def test_capture_error_feedback_matches_the_guide(
    player: InMemoryPlayer, error: Exception, expected: str
) -> None:
    outcome = VoiceAssistant(ScriptedSpeechSource(error), MultimediaController(player)).handle_once()

    assert not outcome.performed
    assert outcome.message == expected
    assert player.calls == []


def test_failed_play_does_not_print_success_or_private_details(player: InMemoryPlayer) -> None:
    player.fail_on = {"play"}
    outcome = VoiceAssistant(ScriptedSpeechSource("Play"), MultimediaController(player)).handle_once()

    assert outcome.status is Status.PLAYER_ERROR
    assert outcome.message == "The media player could not complete that operation."
    assert "injected" not in outcome.message


def test_usability_walkthrough(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    entries = iter(["help", "Play", "Pause", "shuffle", "", "Resume", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    demo.main([])
    output = capsys.readouterr().out

    for expected in [
        "simulated player, no microphone capture or audio output",
        "Command phrases:", "Playback started.", "Player state: playing",
        "Playback paused.", "Player state: paused",
        "That command is not supported.", "No speech was detected.",
        "That operation is not available yet.", "Demo ended.",
    ]:
        assert expected in output


def test_walkthrough_can_show_player_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    entries = iter(["Play", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(entries))

    demo.main(["--fail-play"])
    output = capsys.readouterr().out

    assert "The media player could not complete that operation." in output
    assert "Player state: stopped" in output
    assert "Playback started." not in output


@pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
def test_walkthrough_exits_cleanly_when_input_ends(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], error: type[BaseException]
) -> None:
    def stop_input(_: str) -> str:
        raise error()

    monkeypatch.setattr("builtins.input", stop_input)
    demo.main([])

    assert "Demo ended." in capsys.readouterr().out
