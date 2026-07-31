# Repository Handoff Configuration

Customize this file during installation. It defines standing repository choices so agents do not repeatedly ask for the same planning or validation decisions.

## Git workflow

- Default branch: `main` (change if different)
- Shared remote: `origin` (change if different)
- Branch names: `feature/<purpose>`, `fix/<purpose>`, `chore/<purpose>`
- Merge strategy: merge commit (`--no-ff`) by default; change deliberately if needed
- Direct feature commits to default branch: prohibited
- Agent permissions: require explicit owner authorization for commit, push, PR, merge, stash deletion, and branch deletion unless a documented standing instruction applies

## Execution defaults

- Formal implementation plan: not required for routine, localized, or clearly specified work, including ordinary Android Studio prompts
- Use a plan when requested or when work is ambiguous, high-risk, multi-phase, dependency-ordered, cross-system, or likely to span sessions
- Reuse an existing plan; update it only when the approach materially changes
- Context strategy: inspect relevant files first and expand only when evidence or risk requires it
- Context preflight: batch-scan unknown or potentially large candidates with `python scripts/context_probe.py scan <paths>` before emitting contents
- Append-only records: search first when possible; otherwise retrieve recent log/history chunks and page backward only as needed
- Token-heavy expansion: ask the owner before optional extreme-risk full reads, repository-wide analysis, exhaustive log/history review, broad research, or full validation that materially expands cost and was not explicitly requested
- Closed-loop limit: at most two automatic diagnose/fix/retest cycles for the same failure before asking to expand

## Standing validation profile

Agents may run the configured baseline without asking for approval before every PR. Customize commands during installation:

- Handoff structure: `python scripts/validate_handoffs.py`
- Build: `<command or not configured>`
- Unit tests: `<command or not configured>`
- Lint/type checks: `<command or not configured>`
- Manual checks: `<platform/behavior or not configured>`

For ordinary changes, run only the checks relevant to the affected behavior. Use the full PR baseline for PR/release readiness or when risk triggers justify it. Ask the owner when checks are unusually expensive, require owner participation, are unavailable, or may be deferred. Record meaningful results and deferrals in the active handoff only when they matter to continuation or release readiness.

Wrap noisy commands with `python scripts/compact_check.py --name <label> -- <command>` so full failure logs remain local and successful output can be suppressed with `--quiet`.

## Multi-agent isolation

When agents are actually working concurrently:

1. Create a worktree and branch for each agent (`git worktree add -b <branch> <path> <default-branch>`).
2. Open that path as the agent workspace; never share one working directory across concurrent agents.
3. Keep durable handoff context on the branch that owns the work.
4. Prefer a new worktree over stashing to free another checkout.
5. For Android apps, open each worktree as its own Android Studio project and copy required gitignored machine files such as `local.properties`; see [MULTI_AGENT.md](MULTI_AGENT.md).

If a stash is unavoidable, use `wip <exact-branch-name>: <reason>`, note it in the owning handoff when recovery depends on it, and apply or drop it only on the named branch after verifying disposition.

## Handoff locations

- Active index: `docs/handoffs/README.md`
- Active handoff/history: mirrored branch path under `docs/handoffs/`
- Archive: `docs/handoffs/archive/`
- Global close ledger: `docs/handoffs/HISTORY.md`
- Templates: `docs/handoffs/templates/`
- Parallel-agent procedure: `docs/handoffs/MULTI_AGENT.md`
