# Branch Handoff Index

Read [MASTER_HANDOFF.md](MASTER_HANDOFF.md) and [REPOSITORY.md](REPOSITORY.md) first.

Each active branch has a replacement-style handoff and adjacent append-only history. Closed branches are archived under [archive/](archive/) and logged in [HISTORY.md](HISTORY.md).

Last verified: `YYYY-MM-DD`

| Branch | Tip/state | Role | Handoff | History |
|---|---|---|---|---|
| `main` | `<replace with sha/state>` | Shared integration branch | [main.md](main.md) | [history](main.history.md) |

## Current merge order

`<Describe current dependencies or state that no feature branches are open.>`

New branches use [templates/](templates/). Validate with `python scripts/validate_handoffs.py`.

