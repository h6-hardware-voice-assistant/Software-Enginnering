"""FR-01 / TC-01 tests for the microphone source, without real audio hardware."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from voice_assistant.errors import (
    MicrophoneUnavailableError,
    NoSpeechDetectedError,
    UnrecognizedSpeechError,
    VoiceAssistantError,
)
from voice_assistant.microphone import MicrophoneSpeechSource


class FakeSpeechModule:
    class WaitTimeoutError(Exception):
        pass

    class UnknownValueError(Exception):
        pass

    class RequestError(Exception):
        pass


class FakeMicrophone:
    def __init__(self) -> None:
        self.closed = False

    def __enter__(self) -> object:
        return object()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.closed = True


class FakeRecognizer:
    def __init__(
        self,
        *,
        transcript: str = "  Play.  ",
        listen_error: BaseException | None = None,
        recognition_error: BaseException | None = None,
    ) -> None:
        self.transcript = transcript
        self.listen_error = listen_error
        self.recognition_error = recognition_error
        self.adjustment_duration: float | None = None
        self.listen_options: dict[str, object] | None = None
        self.transcription_options: dict[str, object] | None = None

    def adjust_for_ambient_noise(self, source, *, duration: float) -> None:
        self.adjustment_duration = duration

    def listen(self, source, *, timeout: float, phrase_time_limit: float) -> str:
        self.listen_options = {
            "timeout": timeout,
            "phrase_time_limit": phrase_time_limit,
        }
        if self.listen_error is not None:
            raise self.listen_error
        return "recorded-audio"

    def recognize_google(self, audio, *, language: str) -> str:
        self.transcription_options = {"audio": audio, "language": language}
        if self.recognition_error is not None:
            raise self.recognition_error
        return self.transcript


def build_source(
    recognizer: FakeRecognizer,
    microphone: FakeMicrophone | None = None,
    *,
    microphone_factory=None,
) -> MicrophoneSpeechSource:
    if microphone_factory is None:
        microphone = microphone or FakeMicrophone()
        microphone_factory = lambda: microphone
    return MicrophoneSpeechSource(
        timeout=2.0,
        phrase_time_limit=3.0,
        ambient_noise_duration=0.1,
        language="en-IN",
        speech_module=FakeSpeechModule,
        recognizer=recognizer,
        microphone_factory=microphone_factory,
    )


def test_captures_and_transcribes_one_utterance() -> None:
    recognizer = FakeRecognizer()
    microphone = FakeMicrophone()
    source = build_source(recognizer, microphone)

    assert source.listen() == "Play."
    assert microphone.closed
    assert recognizer.adjustment_duration == 0.1
    assert recognizer.listen_options == {
        "timeout": 2.0,
        "phrase_time_limit": 3.0,
    }
    assert recognizer.transcription_options == {
        "audio": "recorded-audio",
        "language": "en-IN",
    }


def test_timeout_without_speech_is_reported_as_recoverable_no_speech() -> None:
    recognizer = FakeRecognizer(listen_error=FakeSpeechModule.WaitTimeoutError())
    source = build_source(recognizer)

    with pytest.raises(NoSpeechDetectedError):
        source.listen()

    assert recognizer.transcription_options is None


def test_unintelligible_audio_is_reported_without_returning_a_command() -> None:
    recognizer = FakeRecognizer(
        recognition_error=FakeSpeechModule.UnknownValueError()
    )
    source = build_source(recognizer)

    with pytest.raises(UnrecognizedSpeechError):
        source.listen()


def test_missing_microphone_is_reported_as_microphone_unavailable() -> None:
    def no_microphone():
        raise OSError("No default input device available")

    source = build_source(FakeRecognizer(), microphone_factory=no_microphone)

    with pytest.raises(MicrophoneUnavailableError):
        source.listen()


def test_recognition_service_error_has_actionable_feedback() -> None:
    recognizer = FakeRecognizer(
        recognition_error=FakeSpeechModule.RequestError("service offline")
    )
    source = build_source(recognizer)

    with pytest.raises(VoiceAssistantError) as captured:
        source.listen()

    assert "internet connection" in captured.value.user_message.lower()


def test_empty_transcript_is_reported_as_no_speech() -> None:
    source = build_source(FakeRecognizer(transcript="  "))

    with pytest.raises(NoSpeechDetectedError):
        source.listen()
