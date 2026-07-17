# Portable Git Handoff System

Reusable branch-handoff framework for Cursor, Gemini/Google agents, and tools that honor `AGENTS.md`.

## Install in another repository

1. Copy this directory’s **contents** into the repository root, preserving hidden directories.
2. Edit `docs/handoffs/REPOSITORY.md` for that repository.
3. Replace placeholders in `docs/handoffs/main.md` and `main.history.md` with the real default-branch tip.
4. Update the active table in `docs/handoffs/README.md`.
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
```

`AGENTS.md` is the vendor-neutral entry point. Cursor also receives an always-applied rule; Gemini-compatible agents receive `GEMINI.md`. Other IDE-specific instruction files should point to `AGENTS.md` rather than duplicate the full protocol.

Do not copy archived branch data from another repository. Each repository builds its own active handoffs, per-branch histories, and global close ledger.

