# Portable Git Handoff System

Reusable branch-handoff framework for Cursor, Gemini/Google agents, and tools that honor `AGENTS.md`.

## Install in another repository

1. Copy this directory’s **contents** into the repository root, preserving hidden directories.
2. Edit `docs/handoffs/REPOSITORY.md` for that repository.
3. Customize durable integration context in `docs/handoffs/main.md` and record the installation/base milestone in `main.history.md`.
4. Update the active branch roles and merge order in `docs/handoffs/README.md`.
5. Run `python scripts/validate_handoffs.py`.
6. Commit the complete setup.

## Portable files

```text
AGENTS.md
GEMINI.md
.cursor/rules/handoff-maintenance.mdc
.github/workflows/handoff-validation.yml
docs/handoffs/
  MASTER_HANDOFF.md
  REPOSITORY.md
  MULTI_AGENT.md
  README.md
  HISTORY.md
  main.md
  main.history.md
  archive/README.md
  templates/
    BRANCH_HANDOFF.md
    BRANCH_HISTORY.md
    ARCHIVED_HANDOFF.md
scripts/validate_handoffs.py
scripts/context_probe.py
scripts/compact_check.py
```

`AGENTS.md` is the lean, vendor-neutral entry point. Cursor also receives a short always-applied rule; Gemini-compatible agents receive `GEMINI.md`. Other IDE-specific instruction files should point to `AGENTS.md` rather than duplicate or preload the full protocol.

The default workflow avoids formal plans for straightforward changes, loads handoff/history documents only when relevant, and uses risk-proportional verification. Repository-wide analysis or unusually expensive validation should be confirmed with the owner when it materially expands an otherwise bounded request.

## Context and output controls

Size-probe candidate context locally without emitting file contents:

```bash
python scripts/context_probe.py scan AGENTS.md docs/handoffs/MASTER_HANDOFF.md
python scripts/context_probe.py scan docs --recursive --top 20
```

Token estimates are heuristic risk bands. Low-risk files may normally be read in full; medium/high files should be searched or chunked first; extreme-risk full reads require confirmation unless exhaustive review is already in scope.

Read the recent end of an append-only log or history, then page backward only if needed:

```bash
python scripts/context_probe.py tail path/to/history.md --lines 120
python scripts/context_probe.py chunk path/to/history.md --end-line 500 --lines 120
```

The tool preserves normal line order inside each chunk. Do not use tail-first reading for source/configuration files whose earlier structure controls interpretation.

Keep noisy test/build output out of AI context while retaining full failure logs locally:

```bash
python scripts/compact_check.py --name unit -- pytest -q --tb=short --maxfail=1
python scripts/compact_check.py --name build --quiet -- ./gradlew build
```

Successful logs are deleted by default; failure logs go to the system temporary directory and only their bounded tail is printed. Use `--artifact-dir` or `--keep-success-log` when persistent artifacts are needed.

For agents that are actually working concurrently, follow `docs/handoffs/MULTI_AGENT.md`: one Git worktree (folder + branch) per agent. For Android Studio / Android apps, open each worktree as its own project (copy `local.properties`; do not branch-switch into a worktree-held branch)—see the Android Studio section in that file.

Do not copy archived branch data from another repository. Each repository builds its own active handoffs, per-branch histories, and global close ledger.

