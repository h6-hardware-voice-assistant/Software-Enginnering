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
        lambda url: chosen.append(url) or object(),
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
        lambda url: chosen.append(url) or object(),
    )
    monkeypatch.setattr(
        sys, "argv",
        ["h6_live_demo.py", "--sprint", "2", "--url", "192.168.0.40",
         "--log", str(tmp_path / "evidence.jsonl")],
    )

    h6_live_demo.main()
    assert chosen == ["http://192.168.0.40:8080/audio.wav"]
    assert prompts == ["Enter = listen | q = quit: "]
