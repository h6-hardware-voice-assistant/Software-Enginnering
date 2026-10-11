# GitHub Projects V2 Setup — Team H6

This guide is for the **group mini-project only**: Hardware-Based Voice Assistant for Multimedia Controls. The solo `53_arm_wrestle` VibeCoding task is stored in the separate `PES1UG24CS484-pes-vcs/Lab-4` path.

## Already prepared in this repository
- Issues **#1–#6** are the six Epics.
- Issues **#7–#23** are the 17 Stories.
- Story issue descriptions include acceptance criteria, requirement traceability, proposed story points, priority, sprint plan, suggested owner, and a Jira issue link.
- Each GitHub Story has a corresponding Jira Story with a story-point estimate and sprint assignment.
- `BACKLOG.md` contains the full table and Jira mapping.

## One-time board creation (GitHub UI)
The available GitHub connector can manage Issues and files, but it cannot create/configure Projects V2 boards. Use the GitHub website:

1. Open [your GitHub Projects page](https://github.com/users/ignite-2005/projects).
2. Select **New project** and choose **Board**.
3. Name it **H6 — Hardware-Based Voice Assistant Backlog**.
4. Add the existing issues from this repository. Add Epic issues **#1–#6** and Story issues **#7–#23**. Do not create duplicate issues.
5. Add/confirm these fields:
   - **Work Type** — single select: `Epic`, `Story`.
   - **Story Points** — number.
   - **Priority** — single select: `High`, `Medium`, `Low`.
   - **Iteration** — an iteration field with `Sprint 1` and `Sprint 2`.
   - **Status** — Todo / In Progress / Done (the default status field is fine).
6. Set **Work Type** to Epic for #1–#6 and Story for #7–#23.
7. Set Story Points and Priority from `BACKLOG.md`; the planned story-point totals are Sprint 1 = **28** and Sprint 2 = **20**.
8. Assign the Story cards after the collaborators' repository roles are updated.

## Required account-access step before assigning teammates
The repository currently reports `read` permission for `@DerpSpears`, `@shivanibr0512-cmyk`, and `@arpan-joardar`. GitHub did not retain issue assignments to these accounts. A repo owner must change each collaborator's role to **Write** (or another role that allows issue assignment):

1. Open [Manage access](https://github.com/ignite-2005/Software-Enginnering/settings/access).
2. Under collaborators, change the role for:
   - `@DerpSpears` — Shriniketh Kana, PES1UG24CS446
   - `@shivanibr0512-cmyk` — Shivani B R, PES1UG24CS439
   - `@arpan-joardar` — Arpan Joardar, PES1UG25CS805
3. Choose **Write** and save; if the UI requires it, send/re-send the invite and ask the teammate to accept it.
4. Return to this repository's [Issues page](https://github.com/ignite-2005/Software-Enginnering/issues) and retry assignments. The current account `@ignite-2005` is already assigned to the stories owned by Surjo.

## Jira access limitation
The Jira board and all 23 H6 issues are configured under the existing `SCRUM` project. The connected Atlassian directory currently returns only Surjo as assignable. The three teammates must be invited/added to the `ignite005.atlassian.net` Jira site/project with Jira access before their Jira issues can be assigned.

## Roster used
- Surjo Sarkar — PES1UG24CS484 — `@ignite-2005`
- Shriniketh Kana — PES1UG24CS446 — `@DerpSpears`
- Shivani B R — PES1UG24CS439 — `@shivanibr0512-cmyk`
- Arpan Joardar — PES1UG25CS805 — `@arpan-joardar`

Arpan's SRN PES1UG25CS805 is confirmed by the student; the mini-project PDF's PES1UG24CS805 entry is treated as stale.
