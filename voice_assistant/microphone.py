"""Microphone-backed speech input source for story #7 / SRS FR-01.

This adapter captures one utterance from a physical microphone and returns its
transcript. Fixed-vocabulary command matching remains in recognition.py, and
media dispatch remains in processor.py.

Install the optional audio dependencies from requirements-hardware.txt on a
machine with a microphone. The default transcription backend uses Google's
online speech-recognition service, so an internet connection is required.
"""

from __future__ import annotations

from typing import Any, Callable

from voice_assistant.errors import (
    MicrophoneUnavailableError,
    NoSpeechDetectedError,
    UnrecognizedSpeechError,
    VoiceAssistantError,
)


class MicrophoneSpeechSource:
    """Capture one utterance and return its transcript through SpeechSource.

    Args:
        timeout: Seconds to wait for speech to begin before reporting no speech.
        phrase_time_limit: Maximum seconds to capture for one utterance.
        ambient_noise_duration: Seconds used to calibrate background noise.
        language: Speech-recognition locale, for example "en-IN".
        device_index: Optional OS-specific microphone index; None uses the
            system default input device.
        speech_module, recognizer, microphone_factory: Injection points used by
            tests, so behavior can be verified without a real microphone or
            installing audio drivers in CI.
    """

    def __init__(
        self,
        *,
        timeout: float = 5.0,
        phrase_time_limit: float = 5.0,
        ambient_noise_duration: float = 0.3,
        language: str = "en-IN",
        device_index: int | None = None,
        speech_module: Any | None = None,
        recognizer: Any | None = None,
        microphone_factory: Callable[[], Any] | None = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if phrase_time_limit <= 0:
            raise ValueError("phrase_time_limit must be greater than zero")
        if ambient_noise_duration < 0:
            raise ValueError("ambient_noise_duration cannot be negative")
        if not language.strip():
            raise ValueError("language cannot be empty")

        if speech_module is None:
            try:
                import speech_recognition as speech_module
            except ImportError as exc:
                raise MicrophoneUnavailableError(
                    "SpeechRecognition/PyAudio dependencies are not installed.",
                    user_message=(
                        "Voice input dependencies are missing. Install "
                        "requirements-hardware.txt before using the microphone."
                    ),
                ) from exc

        self._speech = speech_module
        self._recognizer = (
            recognizer if recognizer is not None else self._speech.Recognizer()
        )
        self._microphone_factory = microphone_factory or (
            lambda: self._speech.Microphone(device_index=device_index)
        )
        self._timeout = timeout
        self._phrase_time_limit = phrase_time_limit
        self._ambient_noise_duration = ambient_noise_duration
        self._language = language

    def listen(self) -> str:
        """Capture and transcribe one utterance.

        No speech and unintelligible audio are reported as recoverable errors,
        allowing VoiceAssistant.run() to wait for the next utterance. Missing
        or unusable microphone hardware is reported as
        MicrophoneUnavailableError. None of these paths dispatches media.
        """
        try:
            with self._microphone_factory() as microphone:
                self._recognizer.adjust_for_ambient_noise(
                    microphone, duration=self._ambient_noise_duration
                )
                audio = self._recognizer.listen(
                    microphone,
                    timeout=self._timeout,
                    phrase_time_limit=self._phrase_time_limit,
                )
        except self._speech.WaitTimeoutError as exc:
            raise NoSpeechDetectedError(
                "No speech began before the listening timeout."
            ) from exc
        except Exception as exc:
            # Includes no default input device, missing PyAudio, or an audio
            # backend failure while opening/reading the microphone.
            raise MicrophoneUnavailableError(
                str(exc),
                user_message=(
                    "Voice input is unavailable: check that a microphone is "
                    "connected and accessible."
                ),
            ) from exc

        try:
            transcript = self._recognizer.recognize_google(
                audio, language=self._language
            )
        except self._speech.UnknownValueError as exc:
            raise UnrecognizedSpeechError(
                "Speech was captured but could not be transcribed."
            ) from exc
        except self._speech.RequestError as exc:
            # This is not a microphone failure: the online transcription
            # service may be unavailable or the network may be disconnected.
            raise VoiceAssistantError(
                str(exc),
                user_message=(
                    "Speech recognition is unavailable. Check the internet "
                    "connection and try again."
                ),
            ) from exc

        if not isinstance(transcript, str) or not transcript.strip():
            raise NoSpeechDetectedError("The recognizer returned an empty transcript.")

        return transcript.strip()
