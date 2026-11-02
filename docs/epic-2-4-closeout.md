# Epic #2 and Epic #4 — closure record

**Owner:** Shriniketh Kana — PES1UG24CS446 — `@DerpSpears`
**Scope:** the two tracking epics assigned to CS446. Both are closed on the
evidence below; neither epic contained unbuilt child work at closure time.
**Verified against:** `main` at merge of PR #30 (`ee04378`), plus the two test
additions in this branch.
**Raw test and coverage output:** [`evidence/epic-2-4-closure-cs446.txt`](./evidence/epic-2-4-closure-cs446.txt)

Suite at closure: **130 tests passing**. Line coverage of the modules these two
epics own: `processor.py` 100%, `errors.py` 100%, `assistant.py` 96%,
`player.py` 88%, `controller.py` 83% (the uncovered controller lines are the
`increase_volume` / `decrease_volume` stubs owned by story #16 and defensive
re-raise branches).

---

## Epic #2 — Multimedia Playback and Navigation

**Stated outcome:** *"Each recognized command performs the matching player
action and preserves playback state as required."*
**Traceability:** FR-03, FR-04, FR-05, FR-08, FR-09.

| Child | Requirement | Implementation on `main` | Verification | Result |
|---|---|---|---|---|
| #9 | FR-03 / TC-02 | `controller.play_media()` → `player.play()`, asserts the player reached `playing` | `tests/test_play.py` (16) | Verified |
| #10 | FR-04 / TC-03 | `controller.pause_media()`, pauses only while playing, player stays open | `tests/test_pause.py` (8) | Verified |
| #11 | FR-05 | `controller.resume_media()`, resumes only from `paused` | `tests/test_resume.py` (4) | Verified |
| #17 | FR-08 / TC-07 | `controller.next_media()` → `player.next_item()` | `tests/test_next_media.py` (3) | Verified |
| #18 | FR-09 / TC-08 | `controller.previous_media()` → `player.previous_item()` | `tests/test_previous_media.py` (3) | Verified |

**One-to-one routing.** `processor.COMMAND_ROUTES` maps each command to exactly
one controller method, and `tests/test_command_allowlist.py` drives all seven
spoken phrases through `recognize_command()` → `process_command()` and asserts
exactly one operation is called per phrase.

**Gap found and closed during this review.** The five story test files each
check their own operation at the controller level, and none of them asserted
the second half of the epic's outcome — that navigation *preserves playback
state*. The behaviour was already correct in the merged code, but nothing would
have caught a regression. `tests/test_epic2_playback_integrity.py` (13 tests)
now asserts, at the epic level:

- each spoken command (`Play`, `Pause`, `Resume`, `Next`, `Previous`) reaches
  exactly one player operation end to end through `VoiceAssistant`;
- `Next` / `Previous` leave a playing player playing and a paused player paused;
- navigation changes only the selected item — volume and the open player are
  untouched;
- a navigation failure at a playlist edge is reported and changes nothing;
- the sequence `Pause` → `Next` → `Resume` composes and ends playing the newly
  selected item.

Confirmed non-vacuous: forcing `InMemoryPlayer.next_item()` to stop playback
fails 4 of these tests; the suite was green before and after the mutation was
reverted.

**Administrative note.** Child story **#9 is still open** although its code
merged in `d3b5503`/`f9ecc98` and is verified above. Closing it belongs to its
assignee, `@arpan-joardar`; Epic #2 is closed on the implementation evidence
rather than on #9's issue state.

---

## Epic #4 — Command Validation and Error Handling

**Stated outcome / security invariant:** *"No multimedia action is dispatched
until the recognized command is validated against the predefined command
allow-list."*
**Traceability:** FR-10, FR-11, SR-01, SR-02, NFR-04.

| Child | Requirement | Implementation on `main` | Verification | Result |
|---|---|---|---|---|
| #12 | FR-10, NFR-04, SR-01/02 | `commands.is_supported()` type-and-membership check; `processor.process_command()` rejects before any `getattr` dispatch | `tests/test_command_allowlist.py` (12) | Verified |
| #13 | FR-11 | `errors.py` typed failures with user-facing messages; `assistant.VoiceAssistant` converts every failure into an `Outcome` | `tests/test_error_handling.py` (19) | Verified |

**Invariant enforcement point.** `processor.py` checks
`is_supported(command) and command in COMMAND_ROUTES` and raises
`UnsupportedCommandError` *before* resolving a controller method, so an
unsupported candidate cannot reach the player. `test_command_allowlist.py`
asserts this for `None`, a bare string, a list, an int and an unrecognized
transcript, each time checking the controller recorded no calls.

**All six SAD failure cases are covered** — no speech, unrecognized speech,
unsupported command, microphone unavailable, player operation failure and
hardware interface failure — each asserting that no multimedia operation was
dispatched and that the user-facing message is understandable (NFR-02).

**Defect found and fixed during this review.**
`test_an_unbuilt_operation_does_not_fall_through_to_another_operation` was
written against the phrase `Resume`. When story #11 merged, `resume_media()`
became a real operation, so the test stopped exercising the
`NotImplementedError` guard in `assistant.py` it was written to protect and
instead only re-checked that an inapplicable `Resume` is inert. It still
passed, which is why the drift was invisible.

The test now runs against `Volume Up` / `Volume Down` — the operations that are
genuinely unbuilt (story #16) — and asserts the reported status, the
"not available yet" message, that no controller call reached the player and
that playback state is unchanged. The behaviour the old test had drifted into
checking is kept as its own test,
`test_resume_with_nothing_paused_performs_no_operation`.

Confirmed non-vacuous: removing the `NotImplementedError` handler from
`assistant.py` fails both parametrized cases. Before this fix the guard was
reached only incidentally, by the story #15 demo walkthrough in
`tests/test_usability.py`, and not by any FR-11 test.

---

## Handoff — not in this epic closure

These remain open and belong to other assignees; Epic #2 and Epic #4 do not
depend on them.

| Item | Owner | Note |
|---|---|---|
| #9 | `@arpan-joardar` | Implemented and verified; issue needs closing |
| #16 volume up/down | `@arpan-joardar` | The only unbuilt commands; `controller.increase_volume` / `decrease_volume` still raise `NotImplementedError` |
| #20 module separation | `@ignite-2005` | Sprint 2 |
| #21 target hardware | `@arpan-joardar` | Sprint 2 |
| #23 documentation | `@ignite-2005` | Sprint 2. Note the `README.md` module table is now stale: it still states that only `play_media` and `pause_media` are implemented, but `resume_media`, `next_media` and `previous_media` all landed in Sprint 1–2. Left for #23 rather than edited here. |
