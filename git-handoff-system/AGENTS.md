# Repository Agent Defaults

Use the smallest amount of context, planning, and validation that can complete the task reliably.

## Work and planning

- Start with the user's request and directly relevant files. Before editing, run `git status --short --branch`; inspect broader Git state only when it affects the task. Preserve unrelated user changes.
- Do not propose a formal plan for straightforward work, including routine Android Studio prompts, small fixes, localized refactors, documentation edits, and clear follow-ups.
- Plan only when requested or when work is ambiguous, high-risk, multi-phase, dependency-ordered, cross-system, or likely to span sessions. Reuse an existing plan and update it only when the approach materially changes.

## Context guardrails

- Before loading files of unknown or potentially large size, batch-probe them locally with `python scripts/context_probe.py scan <paths>`. The tool emits size and heuristic token risk without emitting file contents.
- Treat individual and aggregate `TOTAL` risk labels as defaults: **low** may be read fully; **medium** should be searched or chunked first; **high** needs a concrete reason for a full read; **extreme** requires user confirmation before a full read unless exhaustive review was explicitly requested or essential to an authorized high-risk operation.
- For append-only histories, logs, and reports, search for known terms first; otherwise read the newest end with `context_probe.py tail` and page backward with `chunk` only as needed. Keep each retrieved chunk in normal order so stack traces and chronology remain intact.
- Do not apply tail-first reading to source code, configuration, manifests, or documents whose earlier structure governs later content. Use symbols, search hits, or targeted line ranges instead.
- Ask before optional repository-wide inspection, exhaustive history/log analysis, broad research, or context expansion that materially exceeds a bounded approach. When asking, state the reason and cheaper alternative.

## Verification

- Run the smallest relevant check, broadening for failures, unclear impact, shared interfaces, dependencies, build configuration, schemas/migrations, security/authentication, concurrency, persistence, PRs, and releases.
- Run noisy checks through `python scripts/compact_check.py --name <label> -- <command>` when practical. Full output stays in a local failure log; successful output is one line or silent with `--quiet`.
- Automatically perform at most two diagnose/fix/retest cycles for the same failure. If it persists or testing must expand materially, summarize and ask before continuing unless broader validation was explicitly requested.
- Do not rerun successful checks unless relevant files changed. Never claim an unrun check passed. Prefer CI for an already-configured full matrix and inspect only failed steps unless more detail is necessary.

## Handoff routing and maintenance

- Read the current handoff only when resuming ongoing work, inheriting an unfamiliar branch, or when scope is unclear. Read history only for a needed past decision, using recency-first chunks.
- Consult only the relevant sections of `MASTER_HANDOFF.md` for lifecycle/recovery work and `REPOSITORY.md` when policy or check profiles matter. Consult the relevant platform/operation section of `MULTI_AGENT.md` only when agents are actually concurrent; concurrent agents require separate Git worktrees.
- Update an active handoff once before finishing only when durable context changed: objective, scope, decisions, blockers, risks, meaningful validation, or next action. Do not update it for read-only, routine, no-op, or context-neutral work.
- Update the index only when branch inventory, role, or merge order changes; append history only for meaningful milestones.
- Run `python scripts/validate_handoffs.py --quiet` once after structural handoff changes and as configured for PR checks. CI may provide it for ordinary content-only updates.

Follow `MASTER_HANDOFF.md` for destructive or branch-closing operations. Never delete branch documentation.
