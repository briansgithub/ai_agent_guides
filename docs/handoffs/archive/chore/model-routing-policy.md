# Archived: `chore/model-routing-policy`

## Identity

- Final tip: `76540cc` — Add token-aware model routing policy
- Merge commit / PR: `98a5dd4`
- History: [model-routing-policy.history.md](model-routing-policy.history.md)
- Closed: `2026-08-13`

## Goal and scope

Add vendor-neutral, token-aware model selection to formal plans without charging routine work for model analysis.

## What landed

Formal plans report only runtime-known identity, assign least-cost capable routes by phase, and pause only when a known available alternative is materially better.

## Validation

Policy regression tests and structural validation passed before the merge; the complete 47-test suite passed on merged `main`.

## Disposition

- Status: merged
- Remote branch deleted: not applicable; no remote configured
- Local branch deleted: no; separate authorization required
- Cleanup completed: branch records archived; local branch retained
