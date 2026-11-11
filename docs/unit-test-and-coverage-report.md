# Unit Test and Coverage Verification — Team H6

**Verification date:** 11 November 2026  
**Environment:** Windows (win32), Python 3.12.10, pytest 9.1.1, pytest-cov 7.1.0, coverage 7.17.2  
**Command:** `python -m pytest -q --cov=voice_assistant --cov-branch --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml`

## Test results
**162 passed in 4.15 seconds.** No test failures were reported.

## Coverage summary
```text
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
voice_assistant\__init__.py          2      0      0      0   100%
voice_assistant\assistant.py        72      3      8      0    96%   130-132
voice_assistant\commands.py         26      0      0      0   100%
voice_assistant\controller.py       78      6     12      3    90%   25, 31, 46, 80-81, 84
voice_assistant\demo.py             43      1      8      1    96%   55
voice_assistant\errors.py           29      0      4      0   100%
voice_assistant\microphone.py       43      8     12      5    76%   52, 54, 56, 58, 61-64
voice_assistant\player.py           57      3     12      3    91%   71, 87, 94
voice_assistant\processor.py        15      0      4      0   100%
voice_assistant\recognition.py      21      0      0      0   100%
----------------------------------------------------------------------------
TOTAL                              386     21     60     12    93%
```

**Interpretation:** 93% is the combined pytest-cov coverage figure, **not a separate branch-only percentage**. The branch column reports 60 identified branches and BrPart reports 12 partial branches. To establish an exact branch-only percentage, inspect the generated coverage XML/JSON report. HTML output was generated at `htmlcov/index.html` and XML at `coverage.xml` on the developer's local machine; these artifacts were not automatically uploaded with this markdown summary.

**Scope limitation:** The displayed report does not include `voice_assistant/ip_webcam.py`, which was added to the remote repository separately. It is not correct to claim this run measured that adapter's coverage. Physical audio playback and Bluetooth output remain unverified.

**Evidence provenance:** Values copied from the developer's actual PowerShell test output; this file does not independently rerun tests.
