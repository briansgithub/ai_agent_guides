# Branch Handoff Index

Active branch inventory and merge order. Consult the linked handoff when resuming that branch; detailed lifecycle and multi-agent guides are conditional references, not required startup reading.

| Branch | Role | Handoff | History |
|---|---|---|---|
| `main` | Shared integration branch | [main.md](main.md) | [history](main.history.md) |
| `chore/flatten-kit-to-root` | Restructure for agent discovery | [handoff](chore/flatten-kit-to-root.md) | [history](chore/flatten-kit-to-root.history.md) |
| `chore/model-routing-policy` | Formal-plan model routing | [handoff](chore/model-routing-policy.md) | [history](chore/model-routing-policy.history.md) |
| `chore/autonomous-commit-policy` | Autonomous commits and Git safety | [handoff](chore/autonomous-commit-policy.md) | [history](chore/autonomous-commit-policy.history.md) |
| `chore/cleanup-artifact-policy` | Confirmed temporary-artifact cleanup | [handoff](chore/cleanup-artifact-policy.md) | [history](chore/cleanup-artifact-policy.history.md) |
| `chore/streamline-agent-rules` | Tiered coordination and standing grants | [handoff](chore/streamline-agent-rules.md) | [history](chore/streamline-agent-rules.history.md) |

## Current merge order

Merge in order: `chore/flatten-kit-to-root`, `chore/model-routing-policy`, `chore/autonomous-commit-policy`, `chore/cleanup-artifact-policy`, then `chore/streamline-agent-rules`. Each branch is based on its predecessor; archive each branch's records in its merge.

## Row format

One row per active branch, four columns. The validator reads the branch name and both link targets; link text is free.

```markdown
| `feature/example` | Feature | [handoff](feature/example.md) | [history](feature/example.history.md) |
```

- The branch name is in backticks, and both targets mirror it: `<branch>.md` and `<branch>.history.md`.
- Every branch listed here must have both files present. Add the current branch only for durable or concurrent work; routine branches intentionally have no row or records.
- Branches owned by other worktrees do not need rows here until they merge.

Update this index only when durable/concurrent branch inventory, role, or merge order changes. Those branches use [templates/](templates/) and validate with `--require-current-handoff`; routine branches use Git only. For actual concurrency, use separate worktrees as described in [MULTI_AGENT.md](MULTI_AGENT.md).
