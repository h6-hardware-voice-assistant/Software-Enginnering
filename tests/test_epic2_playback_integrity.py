"""Epic #2 closure checks — playback and navigation as one behaviour.

Stories #9 (FR-03), #10 (FR-04), #11 (FR-05), #17 (FR-08) and #18 (FR-09) each
have their own tests. What those story tests do not assert is the epic-level
outcome Epic #2 is closed against:

    "Each recognized command performs the matching player action and preserves
     playback state as required."

Two parts of that were unverified before this file: that a *spoken* navigation
command reaches exactly one player operation end to end, and that navigating
between items does not disturb whether media is playing or paused.
"""

from __future__ import annotations

import pytest

from voice_assistant.assistant import Status, VoiceAssistant
from voice_assistant.commands import Command
from voice_assistant.controller import MultimediaController
from voice_assistant.player import PAUSED, PLAYING, InMemoryPlayer

from tests.conftest import ScriptedSpeechSource


def playing(playlist: list[str] | None = None, index: int = 0) -> InMemoryPlayer:
    """A player with media playing, positioned at `index`, with a clean call log."""
    player = InMemoryPlayer(playlist or ["track-1", "track-2", "track-3"])
    player.index = index
    player.play()
    player.calls.clear()
    return player


def paused(playlist: list[str] | None = None, index: int = 0) -> InMemoryPlayer:
    """A player with media paused, positioned at `index`, with a clean call log."""
    player = playing(playlist, index)
    player.pause()
    player.calls.clear()
    return player


@pytest.mark.parametrize(
    ("phrase", "command", "operation", "backend_call"),
    [
        ("Play", Command.PLAY, "play", "play"),
        ("Pause", Command.PAUSE, "pause", "pause"),
        ("Next", Command.NEXT, "next", "next_item"),
        ("Previous", Command.PREVIOUS, "previous", "previous_item"),
    ],
)
def test_spoken_command_reaches_exactly_one_player_operation(
    phrase: str, command: Command, operation: str, backend_call: str
) -> None:
    """FR-03/04/08/09 end to end: transcript in, one matching player call out."""
    player = playing(index=1)

    outcome = VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PERFORMED
    assert outcome.command is command
    assert outcome.operation == operation
    assert player.calls == [backend_call]


def test_spoken_resume_reaches_exactly_one_player_operation() -> None:
    """FR-05 end to end; Resume needs a paused player, so it is set up separately."""
    player = paused(index=1)

    outcome = VoiceAssistant(
        ScriptedSpeechSource("Resume"), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PERFORMED
    assert outcome.command is Command.RESUME
    assert outcome.operation == "resume"
    assert player.calls == ["resume"]
    assert player.state == PLAYING


@pytest.mark.parametrize("phrase", ["Next", "Previous"])
def test_navigation_preserves_whether_media_is_playing(phrase: str) -> None:
    """FR-08/FR-09 must move the selection without starting or stopping playback."""
    player = playing(index=1)

    VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert player.state == PLAYING


@pytest.mark.parametrize("phrase", ["Next", "Previous"])
def test_navigation_preserves_a_paused_player(phrase: str) -> None:
    """Navigating while paused must not silently resume playback."""
    player = paused(index=1)

    VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert player.state == PAUSED


@pytest.mark.parametrize(
    ("phrase", "expected_item"),
    [("Next", "track-3"), ("Previous", "track-1")],
)
def test_navigation_changes_only_the_selected_item(
    phrase: str, expected_item: str
) -> None:
    """Volume and the open player are untouched by a navigation command."""
    player = playing(index=1)
    volume = player.volume

    VoiceAssistant(
        ScriptedSpeechSource(phrase), MultimediaController(player)
    ).handle_once()

    assert player.current_item == expected_item
    assert player.volume == volume
    assert player.is_open


def test_failed_navigation_leaves_playback_state_untouched() -> None:
    """At a playlist edge the command is reported and nothing else changes."""
    player = playing(["only-track"])

    outcome = VoiceAssistant(
        ScriptedSpeechSource("Next"), MultimediaController(player)
    ).handle_once()

    assert outcome.status is Status.PLAYER_ERROR
    assert not outcome.performed
    assert outcome.operation is None
    assert player.state == PLAYING
    assert player.current_item == "only-track"


def test_pause_navigate_resume_returns_to_the_newly_selected_item() -> None:
    """The five operations compose: the epic's playback state survives a sequence."""
    player = playing(index=0)
    assistant = VoiceAssistant(
        ScriptedSpeechSource("Pause", "Next", "Resume"), MultimediaController(player)
    )

    outcomes = assistant.run(3)

    assert [outcome.status for outcome in outcomes] == [Status.PERFORMED] * 3
    assert player.calls == ["pause", "next_item", "resume"]
    assert player.state == PLAYING
    assert player.current_item == "track-2"
