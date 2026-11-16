"""Regression tests for interactive IP Webcam selection in the live Pi demo."""

import sys

import h6_live_demo
from voice_assistant.ip_webcam import normalize_webcam_url


def test_webcam_address_normalization():
    assert normalize_webcam_url("192.168.0.35") == "http://192.168.0.35:8080/audio.wav"
    assert normalize_webcam_url("http://192.168.0.35:8080") == "http://192.168.0.35:8080/audio.wav"
    assert normalize_webcam_url("http://192.168.0.35:8080/audio.wav") == "http://192.168.0.35:8080/audio.wav"
    assert normalize_webcam_url("http://") is None
    assert normalize_webcam_url("") is None


def test_running_sprint_prompts_for_current_phone_url(monkeypatch, tmp_path, capsys):
    chosen = []
    entries = iter(["", "192.168.0.35", "q"])

    monkeypatch.setattr("builtins.input", lambda prompt="": next(entries))
    monkeypatch.setattr(
        h6_live_demo,
        "DemoSpeechSource",
        lambda url, **kwargs: chosen.append(url) or object(),
    )
    monkeypatch.setattr(
        sys, "argv",
        ["h6_live_demo.py", "--sprint", "1", "--log", str(tmp_path / "evidence.jsonl")],
    )

    h6_live_demo.main()
    assert chosen == ["http://192.168.0.35:8080/audio.wav"]
    assert "Invalid address" in capsys.readouterr().out


def test_explicit_url_skips_phone_prompt(monkeypatch, tmp_path):
    chosen = []
    prompts = []

    def fake_input(prompt=""):
        prompts.append(prompt)
        return "q"

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(
        h6_live_demo, "DemoSpeechSource",
        lambda url, **kwargs: chosen.append(url) or object(),
    )
    monkeypatch.setattr(
        sys, "argv",
        ["h6_live_demo.py", "--sprint", "2", "--url", "192.168.0.40",
         "--log", str(tmp_path / "evidence.jsonl")],
    )

    h6_live_demo.main()
    assert chosen == ["http://192.168.0.40:8080/audio.wav"]
    assert prompts == ["Enter = listen | q = quit: "]


def test_sprint1_blocks_sprint2_commands_without_player_dispatch(monkeypatch):
    import pytest
    from voice_assistant.assistant import VoiceAssistant, Status
    from voice_assistant.controller import MultimediaController
    from voice_assistant.player import InMemoryPlayer

    class FakeAudio:
        def __init__(self, text):
            self.text = text

        def listen(self):
            return self.text

    for phrase in ("volume up", "volume down", "next", "previous", "next track"):
        monkeypatch.setattr(
            h6_live_demo, "IPWebcamSpeechSource",
            lambda url, text=phrase: FakeAudio(text),
        )
        source = h6_live_demo.DemoSpeechSource("http://127.0.0.1:8080", sprint="1")
        player = InMemoryPlayer()
        result = VoiceAssistant(source, MultimediaController(player)).handle_once()
        assert result.status is Status.UNSUPPORTED_COMMAND
        assert "introduced in Sprint 2" in result.message
        assert player.calls == []
        assert source.last_command in h6_live_demo.SPRINT_2_ADDITIONS


def test_sprint1_play_pause_resume_succeed(monkeypatch):
    from voice_assistant.assistant import VoiceAssistant, Status
    from voice_assistant.controller import MultimediaController
    from voice_assistant.player import InMemoryPlayer

    class FakeAudio:
        def __init__(self):
            self.words = iter(["play", "pause", "resume"])

        def listen(self):
            return next(self.words)

    monkeypatch.setattr(h6_live_demo, "IPWebcamSpeechSource", lambda url: FakeAudio())
    player = InMemoryPlayer()
    source = h6_live_demo.DemoSpeechSource("http://127.0.0.1:8080", sprint="1")
    assistant = VoiceAssistant(source, MultimediaController(player))
    for _ in range(3):
        assert assistant.handle_once().status is Status.PERFORMED
    assert player.calls == ["play", "pause", "resume"]
    assert player.state == "playing"


def test_sprint2_allows_new_controls_and_retains_play(monkeypatch):
    from voice_assistant.assistant import VoiceAssistant, Status
    from voice_assistant.controller import MultimediaController
    from voice_assistant.player import InMemoryPlayer

    class FakeAudio:
        def __init__(self):
            self.words = iter(["play", "volume up", "volume down", "next track", "previous track"])

        def listen(self):
            return next(self.words)

    monkeypatch.setattr(h6_live_demo, "IPWebcamSpeechSource", lambda url: FakeAudio())
    player = InMemoryPlayer()
    source = h6_live_demo.DemoSpeechSource("http://127.0.0.1:8080", sprint="2")
    assistant = VoiceAssistant(source, MultimediaController(player))
    for _ in range(5):
        assert assistant.handle_once().status is Status.PERFORMED
    assert player.calls == ["play", "volume_up", "volume_down", "next_item", "previous_item"]
    assert player.current_item == "track-1"
    assert player.volume == 50
