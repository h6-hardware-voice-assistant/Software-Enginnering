# Mini Project Backlog — Hardware-Based Voice Assistant for Multimedia Controls

Team H6. Source of requirements: MINI PROJECT.pdf (SRS, Test Plan and SAD bundled in the existing document).

## Sprint plan

| Sprint | Dates | Planned total |
|---|---|---:|
| Sprint 1 | 19–23 Oct 2026 | 28 points |
| Sprint 2 | 26–30 Oct 2026 | 20 points |

Story points use a simple Fibonacci-like planning scale (1, 2, 3, 5, 8). Estimates are proposed sizing, not instructor-approved values. The SRS gives no numeric threshold for NFR-01 latency, so its target needs team/instructor confirmation.

## Epics

| Epic | Scope | GitHub issue |
|---|---|---|
| Epic 1 | Voice input and command recognition | [#1](https://github.com/ignite-2005/Software-Enginnering/issues/1) |
| Epic 2 | Playback and navigation | [#2](https://github.com/ignite-2005/Software-Enginnering/issues/2) |
| Epic 3 | Volume controls | [#3](https://github.com/ignite-2005/Software-Enginnering/issues/3) |
| Epic 4 | Command validation and error handling | [#4](https://github.com/ignite-2005/Software-Enginnering/issues/4) |
| Epic 5 | Quality attributes and hardware portability | [#5](https://github.com/ignite-2005/Software-Enginnering/issues/5) |
| Epic 6 | Automated verification and delivery | [#6](https://github.com/ignite-2005/Software-Enginnering/issues/6) |

## Story backlog

| Issue | User story | SP | Priority | Sprint | Requirement mapping | Suggested owner SRN |
|---|---|---:|---|---|---|---|
| [#7](https://github.com/ignite-2005/Software-Enginnering/issues/7) | Capture microphone input | 3 | High | 1 | FR-01, FR-11, TC-01 | PES1UG24CS484 |
| [#8](https://github.com/ignite-2005/Software-Enginnering/issues/8) | Recognize predefined command vocabulary | 5 | High | 1 | FR-02, TC-01 | PES1UG24CS446 |
| [#9](https://github.com/ignite-2005/Software-Enginnering/issues/9) | Start playback on Play | 3 | High | 1 | FR-03, TC-02 | PES1UG24CS484 |
| [#10](https://github.com/ignite-2005/Software-Enginnering/issues/10) | Pause current media | 2 | High | 1 | FR-04, TC-03 | PES1UG24CS446 |
| [#11](https://github.com/ignite-2005/Software-Enginnering/issues/11) | Resume paused media | 2 | Medium | 1 | FR-05, TC-04 | PES1UG24CS439 |
| [#12](https://github.com/ignite-2005/Software-Enginnering/issues/12) | Validate recognized command allow-list | 3 | High | 1 | FR-10, NFR-04, SR-01/02 | PES1UG24CS484 |
| [#13](https://github.com/ignite-2005/Software-Enginnering/issues/13) | Handle microphone/player failures safely | 3 | High | 1 | FR-11 | PES1UG24CS446 |
| [#14](https://github.com/ignite-2005/Software-Enginnering/issues/14) | Measure command latency | 2 | Medium | 1 | NFR-01 | PES1UG24CS439 |
| [#15](https://github.com/ignite-2005/Software-Enginnering/issues/15) | Keep commands and feedback understandable | 2 | Medium | 1 | NFR-02 | PES1UG24CS805 |
| [#22](https://github.com/ignite-2005/Software-Enginnering/issues/22) | Run tests on pushes and PRs | 3 | High | 1 | Test plan, NFR-03 | PES1UG24CS484 |
| [#16](https://github.com/ignite-2005/Software-Enginnering/issues/16) | Volume Up and Volume Down | 3 | High | 2 | FR-06/07, TC-05/06 | PES1UG24CS805* |
| [#17](https://github.com/ignite-2005/Software-Enginnering/issues/17) | Select next media item | 2 | Medium | 2 | FR-08, TC-07 | PES1UG24CS439 |
| [#18](https://github.com/ignite-2005/Software-Enginnering/issues/18) | Select previous media item | 2 | Medium | 2 | FR-09, TC-08 | PES1UG24CS439 |
| [#19](https://github.com/ignite-2005/Software-Enginnering/issues/19) | Verify correct, repeatable behavior | 3 | High | 2 | NFR-03, TC-01–08 | PES1UG24CS446 |
| [#20](https://github.com/ignite-2005/Software-Enginnering/issues/20) | Separate recognition/processing/control modules | 3 | Medium | 2 | NFR-05, SAD | PES1UG24CS484 |
| [#21](https://github.com/ignite-2005/Software-Enginnering/issues/21) | Verify Raspberry Pi/compatible target | 5 | Medium | 2 | NFR-06 | PES1UG24CS805* |
| [#23](https://github.com/ignite-2005/Software-Enginnering/issues/23) | Document setup, command mapping and evidence | 2 | Medium | 2 | SRS/SAD/Test Plan | PES1UG24CS446 |

**Confirmed team roster:** PES1UG24CS446, PES1UG24CS805, PES1UG24CS439, and PES1UG24CS484. The SRNs in this table are suggested task owners, not GitHub account assignments; the source materials do not provide the team members' GitHub usernames.

## GitHub Projects configuration still needed

A GitHub Projects V2 board should be created and linked to this repository. Add the 6 Epic issues and 17 Story issues above; configure fields:
- Status: Todo / In Progress / Done
- Estimate (number): use the SP values above
- Priority: High / Medium / Low
- Iteration: Sprint 1 (19–23 Oct 2026), Sprint 2 (26–30 Oct 2026)
- Assignees: assign actual GitHub usernames once the team handles are confirmed

The available GitHub connector can create/inspect repository files and issues, but it does not expose Projects V2 board/field mutations. The Issues backlog is live on GitHub; the actual board, Estimate/Iteration fields and person-level assignments are not claimed complete in this file.
