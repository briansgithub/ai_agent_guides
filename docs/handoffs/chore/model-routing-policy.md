# Branch: `chore/model-routing-policy`

## Objective

- Goal: Audit the flattened ruleset and add token-aware model routing to every formal plan.
- Included: Runtime identity handling, per-phase routing, a developer switch gate, discovery caveats, validator/test coverage, and documentation.
- Excluded: Automatic model switching or delegation, a live cross-vendor model catalog, an installer/synchronizer, and merging the predecessor branch.
- Acceptance criteria: The always-loaded trigger stays below budget; detailed routing is on demand; agents never guess identity or availability; tests and structural validation pass.

## Constraints and decisions

- Base/PR target: `main`, after `chore/flatten-kit-to-root`
- Role: chore
- Worktree: primary checkout; no concurrent agents on this work
- Owned paths: agent rules, policy documentation, validator/tests, and this branch's handoff records
- History: [model-routing-policy.history.md](model-routing-policy.history.md)
- Decisions: Define “optimal” as the least-cost route expected to meet risk and quality, including retries and handoff overhead. Require a switch only for a known, materially better available route; literal global optimality is unknowable and would cause repeated pauses.

## Risks or blockers

- Model identity and available choices are not exposed by every host; those fields must remain `unknown` rather than guessed.
- The predecessor flattening branch is committed but not merged into `main`.

## Next action

Developer review, then authorize a commit if desired. Merge the predecessor flattening branch first.

## Validation checkpoint

Passed on Windows 2026-08-13:

- `py -3 scripts\validate_handoffs.py --quiet`
- `py -3 -m unittest discover -s scripts -p 'test_*.py'` — 40 tests
- `git diff --check`

## Merge and cleanup

- Primary checkout: `H:\Desktop\ai_agent_guides`
- After merge: verify reachability, archive this handoff/history, update the index and global history, then remove the branch only with authorization.
