# History: `<branch-name>`

Append-only milestones. Current state belongs in [`<handoff>.md`](<handoff>.md).

### YYYY-MM-DD — Branch created
- Commit/base: `<parent>` at `<sha>`
- Change: Created `<branch-name>` for `<goal>`.
- Validation/decision: Scope and acceptance criteria recorded.

<!-- Append meaningful milestones below. Never rewrite/reorder older entries.
Roll over before 12,000 characters: freeze this file and continue in
`<branch>.history.2.md`, then `.3.md`.

### YYYY-MM-DD — Short milestone
- Commit/base: `<sha>`
- Change: <one or two sentences>
- Validation/decision: <concise result>

Calibration — the test is whether an agent resuming this branch would act
differently without the entry.

WORTH APPENDING:
### 2026-03-14 — Idle timeout replaces absolute session lifetime
- Commit/base: `a1b2c3d`
- Change: Owner rejected the absolute-lifetime approach after it logged users out mid-edit. Reimplemented as an idle timer that refreshes on activity.
- Validation/decision: Auth suite green (41 tests). Reverting to absolute lifetime would reintroduce the reported bug.

NOT WORTH APPENDING (Git already answers these, or nothing downstream changes):
- "Read the auth module and reviewed the token handler."
- "Fixed a typo in a comment."
- "Committed a1b2c3d on feature/session-expiry."
- "Ran the test suite; it passed." (record only when the result changes what happens next)
-->

