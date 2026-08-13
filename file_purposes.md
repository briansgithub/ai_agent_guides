# File purposes

What each file in this repository is for.

**This repository *is* the kit.** These files are live here — the validator validates
this repository and the tests run against it — and they are also what gets copied into
an installing repository.

The `Ships` column says what happens on install:

- **yes** — copy verbatim.
- **seeded** — copy, then replace with the target's own content.
- **no** — do not copy. Copying these produces an install that *passes validation
  while carrying this repository's history as its own*, which nothing detects.

## Agent entry points

`AGENTS.md` is authoritative; every other file here is a short pointer to it, never a
copy of the rules. Tool-specific files take precedence over `AGENTS.md` in clients that
read both, so a pointer redirects to the single source instead of letting a stale copy
win. Each is capped at 600 characters, and a test asserts it points at `AGENTS.md`.

| Path | Tool | Ships |
|---|---|---|
| `AGENTS.md` | **Authoritative** agent defaults. Codex, OpenCode, Zed, Cursor, VS Code chat. The only required entry point. | yes |
| `CLAUDE.md` | Claude Code, VS Code chat | yes |
| `GEMINI.md` | Gemini CLI, Antigravity, Gemini Code Assist, Android Studio | yes |
| `.cursor/rules/handoff-maintenance.mdc` | Cursor | yes |
| `.github/copilot-instructions.md` | GitHub Copilot | yes |
| `.clinerules` | Cline | yes |
| `.windsurfrules` | Windsurf | yes |
| `.rules` | Zed | yes |
| `CONVENTIONS.md` | Aider | yes |
| `.junie/guidelines.md` | JetBrains Junie | yes |
| `.amazonq/rules/agents.md` | Amazon Q Developer | yes |
| `.roo/rules/agents.md` | Roo Code | yes |
| `best_practices.md` | Qodo | yes |
| `QWEN.md`, `AGENT.md`, `.trae/rules/project_rules.md`, `.idx/airules.md`, `.kilocode/rules/agents.md` | Qwen, Amp, Trae, Firebase Studio, Kilo | yes |

Targets may omit unused shims; deleting one from an existing repository requires explicit authorization.

## On-demand policy documents

Routed to from `AGENTS.md` only when relevant; never startup reading.

| Path | Purpose | Ships |
|---|---|---|
| `docs/handoffs/MASTER_HANDOFF.md` | Compact lifecycle reference for choosing routine/durable/concurrent tiers and managing durable records through archive/recovery. | yes |
| `docs/handoffs/REPOSITORY.md` | Repository-specific configuration: workflow tier defaults, exact standing permission grants, check profile, and toolchain notes. Installers customize this first. | yes |
| `docs/handoffs/MULTI_AGENT.md` | Git worktree isolation for genuinely concurrent agents. Toolchain-neutral. | yes |
| `docs/handoffs/MODEL_ROUTING.md` | Formal-plan model routing: runtime identity, capability classes, total-token optimization, and the developer switch gate. | yes |
| `docs/handoffs/GIT_WORKFLOW.md` | Default Git practices: narrow branches, exact staging, autonomous checkpoint commits, confirmed temporary-artifact cleanup, regression-test retention, and destructive-action gates. | yes |
| `docs/handoffs/PLATFORM_COMPATIBILITY.md` | On-demand live-client smoke matrix separating registered rule-file conventions from verified discovery behavior. | yes |

## Branch records

Active handoffs are replacement-style; histories are append-only and enforced as such
against a base ref. Per-branch histories roll over into numbered segments
(`<branch>.history.2.md`); the global ledger rolls into `HISTORY/<year>.md`.

| Path | Purpose | Ships |
|---|---|---|
| `docs/handoffs/README.md` | Active branch index, merge order, and the row format the validator expects. | seeded — reduce to the target's default-branch row |
| `docs/handoffs/main.md` | Replacement-style handoff for the default branch. Left unfilled here on purpose: it doubles as the skeleton an installer renames and fills. | yes — rename to the target's default branch |
| `docs/handoffs/main.history.md` | Append-only milestones for the default branch. Same skeleton role. | yes — rename to match |
| `docs/handoffs/HISTORY.md` | Global close ledger, one entry per closed branch. | seeded — keep the format, empty the entries |
| `docs/handoffs/archive/README.md` | How closed branch records are frozen and where they mirror to. | yes |
| `docs/handoffs/archive/**` (records) | Frozen records for this repository's closed branches. | **no** |
| `docs/handoffs/<branch>/**` | This repository's live branch records, e.g. `chore/`. | **no** |

## Templates

| Path | Purpose | Ships |
|---|---|---|
| `docs/handoffs/templates/BRANCH_HANDOFF.md` | Starter for a new active branch handoff. Carries a filled worked example. | yes |
| `docs/handoffs/templates/BRANCH_HISTORY.md` | Starter for an append-only branch history. Carries worked examples of entries that are and are not worth appending. | yes |
| `docs/handoffs/templates/ARCHIVED_HANDOFF.md` | Frozen post-merge form. | yes |

## Tooling

If `python` is not on PATH, use `python3` (most Linux/macOS) or `py` (Windows).

| Path | Purpose | Ships |
|---|---|---|
| `scripts/validate_handoffs.py` | Structural validator: required files, size budgets, links, active/archive pairs, and append-only histories. `--installed` rejects live placeholders; `--require-current-handoff` enforces durable/concurrent branch records. | yes |
| `scripts/context_probe.py` | Size and token-risk preflight for generated or unfamiliar artifacts, plus bounded recency-first retrieval (`tail`, `chunk`). Estimates calibrated against measured tokenizer output. | yes |
| `scripts/compact_check.py` | Runs one check while keeping full logs off the AI context path: bounded failure tail to the agent, complete log on disk. `--shell` for pipelines and wrapper scripts. | yes |
| `scripts/test_agent_tools.py` | Standard-library tests for all three tools, with a regression case per fixed defect. | yes |

## Distribution and repository metadata

| Path | Purpose | Ships |
|---|---|---|
| `README.md` | What this repository is, the agent entry-point matrix, install instructions, tool usage. | yes |
| `VERSION` | Installed kit version. Record it in the target's handoff history so an upgrade knows what it replaces. | yes |
| `CHANGELOG.md` | What changed between versions and what an upgrade must reconcile. | yes |
| `.gitignore` | Keeps tool bytecode and agent-local settings out of the tree. Merge into any existing one. | yes |
| `.github/workflows/handoff-validation.yml` | Runs the tool tests and the structural validator on Linux and Windows. | yes |
| `file_purposes.md` | This file — documentation about this repository. | **no** |
| `.claude/settings.local.json` | Agent-local permission overrides. Untracked and gitignored. | **no** |
