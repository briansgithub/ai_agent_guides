# Portable Git Handoff System

Reusable branch-handoff framework for any agent that honors `AGENTS.md`, with shims for Claude, Gemini, Cursor, and Copilot.

Version: see [VERSION](VERSION) and [CHANGELOG.md](CHANGELOG.md). Record the installed version in the repository's handoff history so an upgrade can tell what it is replacing.

## Install in another repository

1. Copy this directory’s **contents** into the repository root, preserving hidden directories. Merge `.gitignore` into any existing one.
2. **If the default branch is not `main`,** rename `docs/handoffs/main.md` and `main.history.md` to match it and update the index row in `docs/handoffs/README.md`. Skipping this fails validation immediately: the checked-out branch must appear in the index.
3. Edit `docs/handoffs/REPOSITORY.md` for that repository — default branch, check profile, permissions, toolchain notes.
4. Fill in `docs/handoffs/<default-branch>.md` and record the installation milestone in the adjacent history. Both ship with placeholders that `--installed` will reject until replaced.
5. Update the active branch roles and merge order in `docs/handoffs/README.md`.
6. Delete any per-tool shim you do not use. Only `AGENTS.md` is required.
7. Run `python scripts/validate_handoffs.py --installed`.
8. Commit the complete setup.

If `python` is not on PATH, use `python3` (most Linux/macOS) or `py` (Windows).

## Portable files

```text
AGENTS.md                    authoritative agent defaults; the only required entry point
CLAUDE.md                    per-tool shims, each pointing at AGENTS.md; delete unused ones
GEMINI.md
.cursor/rules/handoff-maintenance.mdc
.github/copilot-instructions.md
.github/workflows/handoff-validation.yml
.gitignore
VERSION
CHANGELOG.md
docs/handoffs/
  MASTER_HANDOFF.md          lifecycle and recovery reference
  REPOSITORY.md              repository-specific policy and check profile
  MULTI_AGENT.md             concurrent-agent worktree isolation
  README.md                  active branch index
  HISTORY.md                 global close ledger
  main.md                    rename to the default branch if it is not `main`
  main.history.md
  archive/README.md
  templates/
    BRANCH_HANDOFF.md
    BRANCH_HISTORY.md
    ARCHIVED_HANDOFF.md
scripts/validate_handoffs.py
scripts/context_probe.py
scripts/compact_check.py
scripts/test_agent_tools.py  standard-library tests for all three tools
```

`AGENTS.md` is the lean, vendor-neutral entry point and the single source of the defaults. The shims exist only so each tool loads something it recognises; every one of them just points back at `AGENTS.md`. Add a shim for any other tool the same way — one short file, no duplicated protocol. The validator caps `AGENTS.md` at 5,000 characters and each shim at 600.

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

For agents that are actually working concurrently, follow `docs/handoffs/MULTI_AGENT.md`: one Git worktree (folder + branch) per agent. Record any toolchain-specific worktree steps — files to copy, one-project-per-worktree IDEs — in `docs/handoffs/REPOSITORY.md`.

Do not copy archived branch data from another repository. Each repository builds its own active handoffs, per-branch histories, and global close ledger.

