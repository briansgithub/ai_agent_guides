# Master Branch Handoff Protocol

Permanent handoffs live in `docs/handoffs/` and are committed with the repository. Read this file, `REPOSITORY.md`, `README.md`, and the current branch handoff/history before work.

## Non-negotiable rules

1. Any agent change to code, configuration, tests, git/branch/stash state, scope, or next actions requires an affected handoff/index update before finishing.
2. Active handoffs are replacement-style: remove stale content and completed checklists.
3. Per-branch histories and global `HISTORY.md` are append-only.
4. Every handoff/history Markdown file must be strictly below 42,000 characters.
5. Verify documentation against git; distinguish git-verified facts, owner-confirmed decisions, unknowns, and recommendations.
6. Keep documents tracked and include relevant updates with the commit/PR they describe.
7. Never delete branch documentation; archive it when the branch closes.

## Layout

- `<branch>.md`: current operating state (replace/update)
- `<branch>.history.md`: meaningful dated milestones (append-only)
- `archive/<branch>.md`: frozen closed handoff
- `archive/<branch>.history.md`: frozen milestone history
- `HISTORY.md`: append-only repository ledger with one close entry per branch
- `README.md`: active branch index and merge order
- `REPOSITORY.md`: repository-specific workflow, permissions, and checks
- `templates/`: starter branch/archive files

Paths mirror branch names:

- `main` → `main.md` + `main.history.md`
- `feature/example` → `feature/example.md` + `feature/example.history.md`

## Startup procedure

1. Read this file, `REPOSITORY.md`, `README.md`, current branch handoff, and adjacent history.
2. Inspect git status, branch tips/upstreams, merge base/diff against the configured default branch, stashes, and relevant tests.
3. Correct stale factual content.
4. Ask the owner only for intent git cannot prove.

Never assume visible uncommitted changes belong to the checked-out branch without confirmation.

## Active handoff structure

Keep these sections concise:

- **Identity:** branch, tip, upstream, parent/base, role, history link, verified date
- **Goal and scope:** purpose, included/excluded work, acceptance criteria
- **Changes since creation:** concise commits/behaviors; no pasted diffs
- **Current status:** clean/dirty state, base relationship, validation, blockers, stashes
- **Next actions:** immediate action first; remove completed items
- **Merge and cleanup:** PR base, readiness, predecessors, closure criteria

## Per-branch history

Create the adjacent history with every new branch. Append only meaningful milestones:

- branch creation/parent tip;
- meaningful commit or implementation milestone;
- approved scope/merge-order change;
- PR checks/results;
- rebase/base change;
- PR opened/merged/superseded/closed;
- stash disposition affecting recoverability.

Do not log routine reads/status checks or duplicate facts. Format:

```markdown
### YYYY-MM-DD — Short milestone
- Commit/base: `<sha>` (when applicable)
- Change: <one or two sentences>
- Validation/decision: <concise result>
```

Never rewrite older entries; add a correction entry. At ~30,000 characters, freeze the history as `<branch>.history/0001.md`, create a new `.history.md` linking it, and continue.

## End-of-change procedure

Before the final response:

1. Reinspect resulting git state.
2. Replace active handoff tip/status/tests/risks/next actions.
3. Append branch history only for a meaningful milestone.
4. Refresh `README.md` if inventory, tips, roles, or order changed.
5. Remove stale content from active handoffs only.
6. Run `python scripts/validate_handoffs.py`.
7. Keep every document below 42,000 characters.
8. Include documentation updates with the implementation commit.

If interrupted, record uncommitted changes, validation, and the first safe next action.

## PR checks and readiness

Before every PR, propose a focused automated/manual check list and ask the owner to approve, revise, or defer it. Record only the latest approved list/results.

Merge-ready means:

- scope/acceptance criteria complete;
- no unrelated WIP and clean tree;
- approved checks pass or explicit deferrals are recorded;
- no known high-severity regression;
- correct current base/predecessor;
- no secrets, generated data, or IDE-local state;
- handoff matches final tip and residual risks;
- PR explains purpose, behavior, validation, and dependencies.

“No known gaps” does not prove validation passed.

## After merge and pull

1. Check out the configured default branch and pull its remote.
2. Verify the feature tip/merge commit is reachable from the remote default branch.
3. Append the closure milestone to the branch history.
4. Move handoff/history to mirrored `archive/` paths.
5. Rewrite only the archived handoff to a frozen form: identity, final goal, what landed, validation, disposition, cleanup.
6. Append one close entry to global `HISTORY.md`.
7. Remove the branch from active `README.md`; update default-branch handoff/history.
8. Delete remote/local git branches after reachability verification.
9. Commit and push the archival cleanup.

Use `git branch -d`; use `-D` only after verified reachability and a known-safe refusal. Superseded intermediates follow the same archive/delete process once their commits are on the default branch.

## Stashes

Delete a superseded stash only after comparing it with reachable commits and proving all meaningful content is implemented. Record the conclusion first. Never delete a unique stash or wanted branch commit.

## New features

1. Update from the remote default branch.
2. Create one narrow `feature/`, `fix/`, or `chore/` branch.
3. Copy the branch handoff/history templates to mirrored paths; record creation/base.
4. Keep commits purpose-focused; exclude secrets, generated output, IDE state, and unrelated formatting.
5. Avoid stacks unless intentional and documented.
6. Ask for PR checks, validate, merge promptly, then complete archival.

## Automated validation

`python scripts/validate_handoffs.py` checks required files, size limits, relative links, active/index pairs, archive pairs, and append-only history prefixes when a base ref is available. CI runs it through `.github/workflows/handoff-validation.yml`.

## Prompt for implementation agents

> Read `AGENTS.md`, `docs/handoffs/MASTER_HANDOFF.md`, `REPOSITORY.md`, `README.md`, and the current branch handoff/history. Verify against git. Implement the immediate next action. Before every PR, propose checks for owner approval. Before finishing, refresh active handoffs/index, append only meaningful history, run the validator, and record results. After merge/pull, archive branch documentation, append global HISTORY, and delete reachable merged branches. Never delete branch documentation or exceed 42,000 characters per file.

