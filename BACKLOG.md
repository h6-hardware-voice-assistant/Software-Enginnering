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

| Issue | User story | SP | Priority | Sprint | Requirement mapping | Suggested owner (SRN / GitHub) |
|---|---|---:|---|---|---|---|
| [#7](https://github.com/ignite-2005/Software-Enginnering/issues/7) | Capture microphone input | 3 | High | 1 | FR-01, FR-11, TC-01 | PES1UG24CS484 / @ignite-2005 |
| [#8](https://github.com/ignite-2005/Software-Enginnering/issues/8) | Recognize predefined command vocabulary | 5 | High | 1 | FR-02, TC-01 | PES1UG24CS446 / @DerpSpears |
| [#9](https://github.com/ignite-2005/Software-Enginnering/issues/9) | Start playback on Play | 3 | High | 1 | FR-03, TC-02 | PES1UG24CS484 / @ignite-2005 |
| [#10](https://github.com/ignite-2005/Software-Enginnering/issues/10) | Pause current media | 2 | High | 1 | FR-04, TC-03 | PES1UG24CS446 / @DerpSpears |
| [#11](https://github.com/ignite-2005/Software-Enginnering/issues/11) | Resume paused media | 2 | Medium | 1 | FR-05, TC-04 | PES1UG24CS439 / @shivanibr0512-cmyk |
| [#12](https://github.com/ignite-2005/Software-Enginnering/issues/12) | Validate recognized command allow-list | 3 | High | 1 | FR-10, NFR-04, SR-01/02 | PES1UG24CS484 / @ignite-2005 |
| [#13](https://github.com/ignite-2005/Software-Enginnering/issues/13) | Handle microphone/player failures safely | 3 | High | 1 | FR-11 | PES1UG24CS446 / @DerpSpears |
| [#14](https://github.com/ignite-2005/Software-Enginnering/issues/14) | Measure command latency | 2 | Medium | 1 | NFR-01 | PES1UG24CS439 / @shivanibr0512-cmyk |
| [#15](https://github.com/ignite-2005/Software-Enginnering/issues/15) | Keep commands and feedback understandable | 2 | Medium | 1 | NFR-02 | PES1UG25CS805 / @arpan-joardar |
| [#22](https://github.com/ignite-2005/Software-Enginnering/issues/22) | Run tests on pushes and PRs | 3 | High | 1 | Test plan, NFR-03 | PES1UG24CS484 / @ignite-2005 |
| [#16](https://github.com/ignite-2005/Software-Enginnering/issues/16) | Volume Up and Volume Down | 3 | High | 2 | FR-06/07, TC-05/06 | PES1UG25CS805 / @arpan-joardar |
| [#17](https://github.com/ignite-2005/Software-Enginnering/issues/17) | Select next media item | 2 | Medium | 2 | FR-08, TC-07 | PES1UG24CS439 / @shivanibr0512-cmyk |
| [#18](https://github.com/ignite-2005/Software-Enginnering/issues/18) | Select previous media item | 2 | Medium | 2 | FR-09, TC-08 | PES1UG24CS439 / @shivanibr0512-cmyk |
| [#19](https://github.com/ignite-2005/Software-Enginnering/issues/19) | Verify correct, repeatable behavior | 3 | High | 2 | NFR-03, TC-01–08 | PES1UG24CS446 / @DerpSpears |
| [#20](https://github.com/ignite-2005/Software-Enginnering/issues/20) | Separate recognition/processing/control modules | 3 | Medium | 2 | NFR-05, SAD | PES1UG24CS484 / @ignite-2005 |
| [#21](https://github.com/ignite-2005/Software-Enginnering/issues/21) | Verify Raspberry Pi/compatible target | 5 | Medium | 2 | NFR-06 | PES1UG25CS805 / @arpan-joardar |
| [#23](https://github.com/ignite-2005/Software-Enginnering/issues/23) | Document setup, command mapping and evidence | 2 | Medium | 2 | SRS/SAD/Test Plan | PES1UG24CS446 / @DerpSpears |

**Team roster mapped from uploaded `5H_VibeCodingGitRepoLinks.xlsx`:** PES1UG24CS446 / @DerpSpears, PES1UG24CS439 / @shivanibr0512-cmyk, PES1UG25CS805 / @arpan-joardar, and PES1UG24CS484 / @ignite-2005. Actual GitHub issue assignments have now been set to these accounts. The mini-project PDF previously listed PES1UG24CS805 for Arpan; confirm this source discrepancy with the team/instructor.

## GitHub Projects configuration still needed

A GitHub Projects V2 board should be created and linked to this repository. Add the 6 Epic issues and 17 Story issues above; configure fields:
- Status: Todo / In Progress / Done
- Estimate (number): use the SP values above
- Priority: High / Medium / Low
- Iteration: Sprint 1 (19–23 Oct 2026), Sprint 2 (26–30 Oct 2026)
- Assignees: assign actual GitHub usernames once the team handles are confirmed

The Epic/Story issues and this backlog register are live on GitHub. The actual GitHub Projects V2 board and its Estimate/Iteration fields are not yet configured. GitHub assignment attempts were verified against issue records: only @ignite-2005 assignments succeeded; the three teammate accounts have read-level repository permission, so their issues remain unassigned until repository access is upgraded. The linked Jira board has the Epic/Story issues, Story point estimates, priorities, and Sprint 1/2 assignments; teammates remain unassigned in Jira because no matching assignable accounts were returned.

## Keep the two lab projects separate
- **Solo VibeCoding task:** `53_arm_wrestle`, committed under `Lab-4/` in [PES1UG24CS484-pes-vcs](https://github.com/ignite-2005/PES1UG24CS484-pes-vcs/tree/main/Lab-4).
- **Group mini-project:** Hardware-Based Voice Assistant for Multimedia Controls, with team SRNs listed above, tracked in this repository.


## Jira cross-reference

The group mini-project backlog has also been created in the connected Jira site under the existing `SCRUM` project, with label `group-mini-project`. This is kept separate from the solo bug-fixing project.

| GitHub issue | Jira issue |
|---|---|
| Epic #1 — Voice input | [SCRUM-6](https://YOUR-JIRA-SITE/browse/SCRUM-6) |
| Epic #2 — Playback/navigation | [SCRUM-7](https://YOUR-JIRA-SITE/browse/SCRUM-7) |
| Epic #3 — Volume | [SCRUM-8](https://YOUR-JIRA-SITE/browse/SCRUM-8) |
| Epic #4 — Validation/errors | [SCRUM-9](https://YOUR-JIRA-SITE/browse/SCRUM-9) |
| Epic #5 — Quality/hardware | [SCRUM-10](https://YOUR-JIRA-SITE/browse/SCRUM-10) |
| Epic #6 — Automation/delivery | [SCRUM-11](https://YOUR-JIRA-SITE/browse/SCRUM-11) |
| Story #7 | [SCRUM-12](https://YOUR-JIRA-SITE/browse/SCRUM-12) |
| Story #8 | [SCRUM-13](https://YOUR-JIRA-SITE/browse/SCRUM-13) |
| Story #9 | [SCRUM-14](https://YOUR-JIRA-SITE/browse/SCRUM-14) |
| Story #10 | [SCRUM-15](https://YOUR-JIRA-SITE/browse/SCRUM-15) |
| Story #11 | [SCRUM-16](https://YOUR-JIRA-SITE/browse/SCRUM-16) |
| Story #12 | [SCRUM-17](https://YOUR-JIRA-SITE/browse/SCRUM-17) |
| Story #13 | [SCRUM-18](https://YOUR-JIRA-SITE/browse/SCRUM-18) |
| Story #14 | [SCRUM-19](https://YOUR-JIRA-SITE/browse/SCRUM-19) |
| Story #15 | [SCRUM-20](https://YOUR-JIRA-SITE/browse/SCRUM-20) |
| Story #16 | [SCRUM-21](https://YOUR-JIRA-SITE/browse/SCRUM-21) |
| Story #17 | [SCRUM-22](https://YOUR-JIRA-SITE/browse/SCRUM-22) |
| Story #18 | [SCRUM-23](https://YOUR-JIRA-SITE/browse/SCRUM-23) |
| Story #19 | [SCRUM-24](https://YOUR-JIRA-SITE/browse/SCRUM-24) |
| Story #20 | [SCRUM-25](https://YOUR-JIRA-SITE/browse/SCRUM-25) |
| Story #21 | [SCRUM-26](https://YOUR-JIRA-SITE/browse/SCRUM-26) |
| Story #22 | [SCRUM-27](https://YOUR-JIRA-SITE/browse/SCRUM-27) |
| Story #23 | [SCRUM-28](https://YOUR-JIRA-SITE/browse/SCRUM-28) |

Jira Sprint 1 is `H6 Voice Assistant — Sprint 1` (19–23 Oct 2026, 28 points); Sprint 2 is `H6 Voice Assistant — Sprint 2` (26–30 Oct 2026, 20 points). The custom `Story point estimate` field, priority and sprint have been written to each Jira Story. Team-member Jira accounts could not be resolved as assignable users; Jira assignee fields remain blank.
