# Branch Coverage Report — Team H6

**Measured 11 November 2026** using coverage.py 7.17.2 and pytest-cov 7.1.0 on Windows, Python 3.12.10.

**Branch coverage: 80%** across **60 measured branches**, with **12 partially covered branches** shown in the HTML coverage summary. **Combined coverage: 93%.**

| Module | Branch coverage | Branches | Partial branches |
|---|---:|---:|---:|
| __init__.py | 100% | 0 | 0 |
| assistant.py | 100% | 8 | 0 |
| commands.py | 100% | 0 | 0 |
| controller.py | 75% | 12 | 3 |
| demo.py | 88% | 8 | 1 |
| errors.py | 100% | 4 | 0 |
| microphone.py | 58% | 12 | 5 |
| player.py | 75% | 12 | 3 |
| processor.py | 100% | 4 | 0 |
| recognition.py | 100% | 0 | 0 |

**Priority gaps:** `microphone.py` (58%), `controller.py` (75%), and `player.py` (75%) have unexercised decision paths. A reported 100% for a file with zero branches means no branches were measured in that file, not that branch-heavy behavior was tested.

**Execution:** `python -m pytest -q --cov=voice_assistant --cov-branch --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml`

**Test result:** 162 passed in 4.15s.

**Evidence:** Local `htmlcov/index.html` screenshot provided by the developer. Generated HTML/XML artifacts remain on the developer's local machine. The displayed measurement does not include the separate `ip_webcam.py` hardware adapter.
