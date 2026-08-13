# Branch: `chore/cleanup-artifact-policy`

## Objective

- Goal: Define safe cleanup of temporary debug, research, and testing artifacts after user confirmation while retaining durable regression and compatibility coverage.
- Included: Candidate criteria, exact confirmation, regression-test retention, durable deletion notes, focused validation/commit behavior, and test/documentation coverage.
- Excluded: Deleting any current repository artifacts, automatic cleanup without confirmation, or merging predecessor branches.
- Acceptance criteria: “Clean up” inventories rather than deletes; exact targets require confirmation; deletion purpose/disposition survives; regression and backward-compatibility assets remain.

## Constraints and decisions

- Base/PR target: `main`, after `chore/autonomous-commit-policy`
- Role: chore
- Worktree: primary checkout; no concurrent agents on this work
- Owned paths: cleanup policy text, documentation/tests, and this branch's handoff records
- History: [cleanup-artifact-policy.history.md](cleanup-artifact-policy.history.md)
- Decisions: A durable deletion note belongs in the active handoff/history or existing decision log. Tracked deletions and the note form one automatic checkpoint commit after exact confirmation.

## Risks or blockers

- The predecessor branches are committed but not merged into `main`.
- Temporary-looking tests may contain durable regression value; uncertainty defaults to keeping them.

## Next action

Await authorization for push or merge after the automatic checkpoint commit. No repository artifacts were deletion candidates in this policy-only task.

## Validation checkpoint

Passed on Windows 2026-08-13:

- `py -3 scripts\validate_handoffs.py --quiet`
- `py -3 -m unittest discover -s scripts -p 'test_*.py'` — 43 tests
- `git diff --check`

## Merge and cleanup

- Primary checkout: `H:\Desktop\ai_agent_guides`
- After merge: verify reachability and archive/commit this handoff. Request explicit authorization before deleting this branch or removing any worktree.
