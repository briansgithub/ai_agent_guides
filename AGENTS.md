# Agent Defaults

Use the least context, planning, and validation that completes the task reliably.

These defaults apply everywhere. Rules marked *if present* use optional kit files; without them, keep the principle and skip the mechanism. On conflict, follow narrower repository-scoped instructions and name what you set aside.

## Work

- Start from the request and the files it names. Run `git status --short --branch` before editing.
- Preserve unrelated changes. Never assume uncommitted work is disposable.
- Do not write a formal plan for clear, localized work. Plan when the task is ambiguous, high-risk, multi-phase, dependency-ordered, cross-system, or spans sessions.
- Reuse an existing plan. Update it only when the approach changes materially.
- When planning, report the runtime provider/model or `unknown`, tag each phase with its least-cost capable route, and follow `docs/handoffs/MODEL_ROUTING.md` *if present*. Ask the developer to switch before a phase when a known alternative is materially better; never guess identity, availability, or price.
- Make the narrowest change that satisfies the request. Do not widen scope; say what you deliberately left out.

## Context

- Search before reading. Locate with grep/glob, then read the lines that matter. Read a file whole when its structure controls interpretation.
- Batch independent reads, searches, and commands into one step instead of one per turn.
- Do not re-read a file you just wrote. Do not paste file contents back to the user; cite `path:line`.
- Run `git diff --stat` before `git diff`, and scope with `--` pathspecs.
- Probe before loading generated or unfamiliar artifacts — logs, build output, data dumps, vendored trees. *If present:* `python scripts/context_probe.py scan <paths>`. Source and documentation you already have reason to open do not need a probe.
- Risk bands, applied to each file and to the batch `TOTAL`: **low** read fully; **medium** search or chunk; **high** give a task reason for a full read; **extreme** ask first, unless exhaustive review is already the task.
- For append-only logs and histories, search known identifiers first, then read the recent end, then page backward only as needed. Never read source tail-first.
- Ask before repository-wide inspection, exhaustive history or log review, or other major context expansion. Say why it helps and name the bounded alternative.

## Verification

- Run the smallest check that covers the change. Broaden it for failures, shared interfaces, dependencies, build configuration, schemas, migrations, security, concurrency, persistence, PRs, and releases.
- Keep noisy output off the context path. *If present:* `python scripts/compact_check.py --name <label> -- <command>`; add `--quiet` for silent success, `--shell` for pipelines or wrapper scripts.
- Report the exact command and its result. Never state or imply that an unrun check passed.
- Do not rerun a passing check when nothing relevant changed.
- Allow at most two diagnose/fix/retest cycles for the same failure, then summarize and ask before expanding.

## Durable context and handoffs

- Record something only if an agent resuming this work would act differently without it. That is the test for "durable" and "meaningful" throughout these rules.
- Keep durable context where the repository already keeps it. Get transient facts — tips, dirty state, ahead/behind — from Git instead of copying them into prose.
- *If `docs/handoffs/` is present:* it is that location. Read the active handoff only when resuming or inheriting work, or when scope is unclear, and read only the newest history you need. Route on demand — `MASTER_HANDOFF.md` for lifecycle and recovery, `REPOSITORY.md` for policy and check profiles, `MULTI_AGENT.md` only when agents are actually concurrent.
- *If present:* update the handoff once, at the end, and only when objective, scope, decisions, blockers, risks, validation, or next action changed. Skip it for read-only, routine, and no-op work. Update the index only for branch inventory, role, or merge order; append history only for milestones.
- Concurrent agents need separate worktrees: sibling folders beside the primary checkout, never nested. Each is a normal branch; `push` publishes it, only an authorized merge or PR lands it.
- Close work from the primary checkout: verify the merge is reachable, archive the handoff, remove the sibling worktree, then `git branch -d`. Delete a remote branch only with authorization. Stop on dirty or unmerged work; never force-delete or overwrite another agent's work.
- *If present:* run `python scripts/validate_handoffs.py --quiet` after structural handoff changes. Never delete branch documentation.

If `python` is missing, use `python3` or `py`.
