# Branch: `chore/flatten-kit-to-root`

## Objective

- Goal: Make this repository's agent rules discoverable by any agent or IDE pointed at its root, without per-tool configuration.
- Included: Flattening the kit to the repository root, the branch records this repository now needs to validate itself, reconciling the documentation the flatten invalidates, and a per-tool shim for every known convention.
- Excluded: An install script. The install story is documentation-only for now; revisit if the kit is ever installed somewhere real. Also excluded: resolving the conflicting rule files that live above this repository on the Desktop.
- Acceptance criteria: `validate_handoffs.py` and the tool test suite both pass from the repository root; `AGENTS.md` and every shim sit at depth 0; `.github/workflows/` sits where GitHub would execute it.

## Constraints and decisions

- Base/PR target: `main`
- Role: chore
- Worktree: primary checkout; no concurrent agents on this work
- Owned paths: the whole repository. This branch restructures it.
- History: [flatten-kit-to-root.history.md](flatten-kit-to-root.history.md)
- Decisions:
  - Four global agent configs already pointed at this repository's root and named `AGENTS.md` as the entry point. Flattening repairs a pointer they depend on rather than introducing a new convention.
  - `master` renamed to `main`. The kit's docs, templates, and CI trigger all assume `main`, and no remote existed, so the rename was free. The alternative was six coordinated edits and a permanent fork between this repository and the artifact it ships.
  - This repository does not adopt `--installed`. `main.md` and `main.history.md` keep their placeholders deliberately so they stay copyable skeletons; that is what the kit's own documentation already specifies.
  - Shims are pointers to `AGENTS.md`, never copies of the rules. Tool-specific files take precedence over `AGENTS.md` in clients that read both, so a pointer redirects to the single source instead of letting a stale duplicate win.
  - Extended shims land in their own commit so they can be reverted without touching the flatten.

## Risks or blockers

None blocking. Two accepted consequences:

- The tool test suite is now coupled to live repository state. `test_kit_validates_clean` fails on any branch without handoff records, including a branch opened for a one-line fix. This is intended dogfooding, documented in the README rather than worked around.
- CI is now in a location GitHub would execute, but no remote is configured, so nothing runs yet. Flattening was necessary, not sufficient.

## Next action

None; scope is complete. Merge to `main` with `--no-ff`, and archive this handoff and its history in the same merge so `main` does not inherit a permanently required index row.

## Validation checkpoint

`python scripts/validate_handoffs.py` and `python -m unittest discover -s scripts -p "test_*.py"` both pass from the repository root. Rename history verified with `git log --follow`.

## Merge and cleanup

- Primary checkout: `H:\Desktop\ai_agent_guides`
- After merge: archive this handoff and history together to `docs/handoffs/archive/chore/`, remove the index row, and append one close entry to `HISTORY.md`. Moving only one of the pair fails `validate_archive_pairs`.
