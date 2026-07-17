# Repository Handoff Configuration

Customize this file during installation.

## Git workflow

- Default branch: `main` (change if different)
- Shared remote: `origin` (change if different)
- Branch names: `feature/<purpose>`, `fix/<purpose>`, `chore/<purpose>`
- Merge strategy: merge commit (`--no-ff`) by default; change deliberately if needed
- Direct feature commits to default branch: prohibited
- Agent permissions: require explicit owner authorization for commit, push, PR, merge, stash deletion, and branch deletion unless a documented standing instruction applies

## Required PR-check process

Before each PR, the agent proposes checks and asks the owner to approve/revise them.

Baseline commands:

- Handoffs: `python scripts/validate_handoffs.py`
- Build: `<command>`
- Unit tests: `<command>`
- Lint/type checks: `<command>`
- Manual checks: `<platform/behavior>`

Record approved checks, results, and deferrals in the active branch handoff.

## Handoff locations

- Active index: `docs/handoffs/README.md`
- Active handoff/history: mirrored branch path under `docs/handoffs/`
- Archive: `docs/handoffs/archive/`
- Global close ledger: `docs/handoffs/HISTORY.md`
- Templates: `docs/handoffs/templates/`

