# Branch Handoff Index

Active branch inventory and merge order. Consult the linked handoff when resuming that branch; detailed lifecycle and multi-agent guides are conditional references, not required startup reading.

| Branch | Role | Handoff | History |
|---|---|---|---|
| `main` | Shared integration branch | [main.md](main.md) | [history](main.history.md) |

## Current merge order

No active dependent branches. Add durable/concurrent branches here in dependency order; routine branches remain unindexed.

## Row format

One row per active branch, four columns. The validator reads the branch name and both link targets; link text is free.

```markdown
| `feature/example` | Feature | [handoff](feature/example.md) | [history](feature/example.history.md) |
```

- The branch name is in backticks, and both targets mirror it: `<branch>.md` and `<branch>.history.md`.
- Every branch listed here must have both files present. Add the current branch only for durable or concurrent work; routine branches intentionally have no row or records.
- Branches owned by other worktrees do not need rows here until they merge.

Update this index only when durable/concurrent branch inventory, role, or merge order changes. Those branches use [templates/](templates/) and validate with `--require-current-handoff`; routine branches use Git only. For actual concurrency, use separate worktrees as described in [MULTI_AGENT.md](MULTI_AGENT.md).
