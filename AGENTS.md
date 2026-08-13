# Agent Defaults

Use the least context, planning, and validation that completes the task reliably.

These defaults apply everywhere. Rules marked *if present* use optional kit files; without them, keep the principle and skip the mechanism. On conflict, follow narrower repository-scoped instructions and name what you set aside.

## Work

- Start with requested files and `git status --short --branch`; preserve unrelated and uncommitted work.
- Do not formally plan clear, localized work. Plan only when requested or when ambiguity, risk, dependent phases, cross-system work, or session continuity warrants it; reuse plans until the approach changes.
- When planning, report the runtime model or `unknown`, tag phases with least-cost capable routes, and follow `docs/handoffs/MODEL_ROUTING.md` *if present*. Ask for a switch when a known alternative is materially better; never guess identity, availability, or price.
- *If present:* follow `docs/handoffs/GIT_WORKFLOW.md`. Use a narrow task branch and autonomously commit coherent, validated checkpoints containing only in-scope files. Require explicit authorization for deletion, discarded work, or history/ancestry changes beyond a normal commit.
- Make the narrowest change that satisfies the request; name deliberate exclusions.

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
- *If `docs/handoffs/` is present,* choose the lightest coordination tier: **routine** localized/single-session work uses Git only; **durable** multi-session, material, risky, or decision-heavy work adds a branch handoff/history; **concurrent** work adds those records plus a separate sibling worktree per agent.
- Route on demand: `MASTER_HANDOFF.md` for durable lifecycle/recovery, `REPOSITORY.md` for standing permissions and check profiles, and `MULTI_AGENT.md` only for actual concurrency. Read only the active record and newest history needed.
- For durable/concurrent work, update the handoff once at the end only when objective, decisions, blockers, risks, validation, or next action changed; append history only for milestones. Routine/read-only/no-op work creates none.
- Close durable work from the primary checkout: verify reachability and archive its records, then require authorization not already granted in `REPOSITORY.md` before removing worktrees or deleting branches. Stop on dirty or unmerged work; never force-delete or overwrite another agent's work.
- *If present:* after structural changes run `python scripts/validate_handoffs.py --quiet`; add `--require-current-handoff` for durable or concurrent branches. Never delete branch documentation.

If `python` is missing, use `python3` or `py`.
