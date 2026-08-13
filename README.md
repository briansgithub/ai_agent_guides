# Portable Git Handoff System

Reusable branch-handoff framework for any agent that honors `AGENTS.md`, with pointer shims for every other rule-file convention in common use.

Version: see [VERSION](VERSION) and [CHANGELOG.md](CHANGELOG.md). Record the installed version in the repository's handoff history so an upgrade can tell what it is replacing.

## What this repository is

**This repository *is* the kit, and it installs itself.** `AGENTS.md`, `docs/handoffs/`, `scripts/`, and `.github/workflows/` here are live, not samples — the validator validates *this* repository and the tests run against it.

Agents and IDEs pointed at this directory need no configuration: `AGENTS.md` is authoritative, and every per-tool file at the root is a short pointer to it.

To use it elsewhere, see [Install in another repository](#install-in-another-repository).

## Agent entry points

`AGENTS.md` is the single source of the defaults. Everything else is a pointer to it, because tool-specific files take precedence over `AGENTS.md` in clients that read both — a pointer redirects to the one source instead of letting a stale copy win. The validator caps `AGENTS.md` at 5,000 characters and every shim at 600, and a test asserts each shim actually points at `AGENTS.md`.

| Path | Tool |
|---|---|
| `AGENTS.md` | **authoritative** — Codex, OpenCode, Zed, Cursor, VS Code chat |
| `CLAUDE.md` | Claude Code, VS Code chat |
| `GEMINI.md` | Gemini CLI, Antigravity, Gemini Code Assist, Android Studio |
| `.cursor/rules/handoff-maintenance.mdc` | Cursor |
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

Delete any you do not use — only `AGENTS.md` is required. Adding support for another tool is one short file pointing at `AGENTS.md`, plus its path in `ENTRYPOINT_LIMITS`.

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
3. Edit `docs/handoffs/REPOSITORY.md` — default branch, check profile, permissions, toolchain notes.
4. Delete any per-tool shim the target does not use.
5. Run `python scripts/validate_handoffs.py --installed`. It will report the placeholders in the renamed default-branch records; filling them is step 6.
6. Fill those fields and commit the complete setup.

Copying the excluded paths produces an install that **passes validation while carrying this repository's branch history as its own** — the copied index and copied records are internally consistent, so nothing detects it. That is why the exclusion list matters more than the copy step.

`file_purposes.md` carries a `Ships` column marking every file `yes`, `no`, or `seeded`.

If `python` is not on PATH, use `python3` (most Linux/macOS) or `py` (Windows).

The default workflow avoids formal plans for straightforward changes, loads handoff/history documents only when relevant, and uses risk-proportional verification. Repository-wide analysis or unusually expensive validation should be confirmed with the owner when it materially expands an otherwise bounded request.

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

The end-to-end test validates *this* repository, so a new branch needs its handoff records before the suite passes — even a branch opened for a one-line fix. That is the kit applying to itself; create the two records from `docs/handoffs/templates/` as `MASTER_HANDOFF.md`'s New branches procedure already requires.

For agents that are actually working concurrently, follow `docs/handoffs/MULTI_AGENT.md`: one Git worktree (folder + branch) per agent. Record any toolchain-specific worktree steps — files to copy, one-project-per-worktree IDEs — in `docs/handoffs/REPOSITORY.md`.

Do not copy archived branch data from another repository. Each repository builds its own active handoffs, per-branch histories, and global close ledger.

