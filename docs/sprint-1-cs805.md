# Sprint 1 - Play and command usability

- **Name:** Arpan Joardar
- **SRN:** PES1UG25CS805
- **GitHub:** @arpan-joardar
- **Sprint:** 19-23 October 2026
- **Verification date:** 22 October 2026

## Assigned work

| Story | Points | Requirement | Work |
|---|---:|---|---|
| [#9](https://github.com/ignite-2005/Software-Enginnering/issues/9) | 3 | FR-03, TC-02 | Start the selected media through the player's Play operation; test valid input, rejected input and player failures. |
| [#15](https://github.com/ignite-2005/Software-Enginnering/issues/15) | 2 | NFR-02 | Document the commands, use clear feedback and provide a repeatable usability walkthrough. |

Requirements come from [MINI PROJECT.pdf](../MINI%20PROJECT.pdf): FR-03 on
page 5, NFR-02 on page 7, the Play sequence on page 17, `play_media()` on
page 19, error handling on page 21 and TC-02 on page 22. Assignments and
sprint dates come from [BACKLOG.md](../BACKLOG.md) and the two story issues.

The Play controller calls `player.play()` once. It returns `play` only after the
backend reports the `playing` state. A rejected request, backend exception or
failure to enter that state produces a player error without trying a different
operation. Selection and audio playback belong to the player backend.

## Command guide

Say one complete phrase at a time. Case, punctuation and extra spaces in a
transcript are normalized. Extra words do not form a supported command:
`Play` is accepted, while `play something else` is rejected.

| Phrase | Intended operation | Availability in this branch on 22 October |
|---|---|---|
| Play | Start the selected media | Implemented through the backend interface (#9). |
| Pause | Pause the current media, keeping the player open | Existing implementation (#10). |
| Resume | Continue paused playback | Recognized; controller implementation remains #11. |
| Volume Up | Increase the current volume | Recognized; controller implementation remains Sprint 2 #16. |
| Volume Down | Decrease the current volume | Recognized; controller implementation remains Sprint 2 #16. |
| Next | Select the next media item | Recognized; controller implementation remains Sprint 2 #17. |
| Previous | Select the previous media item | Recognized; controller implementation remains Sprint 2 #18. |

An operation that is still unavailable reports that fact and does not start
another operation. This work does not implement Resume, volume or navigation.

## Feedback and recovery

| Situation | Message | Next step |
|---|---|---|
| Play succeeds | Playback started. | Say the next command. |
| Pause succeeds | Playback paused. | The player remains open. |
| Unsupported input | That command is not supported. Say Play, Pause, Resume, Volume Up, Volume Down, Next or Previous. | Use one of the listed phrases. |
| No speech detected | No speech was detected. Please say a command. | Say a command. |
| Speech cannot be recognized | The speech could not be recognized. Please repeat the command. | Repeat the phrase clearly. |
| Microphone unavailable | Voice input is unavailable: the microphone could not be used. | Check the microphone before restarting. |
| Player failure | The media player could not complete that operation. | Check that media and the player are available, then retry. |
| Hardware failure | The hardware interface is unavailable. No action was performed. | Check the hardware before restarting. |
| Controller operation not implemented | That operation is not available yet. | Use an implemented command for this sprint demonstration. |

No-speech, unrecognized-input, unsupported-command and player failures allow
another attempt. The listening loop stops on microphone or hardware failure.
These are the existing error-handling rules from #13; this story changes the
success and unsupported-command wording for usability.

## Usability walkthrough

From the repository root, install the test dependencies and run the demo:

```bash
python -m pip install -r requirements-dev.txt
python -m voice_assistant.demo
```

The demo takes typed transcripts and uses `InMemoryPlayer`. It runs the normal
recognition, validation, controller and feedback code, but does not capture
microphone audio or play a media file. Its startup message states this.

| Step | Type | Expected observation |
|---|---|---|
| 1 | `help` | The seven allowed phrases are listed. No player action occurs. |
| 2 | `Play` | "Playback started." State becomes `playing`. |
| 3 | `Pause` | "Playback paused." State becomes `paused`. |
| 4 | `shuffle` | Unsupported-command feedback lists the valid phrases. State stays `paused`. |
| 5 | Press Enter without text | Simulated no-speech feedback asks for a command. State stays `paused`. |
| 6 | `Resume` | This branch reports the operation unavailable. State stays `paused`. |
| 7 | `quit` | The demo exits. |

`help` and `quit` are demo controls, not additional voice commands.
To show a failed player request, restart with:

```bash
python -m voice_assistant.demo --fail-play
```

Enter `Play`. The player-failure message appears and the state stays `stopped`.
The demo must not report that playback started. Enter `quit` to exit.
EOF or Ctrl+C also ends the demo cleanly.

## Requirement checks

| Requirement / criterion | Verification |
|---|---|
| FR-03 / TC-02: Play starts the selected media | `tests/test_play.py` checks the backend call, `playing` state, selection, volume and player availability. |
| Invalid commands never invoke Play | `tests/test_play.py` checks empty, unsupported and multi-command transcripts for zero backend calls. |
| Failed Play is reported safely | `tests/test_play.py` checks rejected operations, unexpected backend faults and a backend that does not enter `playing`. |
| NFR-02: supported commands are documented | The command table above lists the exact seven SRS phrases and their availability. |
| NFR-02: understandable feedback | `tests/test_usability.py` checks success messages, allowed-phrase guidance and capture/player error messages. |
| NFR-02: basic walkthrough | `tests/test_usability.py` exercises the walkthrough, simulated player failure and clean exit. |

Verification ran on 22 October 2026 (IST):

| Environment | Result |
|---|---|
| Windows, Python 3.12.10, pytest 9.1.1 | 82 tests passed. |
| Kali Linux under WSL 2, Python 3.14.7, pytest 9.1.1 | 82 tests passed. |
| Windows dependency check | `pip check` reported no broken requirements. |
| Transcript walkthrough and simulated player failure | Both commands exited with code 0 and produced the feedback shown above. |

[Test output](./evidence/sprint-1-cs805-tests.txt) and
[walkthrough output](./evidence/sprint-1-cs805-walkthrough.txt) retain the run time,
base commit, checksums of the tested Python files, commands and exit codes.
These are software checks with a simulated player and injected failures. They
do not establish speech-recognition accuracy, audible playback or usability
with independent participants.

## Remaining physical check

The PDF's full TC-02 expects selected media to start playing in the intended
hardware environment. This has not been tested on Raspberry Pi, a microphone or
a physical media-player backend here. To complete that check, connect the target
hardware and media backend, select a known playable file, say "Play", and record
whether the selected item is audibly or visibly playing. Record the hardware,
backend, file, date and result from that actual run. Do not mark this as a passed
hardware test based on the transcript demo.

Volume (#16) and target-hardware portability (#21) remain assigned Sprint 2
work for 26-30 October 2026.
