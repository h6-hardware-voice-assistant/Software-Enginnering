# Target hardware and smoke-test plan

Story #21 / NFR-06.

## Target and dependencies

- Target: Raspberry Pi 5 with Raspberry Pi OS 64-bit and CPython 3.11+.
- USB microphone, audio output device and a playable media file.
- SpeechRecognition and PyAudio from `requirements-hardware.txt`; PyAudio needs
  PortAudio and the system's audio drivers.
- On 64-bit Raspberry Pi OS, install the `flac` command for SpeechRecognition's
  Google recognizer. Without it, microphone capture can work but transcription fails.
- Internet access: `MicrophoneSpeechSource` uses Google's online recognizer.
- A real player implementing `MediaPlayerBackend` is needed for audible media
  control. The repository currently supplies only `InMemoryPlayer`, which
  records actions without playing audio.

## Setup on the Pi

```bash
sudo apt update
sudo apt install python3-venv python3-dev build-essential portaudio19-dev alsa-utils flac
git clone https://github.com/h6-hardware-voice-assistant/Software-Enginnering.git
cd Software-Enginnering
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -r requirements-hardware.txt
```

Check that the USB microphone appears in `arecord -l` and in:

```bash
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

Use its device index in `MicrophoneSpeechSource(device_index=...)` if it is not
the default microphone. Run `python -m pytest` to check the software separately.

## Smoke-test plan on the target

| Check | Steps | Expected result |
|---|---|---|
| Microphone / TC-01 | Connect the microphone. Run the command below and say Play. | The result is `Command.PLAY`. |
| Media playback / TC-02 | Connect a real backend through `MultimediaController` and `VoiceAssistant`, select a media file, then say Play. | The selected file audibly or visibly starts. |
| Pause and Resume / TC-03, TC-04 | While playing, say Pause, then Resume. | Playback pauses and continues from the paused position. |
| Volume / TC-05, TC-06 | At a mid-range volume, say Volume Up, then Volume Down. Repeat at the player's limits. | Volume changes in the requested direction and stays within the player's range. |
| Invalid input and device failure | Say an unsupported phrase, then test with the microphone disconnected. | Unsupported input performs no media action; an unavailable microphone produces feedback. |

```bash
python -c "from voice_assistant.microphone import MicrophoneSpeechSource; from voice_assistant.recognition import recognize_command; print(recognize_command(MicrophoneSpeechSource().listen()).command)"
```

## Pi verification — 10 November 2026

Raspberry Pi 5 Model B Rev 1.1, Raspberry Pi OS 64-bit (Trixie), Python 3.13.5.
The test used a Shure MV6 USB microphone and mpv 0.40.0 playing `Front_Center.wav`
through BlueALSA to Sony WH-XB910N headphones. A local smoke-test adapter connected
mpv to `MultimediaController`; the repository demo still uses `InMemoryPlayer`.

- Software: 162 tests passed on the Pi at `76d9c95`; `pip check` found no broken
  dependencies after installing the hardware requirements.
- TC-01 / TC-02: The Shure captured at 48 kHz. A spoken `Play` was recognized,
  the app reported `Playback started.`, and playback was heard in the headphones.
  On the repeat test, `Play` was recognized on the third attempt.
- TC-03–TC-06: With test transcripts, the playback position stopped on Pause and
  advanced on Resume. The real player volume changed from 30 to 40 and back to
  30, and repeated commands held the 0 and 100 limits. Spoken `Volume Up` raised
  the volume from 30 to 40 with `en-IN`. The recognizer returned `Volume Up`
  during the `Volume Down` check with `en-IN`; switching the smoke test to
  `en-US` recognized `Volume Down` after retries and lowered the volume to 30.

## ESP limitation

This implementation targets Linux and CPython. An ESP32 running MicroPython
does not provide the same CPython, PyAudio/PortAudio and Linux media-player
environment, so this application cannot be deployed to it unchanged. An ESP
version would require a separate audio-capture, recognition and media-control
implementation; it is not verified here.

Dependency references: [SpeechRecognition requirements](https://github.com/Uberi/speech_recognition#requirements),
[PyAudio installation](https://people.csail.mit.edu/hubert/pyaudio/),
[Raspberry Pi OS](https://www.raspberrypi.com/documentation/computers/os.html),
[MicroPython on ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html).
