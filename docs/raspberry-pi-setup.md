# Target hardware and smoke-test plan

Story #21 / NFR-06.

## Target and dependencies

- Planned target: Raspberry Pi 5 with Raspberry Pi OS 64-bit and CPython 3.11+.
- USB microphone, audio output device and a playable media file.
- SpeechRecognition and PyAudio from `requirements-hardware.txt`; PyAudio needs
  PortAudio and the system's audio drivers.
- Internet access: `MicrophoneSpeechSource` uses Google's online recognizer.
- A real player implementing `MediaPlayerBackend` is needed for audible media
  control. The repository currently supplies only `InMemoryPlayer`, which
  records actions without playing audio.

## Setup on the Pi

```bash
sudo apt update
sudo apt install python3-venv python3-dev build-essential portaudio19-dev alsa-utils
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

The hardware smoke test remains pending until a Pi and a real media backend are
available. Passing tests or running `voice_assistant.demo` with its simulated
player does not establish physical playback.

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
