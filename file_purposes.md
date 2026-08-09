# File purposes

What each file in this repository is for. This repository distributes reusable,
vendor-neutral guidance kits; it does not itself install one.

## Repository root

| Path | Purpose |
|---|---|
| `README.md` | Index of the available kits and how to install one. |
| `file_purposes.md` | This file. |
| `.gitignore` | Keeps Python bytecode and check artifacts out of the tree. |

## `git-handoff-system/` — the portable kit

Copy this directory's **contents** into a target repository root; see its
[README](git-handoff-system/README.md) for the install sequence.

### Agent entry points

| Path | Purpose |
|---|---|
| `AGENTS.md` | **Authoritative** agent defaults: work, context, verification, and handoff rules. The only always-loaded file and the only required entry point. Capped at 5,000 characters. |
| `CLAUDE.md` | Shim pointing Claude at `AGENTS.md`. |
| `GEMINI.md` | Shim pointing Gemini/Google agents at `AGENTS.md`. |
| `.cursor/rules/handoff-maintenance.mdc` | Always-applied Cursor rule pointing at `AGENTS.md`. |
| `.github/copilot-instructions.md` | Shim pointing Copilot at `AGENTS.md`. |

Shims are optional and interchangeable — delete any you do not use, and add one
for another tool the same way. Each is capped at 600 characters and must point
at `AGENTS.md` rather than restate the protocol, so the rules have one source.

### On-demand policy documents

Routed to from `AGENTS.md` only when relevant; never startup reading.

| Path | Purpose |
|---|---|
| `docs/handoffs/MASTER_HANDOFF.md` | Lifecycle reference: startup, context budget, handoff contents, per-branch history, close/archive sequence, verification and PR readiness, stash recovery. |
| `docs/handoffs/REPOSITORY.md` | Repository-specific configuration: default branch, merge strategy, agent permissions, standing check profile, toolchain notes. The file installers customize first. |
| `docs/handoffs/MULTI_AGENT.md` | Git worktree isolation for genuinely concurrent agents. Toolchain-neutral. |

### Branch records

| Path | Purpose |
|---|---|
| `docs/handoffs/README.md` | Active branch index, merge order, and the index row format the validator expects. |
| `docs/handoffs/main.md` | Replacement-style handoff for the default branch. Rename if the default branch is not `main`. |
| `docs/handoffs/main.history.md` | Append-only milestones for the default branch. |
| `docs/handoffs/HISTORY.md` | Global close ledger — one entry per closed branch. Rolls over into `HISTORY/<year>.md`. |
| `docs/handoffs/archive/README.md` | How closed branch records are frozen and where they mirror to. |

Active handoffs are replacement-style; histories are append-only and enforced as
such against a base ref. Per-branch histories roll over into numbered segments
(`<branch>.history.2.md`).

### Templates

| Path | Purpose |
|---|---|
| `docs/handoffs/templates/BRANCH_HANDOFF.md` | Starter for a new active branch handoff. Carries a filled worked example. |
| `docs/handoffs/templates/BRANCH_HISTORY.md` | Starter for an append-only branch history. Carries worked examples of entries that are and are not worth appending. |
| `docs/handoffs/templates/ARCHIVED_HANDOFF.md` | Frozen post-merge form. |

### Tooling

| Path | Purpose |
|---|---|
| `scripts/validate_handoffs.py` | Structural validator: required files, size budgets, links, active/archive pairs, append-only histories. `--installed` also rejects unfilled template placeholders. |
| `scripts/context_probe.py` | Local size and token-risk preflight for generated or unfamiliar artifacts, plus bounded recency-first retrieval (`tail`, `chunk`). Estimates are calibrated against measured tokenizer output. |
| `scripts/compact_check.py` | Runs one check while keeping full logs off the AI context path: bounded failure tail to the agent, complete log on disk. `--shell` for pipelines and wrapper scripts. |
| `scripts/test_agent_tools.py` | Standard-library tests for all three tools, including a regression case per fixed defect. |

If `python` is not on PATH, use `python3` (most Linux/macOS) or `py` (Windows).

### Distribution and CI

| Path | Purpose |
|---|---|
| `VERSION` | Installed kit version. Record it in the target repository's handoff history so an upgrade knows what it replaces. |
| `CHANGELOG.md` | What changed between versions and what an upgrade must reconcile. |
| `.gitignore` | Merged into the target repository so tool bytecode is not committed. |
| `.github/workflows/handoff-validation.yml` | Runs the tool tests and the structural validator on Linux and Windows for pull requests and pushes to `main`. |
