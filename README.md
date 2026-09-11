# Portable Git Handoff System

Reusable branch-handoff framework for agents that honor `AGENTS.md`, with small pointer shims for many common rule-file conventions.

Version: see [VERSION](VERSION) and [CHANGELOG.md](CHANGELOG.md). Record the installed version in the repository's handoff history so an upgrade can tell what it is replacing.

## What this repository is

**This repository *is* the kit, and it installs itself.** `AGENTS.md`, `docs/handoffs/`, `scripts/`, and `.github/workflows/` here are live, not samples — the validator validates *this* repository and the tests run against it.

When this directory is the workspace root and a client honors one of the registered conventions, `AGENTS.md` is authoritative and each tool-specific file is only a short pointer to it. No file layout can force an IDE to load rules it does not support.

To use it elsewhere, see [Install in another repository](#install-in-another-repository).

## Agent entry points

`AGENTS.md` is the single source of the defaults. Everything else is a pointer to it, because tool-specific files take precedence over `AGENTS.md` in clients that read both — a pointer redirects to the one source instead of letting a stale copy win. The validator caps `AGENTS.md` at 5,000 characters and every shim at 600, and a test asserts each shim actually points at `AGENTS.md`.

| Path | Tool |
|---|---|
| `AGENTS.md` | **authoritative** — Codex, OpenCode, Zed, Cursor, VS Code chat, Grok CLI (xAI) |
| `CLAUDE.md` | Claude Code, VS Code chat |
| `GEMINI.md` | Gemini CLI, Antigravity, Gemini Code Assist, Android Studio |
| `.cursor/rules/handoff-maintenance.mdc` | Cursor, including Grok in Cursor |
| `.grok/rules/agents.md` | Grok CLI (xAI) |
| `.grok/GROK.md` | community grok-cli |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.clinerules` | Cline |
| `.windsurfrules` | Windsurf |
| `.rules` | Zed |
| `CONVENTIONS.md` | Aider |
| `.junie/guidelines.md` | JetBrains Junie |
| `.amazonq/rules/agents.md` | Amazon Q Developer |
| `.roo/rules/agents.md` | Roo Code |
| `best_practices.md` | Qodo |
| `QWEN.md`, `AGENT.md`, `.trae/rules/project_rules.md`, `.idx/airules.md`, `.kilocode/rules/agents.md` | Qwen, Amp, Trae, Firebase Studio, Kilo |

Targets may omit unused shims—only `AGENTS.md` is required. Removing an existing shim requires explicit authorization. Adding support for another tool is one short file pointing at `AGENTS.md`, plus its path in `ENTRYPOINT_LIMITS`.

These files are discovered relative to the workspace a tool opens. An agent working in another repository will not normally scan this unrelated directory automatically. Either install the kit into that repository's root or configure the tool's global/user instructions to read this root `AGENTS.md`. Verify each client with a small rule-following smoke task; unsupported or disabled conventions remain inert.

Record real discovery results in [PLATFORM_COMPATIBILITY.md](docs/handoffs/PLATFORM_COMPATIBILITY.md). Its live-client matrix distinguishes a registered filename from a tested integration without adding startup context.

## Install in another repository

Copy everything **except**:

```text
.git/                          this repository's own history
.claude/                       agent-local permission overrides
file_purposes.md               documentation about this repository
docs/handoffs/<branch>/**      this repository's live branch records
docs/handoffs/archive/**       except archive/README.md
```

Then, in the target:

1. Rename `docs/handoffs/main.md` and `main.history.md` to the target's default branch, and update the index row in `docs/handoffs/README.md` to match. Skipping this fails validation immediately: the checked-out branch must appear in the index.
2. Reduce the index in `docs/handoffs/README.md` to that one row, and empty the entries under `docs/handoffs/HISTORY.md`.
3. Edit `docs/handoffs/REPOSITORY.md` — default branch, check profile, permissions, toolchain notes, and optional standing model routes.
4. Omit unused per-tool shims from a new install; obtain explicit authorization before removing one from an existing repository.
5. Run `python scripts/validate_handoffs.py --installed`. It will report the placeholders in the renamed default-branch records; filling them is step 6.
6. Fill those fields and commit the complete setup.

Copying the excluded paths produces an install that **passes validation while carrying this repository's branch history as its own** — the copied index and copied records are internally consistent, so nothing detects it. That is why the exclusion list matters more than the copy step.

`file_purposes.md` carries a `Ships` column marking every file `yes`, `no`, or `seeded`.

If `python` is not on PATH, use `python3` (most Linux/macOS) or `py` (Windows).

The default workflow avoids formal plans for straightforward changes, loads handoff/history documents only when relevant, and uses risk-proportional verification. Coordination has three tiers: routine localized work uses Git only; durable material or multi-session work adds branch records; concurrent work adds one sibling worktree per agent. Repository-wide analysis or unusually expensive validation should be confirmed with the owner when it materially expands an otherwise bounded request.

Formal plans use [MODEL_ROUTING.md](docs/handoffs/MODEL_ROUTING.md): the agent reports only runtime-known identity, tags each phase with the least-cost capable model route, and pauses before a phase when a known available alternative is materially better. Exact model catalogs stay outside the evergreen defaults because names, access, and prices change.

Git work follows [GIT_WORKFLOW.md](docs/handoffs/GIT_WORKFLOW.md). Agents create narrow task branches and automatically commit coherent, validated checkpoints containing only their in-scope files. Normal commits and branch creation are standing-authorized; other mutations require current authorization or an exact standing grant recorded in [REPOSITORY.md](docs/handoffs/REPOSITORY.md). Ambiguous or example grants authorize nothing.

“Clean up” starts a candidate inventory. The agent identifies disposable debug/research/testing artifacts, explains their purpose, and requests confirmation for exact targets. Regression and backward-compatibility coverage is retained. Confirmed deletions receive a durable purpose/disposition note and a focused cleanup commit.

## Context and output controls

Size-probe candidate context locally without emitting file contents:

```bash
python scripts/context_probe.py scan build/reports vendor --recursive --top 20
```

Reach for this before **generated or unfamiliar** artifacts — logs, build output, data dumps, vendored trees. Ordinary source and documentation you already have a reason to open do not need a preflight; the probe costs a round trip and a targeted read is cheaper.

Estimates are calibrated against measured tokenizer output (ASCII text runs about 4.5 characters per token; CJK about 1.1) and reported as a range, with routing done on the midpoint. Low-risk files may normally be read in full; medium/high files should be searched or chunked first; extreme-risk full reads require confirmation unless exhaustive review is already in scope. The `TOTAL` line bands the whole scan on a larger scale, because a batch competes for the context window rather than one file's budget.

Read the recent end of an append-only log or history, then page backward only if needed:

```bash
python scripts/context_probe.py tail path/to/history.md --lines 120
python scripts/context_probe.py chunk path/to/history.md --end-line 500 --lines 120
```

The tool preserves normal line order inside each chunk. Do not use tail-first reading for source/configuration files whose earlier structure controls interpretation.

Keep noisy test/build output out of AI context while retaining full failure logs locally:

```bash
python scripts/compact_check.py --name unit -- pytest -q --tb=short --maxfail=1
python scripts/compact_check.py --name build --quiet --shell -- "./gradlew build"
```

Commands run without a shell by default, so argv is passed through untouched. Add `--shell` for pipelines, shell builtins, and wrapper scripts such as `./gradlew` or `gradlew.bat`; with `--shell` the whole command is one string and you own the quoting inside it.

Successful logs are deleted by default; failure logs go to the system temporary directory and only their bounded tail is printed. Use `--artifact-dir` or `--keep-success-log` when persistent artifacts are needed. A timeout kills the whole process tree, so build daemons are not orphaned, and old failure logs are pruned to the most recent 20 per directory.

## Tests

```bash
python -m unittest discover -s scripts -p "test_*.py"
```

Standard library only — an installing repository does not inherit a test dependency. CI runs these plus the structural validator on Linux and Windows.

The default validator allows routine branches without handoff records. Durable and concurrent branches create the two records from `docs/handoffs/templates/`, add the active-index row, and validate with `--require-current-handoff`. Installed repositories also use `--installed`; the flags may be combined.

For agents that are actually working concurrently, follow `docs/handoffs/MULTI_AGENT.md`: one Git worktree (folder + branch) per agent. Record any toolchain-specific worktree steps — files to copy, one-project-per-worktree IDEs — in `docs/handoffs/REPOSITORY.md`.

Do not copy archived branch data from another repository. Each repository builds its own active handoffs, per-branch histories, and global close ledger.

