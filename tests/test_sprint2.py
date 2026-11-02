"""Sprint 2 tests: volume, playlist navigation and safe backend failures."""
from unittest.mock import Mock
import pytest
from voice_assistant.assistant import Status, VoiceAssistant
from voice_assistant.controller import MultimediaController
from voice_assistant.errors import PlayerOperationError
from voice_assistant.player import InMemoryPlayer, MediaPlayerBackend, STOPPED
from tests.conftest import ScriptedSpeechSource

@pytest.mark.parametrize(("phrase","call","volume"), [
    ("Volume Up","volume_up",60), ("Volume Down","volume_down",40)])
def test_volume_commands(phrase, call, volume):
    player = InMemoryPlayer(volume=50)
    outcome = VoiceAssistant(ScriptedSpeechSource(phrase), MultimediaController(player)).handle_once()
    assert outcome.status is Status.PERFORMED
    assert player.volume == volume
    assert player.calls == [call]

def test_volume_is_clamped_at_limits():
    player = InMemoryPlayer(volume=100)
    MultimediaController(player).increase_volume()
    assert player.volume == 100
    player.volume = 0
    MultimediaController(player).decrease_volume()
    assert player.volume == 0

@pytest.mark.parametrize(("phrase","index","item","call"), [
    ("Next",0,"track-2","next_item"), ("Previous",1,"track-1","previous_item")])
def test_navigation_selects_adjacent_item(phrase,index,item,call):
    player = InMemoryPlayer()
    player.index = index
    outcome = VoiceAssistant(ScriptedSpeechSource(phrase), MultimediaController(player)).handle_once()
    assert outcome.status is Status.PERFORMED
    assert player.current_item == item
    assert player.calls == [call]

@pytest.mark.parametrize(("method","index","call"), [
    ("next_media",2,"next_item"), ("previous_media",0,"previous_item")])
def test_navigation_boundary_errors_do_not_change_selection(method,index,call):
    player = InMemoryPlayer()
    player.index = index
    with pytest.raises(PlayerOperationError):
        getattr(MultimediaController(player),method)()
    assert player.calls == [call]
    assert player.index == index

@pytest.mark.parametrize(("phrase","method"), [
    ("Volume Up","volume_up"),("Volume Down","volume_down"),
    ("Next","next_item"),("Previous","previous_item")])
def test_backend_failure_is_not_retried(phrase,method):
    backend = Mock(spec=MediaPlayerBackend)
    backend.state = STOPPED
    getattr(backend,method).side_effect = OSError("device unavailable")
    outcome = VoiceAssistant(ScriptedSpeechSource(phrase),MultimediaController(backend)).handle_once()
    assert outcome.status is Status.PLAYER_ERROR
    assert outcome.operation is None
    assert backend.method_calls == [(method,(),{})]
