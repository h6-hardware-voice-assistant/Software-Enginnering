"""IP Webcam speech input adapter for Raspberry Pi.

Set IP_WEBCAM_AUDIO_URL to the phone's live /audio.wav endpoint.
Requires ffmpeg, SpeechRecognition and internet access for Google STT.
"""
import os
import subprocess
import tempfile
from pathlib import Path
import speech_recognition as sr
from voice_assistant.errors import MicrophoneUnavailableError, UnrecognizedSpeechError, VoiceAssistantError

class IPWebcamSpeechSource:
    def __init__(self, url=None, language="en-IN"):
        self.url = url or os.environ.get("IP_WEBCAM_AUDIO_URL")
        if not self.url:
            raise ValueError("Set IP_WEBCAM_AUDIO_URL to the IP Webcam /audio.wav URL.")
        self.language = language
        self.recognizer = sr.Recognizer()

    def listen(self):
        with tempfile.TemporaryDirectory() as directory:
            audio_file = Path(directory) / "voice.wav"
            command = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error", "-re", "-i", self.url, "-t", "8", "-ac", "1", "-ar", "16000", str(audio_file)]
            try:
                subprocess.run(command, check=True, timeout=25, capture_output=True)
            except (subprocess.SubprocessError, OSError) as exc:
                raise MicrophoneUnavailableError(f"IP Webcam audio capture failed: {exc}") from exc
            try:
                with sr.AudioFile(str(audio_file)) as source:
                    audio = self.recognizer.record(source)
                transcript = self.recognizer.recognize_google(audio, language=self.language)
            except sr.UnknownValueError as exc:
                raise UnrecognizedSpeechError("Speech was captured but not understood.") from exc
            except sr.RequestError as exc:
                raise VoiceAssistantError(f"Speech recognition service failed: {exc}") from exc
            return transcript.strip()
