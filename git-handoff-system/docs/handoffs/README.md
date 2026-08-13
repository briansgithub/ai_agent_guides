# Branch Handoff Index

Active branch inventory and merge order. Consult the linked handoff when resuming that branch; detailed lifecycle and multi-agent guides are conditional references, not required startup reading.

| Branch | Role | Handoff | History |
|---|---|---|---|
| `main` | Shared integration branch | [main.md](main.md) | [history](main.history.md) |

## Current merge order

`<Describe current dependencies or state that no feature branches are open.>`

## Row format

One row per active branch, four columns. The validator reads the branch name and both link targets; link text is free.

```markdown
| `feature/example` | Feature | [handoff](feature/example.md) | [history](feature/example.history.md) |
```

- The branch name is in backticks, and both targets mirror it: `<branch>.md` and `<branch>.history.md`.
- Every branch listed here, plus the branch currently checked out, must have both files present in this checkout.
- Branches owned by other worktrees do not need rows here until they merge.

Update this index only when branch inventory, role, or merge order changes. New branches use [templates/](templates/). For actual concurrent work, use separate Git worktrees as described in [MULTI_AGENT.md](MULTI_AGENT.md).
