# Durable Handoff Lifecycle

Permanent handoffs live in `docs/handoffs/` and travel with their owning branch. This file controls when records exist and how they move through their lifecycle; it is not startup reading for routine work.

Use the specialized policies instead of restating them here:

- [GIT_WORKFLOW.md](GIT_WORKFLOW.md): branches, commits, permissions, cleanup, integration safety
- [REPOSITORY.md](REPOSITORY.md): repository-specific grants, check profile, toolchain choices
- [MULTI_AGENT.md](MULTI_AGENT.md): concurrent-agent worktrees and ownership
- [MODEL_ROUTING.md](MODEL_ROUTING.md): model choice only when a formal plan exists
- `AGENTS.md`: context and verification defaults

## Non-negotiable invariants

1. Preserve unrelated work; derive transient branch facts from Git.
2. Active handoffs are replacement-style. Per-branch histories and global `HISTORY.md` are append-only.
3. Never delete branch documentation; archive it when work closes.
4. Never run concurrent agents in one working directory.
5. Keep `AGENTS.md` below 5,000 characters, shims below 600, handoffs below 6,000, history segments below 12,000, and policy documents below 20,000. The validator enforces these limits.
6. Keep relevant durable records in the commit or PR they describe.

## Choose the coordination tier

Use the lightest tier that preserves reliable continuation:

| Tier | Use when | Required state |
|---|---|---|
| **Routine** | Localized, single-session work with no material decision, recovery, or coordination need | Git branch/commits only; no handoff, history, or index row |
| **Durable** | Material, risky, decision-heavy, multi-phase, or likely multi-session work | Mirrored branch handoff/history plus active-index row |
| **Concurrent** | Two or more agents are actively working in the repository | Durable records plus one sibling worktree per agent and explicit owned/no-go paths |

Escalate from routine to durable as soon as a lasting decision, blocker, risky partial state, or session boundary makes resumption context valuable. Creating records late is valid; record the current durable state rather than reconstructing routine narration. Concurrency always uses the concurrent tier.

Do not create handoff records merely because a task has a branch, an IDE opened, an agent made a plan, or a small change received a follow-up prompt.

## Durable branch startup

1. Start with concise Git status and confirm the intended base.
2. Create the mirrored handoff/history from `templates/` and add one index row.
3. Record objective, bounded scope, acceptance criteria, durable decisions, risks, and one next action.
4. For concurrent work, follow `MULTI_AGENT.md` before edits and record the sibling worktree plus owned/no-go paths.
5. Run `python scripts/validate_handoffs.py --quiet --require-current-handoff` after the structural change.

When resuming or inheriting durable work, read the active handoff and only the newest relevant history. Verify only claims that affect the next action. Inspect tips, upstreams, merge bases, stashes, or longer history only when the action depends on them.

## Active record contents

Keep only information that would change a resuming agent's next action:

- objective, scope, non-goals, and acceptance criteria;
- owner decisions and constraints;
- unresolved risks or blockers;
- one immediate safe next action;
- the latest meaningful validation checkpoint or relevant deferral;
- worktree and path ownership when concurrent.

Do not mirror current SHA, clean/dirty state, upstream tracking, ahead/behind counts, routine reads, or complete stash inventories. Include an identifier only when it is essential to recovery.

Update the active handoff once near the end of meaningful work, and only when its durable state changed. Update the index only for branch inventory, role, or merge order.

## Append-only history

Append a milestone only when omitting it would change future action, for example:

- branch creation and intended base;
- a material implementation or owner-decision checkpoint;
- approved scope or merge-order change;
- consequential validation, PR, rebase, recovery, or closure event;
- stash disposition needed for recovery.

Do not log every prompt, read, commit, status check, or passing test. Correct an old entry with a new entry; never rewrite it.

Before 12,000 characters, freeze the segment and continue with `<branch>.history.2.md`, then `.3.md`. Roll global closure history into `HISTORY/<year>.md`. Search by identifier first; otherwise read the recent end and move backward only as evidence requires.

## End of durable work

1. Inspect scoped diff and status once.
2. Apply the proportional verification and retry limits in `AGENTS.md`; use the standing profile in `REPOSITORY.md`.
3. Update the active handoff once if durable state changed and append history only for a milestone.
4. Run `python scripts/validate_handoffs.py --quiet --require-current-handoff` after structural record changes.
5. Commit coherent, in-scope checkpoints under `GIT_WORKFLOW.md`.

Routine work skips this section's record maintenance. If routine work becomes durable, escalate tiers before leaving material unfinished state.

## Merge readiness and closure

Merge-ready means the requested scope is complete, unrelated work is absent, applicable checks pass or deferrals are recorded, no known high-severity regression remains, the base is correct, and durable records describe residual risk.

After an authorized merge or PR landing, work from the primary checkout:

1. Verify the feature tip or merge commit is reachable from the remote default branch.
2. Append the closure milestone and move the handoff/history to mirrored `archive/` paths without rewriting them.
3. Freeze the archived handoff to landed behavior, validation, disposition, and remaining cleanup.
4. Append one global close entry and remove the active-index row.
5. Commit the archival documentation; push only with current authorization or a matching standing grant.
6. Remove worktrees or local/remote branches only with current authorization or a matching grant, after verifying no dirty, unique, or unmerged work remains.

Never force-remove a dirty worktree or force-delete an unverified branch. A pushed but unmerged branch remains preserved.

## Recovery and stashes

Prefer a dedicated worktree over stashing. If a stash is unavoidable, name it `wip <exact-branch-name>: <reason>` and mention it in the owning durable handoff only when recovery depends on it.

Before applying, verify the named branch and compare disposition. `pop` deletes on success, so use it only with appropriate authorization; otherwise use `apply`. Drop a stash only after its meaningful content is reachable or explicitly abandoned. Never act on another branch's stash.

For conflict resolution, worktree ownership, and deletion gates, use `GIT_WORKFLOW.md` and `MULTI_AGENT.md` rather than inventing a recovery path.

## Validation

`python scripts/validate_handoffs.py` checks required files, budgets, links, indexed pairs, archives, and append-only history when a base ref is available. Add:

- `--installed` in an installed repository to reject unfilled live-record placeholders;
- `--require-current-handoff` for durable and concurrent branches;
- `--quiet` for silent success;
- `--verbose` only for worktree/tracking/stash diagnostics.

Routine branches intentionally pass without their own records. CI should use the repository's configured baseline; durable/concurrent branch preparation should use the stricter flag.
