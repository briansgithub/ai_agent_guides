# Branch Handoff History

Append-only repository ledger of closed branches. Add exactly one close entry per branch at the bottom. Never rewrite older entries.

Detailed milestones belong in each branch’s adjacent `.history.md` and archive with it.

## Entry format

```markdown
### YYYY-MM-DD — `feature/example` → merged into `main`
- Final tip: `<sha>`
- Merge / PR: `<sha or URL>`
- Summary: <one or two sentences>
- Archive: `archive/feature/example.md`
```

## Entries

<!-- Append below. Before 12,000 characters, start HISTORY/YYYY.md and link it here. -->

### 2026-08-13 — `chore/flatten-kit-to-root` → merged into `main`
- Final tip: `ee386c9`
- Merge / PR: `98a5dd4`
- Summary: Flattened the kit to the repository root and added pointer shims for supported discovery conventions.
- Archive: `archive/chore/flatten-kit-to-root.md`

### 2026-08-13 — `chore/model-routing-policy` → merged into `main`
- Final tip: `76540cc`
- Merge / PR: `98a5dd4`
- Summary: Added token-aware, capability-class routing and a material-benefit model switch gate for formal plans.
- Archive: `archive/chore/model-routing-policy.md`

### 2026-08-13 — `chore/autonomous-commit-policy` → merged into `main`
- Final tip: `d680459`
- Merge / PR: `98a5dd4`
- Summary: Authorized safe task branches and checkpoint commits while protecting destructive and ancestry-changing Git operations.
- Archive: `archive/chore/autonomous-commit-policy.md`

### 2026-08-13 — `chore/cleanup-artifact-policy` → merged into `main`
- Final tip: `578cc32`
- Merge / PR: `98a5dd4`
- Summary: Added confirmed temporary-artifact cleanup, durable deletion notes, and regression/backward-compatibility retention.
- Archive: `archive/chore/cleanup-artifact-policy.md`

### 2026-08-13 — `chore/streamline-agent-rules` → merged into `main`
- Final tip: `31cb5c8`
- Merge / PR: `98a5dd4`
- Summary: Added coordination tiers, exact standing grants, platform smoke evidence, and a compact lifecycle guide.
- Archive: `archive/chore/streamline-agent-rules.md`

