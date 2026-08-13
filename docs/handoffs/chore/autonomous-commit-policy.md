# Branch: `chore/autonomous-commit-policy`

## Objective

- Goal: Make normal commits autonomous and automatic while requiring explicit authorization for deletion, discarded work, and Git history/ancestry changes.
- Included: Evergreen Git best practices, branch/staging/commit defaults, destructive-action boundaries, documentation, and validator/test coverage.
- Excluded: Automatic push, PR, merge, release, cleanup deletion, or history rewrite; merging predecessor branches.
- Acceptance criteria: Agents create narrow branches, stage only owned files, commit coherent validated checkpoints without asking, and never delete or change ancestry without exact authorization.

## Constraints and decisions

- Base/PR target: `main`, after `chore/model-routing-policy`
- Role: chore
- Worktree: primary checkout; no concurrent agents on this work
- Owned paths: agent rules, Git policy documentation, validator/tests, and this branch's records
- History: [autonomous-commit-policy.history.md](autonomous-commit-policy.history.md)
- Decisions: A normal commit is additive and recoverable, so it is standing-authorized. Amend, rebase, reset, revert, cherry-pick, force-update, deletion, and discard operations require explicit authorization because they can alter ancestry or destroy recoverable state.

## Risks or blockers

- The flattened layout and model-routing predecessor branches are committed but not merged into `main`.
- Broad phrases such as “clean up” or “sync” must not be interpreted as deletion authorization.

## Next action

Await authorization for any push, merge, or cleanup deletion after the automatic checkpoint commit.

## Validation checkpoint

Passed on Windows 2026-08-13:

- `py -3 scripts\validate_handoffs.py --quiet`
- `py -3 -m unittest discover -s scripts -p 'test_*.py'` — 42 tests
- `git diff --check`

## Merge and cleanup

- Primary checkout: `H:\Desktop\ai_agent_guides`
- After merge: verify reachability and archive/commit this handoff. Request explicit authorization before deleting this branch or removing any worktree.
