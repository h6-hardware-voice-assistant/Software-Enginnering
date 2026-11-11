# Sprint 2 implementation and verification — Team H6

**Project:** Hardware-Based Voice Assistant for Multimedia Controls  
**Sprint:** 26–30 October 2026 | **Planned capacity:** 20 points

## Requirement traceability

| Issue | Points | Requirement | Implementation/evidence |
|---|---:|---|---|
| [#16](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/16) | 3 | FR-06/07, TC-05/06 | Controller volume methods; regression tests for increments, limits and failures |
| [#17](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/17) | 2 | FR-08, TC-07 | Next item and end-of-playlist failure |
| [#18](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/18) | 2 | FR-09, TC-08 | Previous item and start-of-playlist failure |
| [#19](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/19) | 3 | NFR-03 | Regression tests ensure one command calls one backend method |
| [#20](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/20) | 3 | NFR-05, SAD | Recognition, processing, controller and player remain separate modules |
| [#21](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/21) | 5 | NFR-06 | Keep hardware dependencies separate; physical target verification is still required |
| [#23](https://github.com/h6-hardware-voice-assistant/Software-Enginnering/issues/23) | 2 | SRS/SAD/Test Plan | This guide and the test/evidence checklist |

## Run locally

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m voice_assistant.demo
```

Expected simulated behavior: Volume Up/Down change volume by 10 (clamped to 0–100); Next/Previous select adjacent playlist items; boundary errors are reported without another action; backend failures do not cause retries or alternate operations.

## Record actual verification before submission

| Check | Actual result |
|---|---|
| Date/time, OS and Python version | Fill in after running |
| `python -m pytest` summary and exit code | Fill in after running |
| Demo walkthrough and exit code | Fill in after running |
| Target device model / OS | Fill in only after physical test |
| Real player backend and media tested | Fill in only after physical test |
| Physical volume/navigation result | Fill in only after physical test |

**Limitation:** `InMemoryPlayer` is a test double. Passing unit tests does not prove audible playback or Raspberry Pi hardware portability. Do not mark physical checks passed without performing them and recording actual output.

## Raspberry Pi 5 verification record (11 November 2026)

**Observed environment:** Raspberry Pi 5, Debian GNU/Linux 13.7 (Trixie), Python 3.13.5. Development dependencies were installed in a Python virtual environment. The Raspberry Pi had no local ALSA microphone capture device; an Android Redmi 13C 5G running IP Webcam supplied live audio over Wi-Fi. The adapter is in `voice_assistant/ip_webcam.py` and uses ffmpeg with `-re` for real-time capture, then Google SpeechRecognition (`en-IN`). A live microphone connection and internet access are prerequisites.

**Automated verification:** `python -m pytest -q` returned **162 passed in 0.17s** on the Pi. This is a reported observation from the interactive hardware session, not an attached CI log.

**Live end-to-end voice-to-controller smoke test:** The utterance “hello assistant play music” was transcribed, mapped to the allowlisted `play` command by a temporary alias wrapper, dispatched to `MultimediaController`, and recorded by `InMemoryPlayer`. Terminal result:

```text
HEARD: hello assistant play music
STATUS: performed
MESSAGE: Playback started.
PLAYER OPERATIONS: ['play']
PLAYER STATE: playing
```

**Scope and remaining limitations:** This validates real speech capture and speech-to-command-to-controller integration. It does **not** demonstrate audible playback, a real media-player backend, Bluetooth speaker/headphone pairing, or physical volume/track navigation. The alias wrapper was part of the smoke-test harness, not a persistent natural-language command parser. A repeatable Pi demo should configure `IP_WEBCAM_AUDIO_URL` for the phone's current `/audio.wav` endpoint; do not commit the phone's transient IP address.

**Presentation framing:** “The modular voice-command software and its 162-test suite were verified on Raspberry Pi 5; a live spoken Play command reached the multimedia controller. The current playback backend is simulated; speaker output remains future integration work.”
