# History: `chore/autonomous-commit-policy`

Append-only milestones. Current state belongs in [autonomous-commit-policy.md](autonomous-commit-policy.md).

### 2026-08-13 — Branch created for autonomous commits
- Commit/base: `76540cc` on `chore/model-routing-policy`
- Change: Began a separate policy for automatic checkpoint commits and explicit authorization for Git deletion, discard, or ancestry-changing operations.
- Validation/decision: Keep normal commits autonomous because they preserve recoverable history; keep destructive and history-altering commands behind exact authorization.

### 2026-08-13 — Git workflow policy implemented
- Commit/base: checkpoint on `chore/autonomous-commit-policy`, based on `76540cc`
- Change: Added narrow branch, exact staging, automatic checkpoint commit, conflict/recovery, and explicit destructive-operation rules; reconciled worktree and stash cleanup guidance.
- Validation/decision: Structural validation, 42 standard-library tests, and `git diff --check` passed. Push, PR, merge, release/tag creation, deletion, discard, and ancestry-changing commands remain authorization-gated.
