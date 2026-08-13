# Branch: `chore/streamline-agent-rules`

## Objective

- Goal: Reduce routine coordination overhead while improving permission reuse and evidence-backed platform discovery.
- Included: Three coordination tiers, optional strict current-branch validation, compact lifecycle routing, a platform smoke matrix, exact standing permission grants, and the multi-agent base-update correction.
- Excluded: Automated installer/updater work, live testing every supported IDE, branch deletion, or history rewriting.
- Acceptance criteria: Routine branches need no handoff; durable/concurrent work remains strict; no guide recommends implicit pull integration; grants are exact and deny-by-default; registered entry points appear in the smoke matrix.

## Constraints and decisions

- Base/PR target: `main`, after `chore/cleanup-artifact-policy`
- Role: chore
- Coordination tier: durable
- Worktree: primary checkout; no concurrent agents
- Owned paths: agent policies, validator/tests, documentation, and this branch's handoff records
- History: [streamline-agent-rules.history.md](streamline-agent-rules.history.md)
- Decisions: Tier selection is based on recovery/coordination value, not branch existence. Standing grants require owner-recorded exact scope and cannot authorize force/history/unknown-work destruction.

## Risks or blockers

- The preceding feature branches are committed but not yet merged into `main`; this branch intentionally carries their linear stack.
- Live platform discovery remains unverified until each client is smoke-tested; the matrix must not imply otherwise.

## Next action

Commit the validated policy update, merge it into `main`, and verify reachability and final status. Do not delete branches without separate authorization or a matching grant.

## Validation checkpoint

Passed on Windows 2026-08-13:

- `py -3 scripts/validate_handoffs.py --quiet --require-current-handoff`
- `py -3 -m unittest discover -s scripts -p 'test_*.py'` — 47 tests
- `git diff --check`

## Merge and cleanup

- Primary checkout: `H:\Desktop\ai_agent_guides`
- After merge: verify reachability and update durable closure records. Branch/worktree deletion still requires an exact grant or fresh authorization.
