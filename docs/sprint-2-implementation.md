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
