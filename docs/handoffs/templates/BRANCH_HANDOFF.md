# Branch: `<branch-name>`

## Objective

- Goal: `<why this branch exists>`
- Included: `<bounded scope>`
- Excluded: `<important non-goals>`
- Acceptance criteria: `<observable completion conditions>`

## Constraints and decisions

- Base/PR target: `<branch>`
- Role: `<feature/fix/chore/integration>`
- Worktree: `<sibling path; one branch only>`
- Owned paths: `<paths this branch may edit; no-go paths if useful>`
- History: [<filename>.history.md](<filename>.history.md)
- Decisions: `<durable owner or implementation decisions>`

## Risks or blockers

`<Unresolved issue affecting continuation, or none>`

## Next action

`<One immediate safe action>`

## Validation checkpoint

`<Latest meaningful commands/results, explicit deferrals, or not yet required>`

## Merge and cleanup

- Primary checkout: `<path used for merge/cleanup>`
- After merge: verify reachability and archive this handoff/history; obtain explicit authorization before removing the sibling worktree or deleting local/remote branches.

Do not routinely copy tip, clean/dirty state, upstream tracking, ahead/behind counts, or complete stash inventory from Git. Record identifiers only when essential to recovery or a durable milestone.

<!-- Filled example, for calibration. Delete this comment when you fill the template.

# Branch: `feature/session-expiry`

## Objective
- Goal: Log users out after 30 minutes of inactivity; the current session never expires.
- Included: Idle timeout, refresh-on-activity, the logout redirect.
- Excluded: Password rotation and MFA. Absolute session lifetime stays as-is.
- Acceptance criteria: An idle session rejects the next API call and redirects to /login; an active one never expires mid-use.

## Constraints and decisions
- Base/PR target: main
- Role: feature
- Worktree: ../app-wt-session-expiry
- Owned paths: src/auth/**, tests/auth/**. No-go: src/billing/**.
- History: [feature/session-expiry.history.md](session-expiry.history.md)
- Decisions: Owner chose idle timeout over absolute lifetime, so long editing sessions are not interrupted. 30 minutes is a product decision, not a technical one.

## Risks or blockers
The mobile client refreshes tokens on its own schedule and may log users out early. Unverified; needs a device check before merge.

## Next action
Add the idle-timeout branch to `RefreshTokenHandler`, then run the auth suite.

## Validation checkpoint
`pytest tests/auth -q` passes (41 tests). Mobile device check deferred; recorded above as a risk.

Note what the example does NOT contain: the current SHA, whether the tree is dirty,
ahead/behind counts. Git answers those, and copying them here only creates stale text.
-->

