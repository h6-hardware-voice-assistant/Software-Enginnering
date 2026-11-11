# Code Coverage Report — Team H6

**Measured 11 November 2026** using coverage.py 7.17.2 and pytest-cov 7.1.0 on Windows, Python 3.12.10.

**Statement coverage: 95%.** Across the reported modules, 386 statements were identified and 21 were missing. The report also lists 17 excluded lines. **Combined statement-and-branch coverage: 93%.**

| Module | Statement coverage |
|---|---:|
| __init__.py | 100% |
| assistant.py | 96% |
| commands.py | 100% |
| controller.py | 92% |
| demo.py | 98% |
| errors.py | 100% |
| microphone.py | 81% |
| player.py | 95% |
| processor.py | 100% |
| recognition.py | 100% |

**Execution:** `python -m pytest -q --cov=voice_assistant --cov-branch --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml`

**Test result:** 162 passed in 4.15s.

**Evidence:** Local `htmlcov/index.html` screenshot and terminal output provided by the developer. Generated HTML/XML artifacts remain on the developer's local machine and are not included in this markdown file.

**Scope:** The displayed measurement covers only the ten listed modules; it does not show coverage for the separate `ip_webcam.py` hardware adapter. This report does not assert full physical hardware validation.
