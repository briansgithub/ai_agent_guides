# Archived: `chore/flatten-kit-to-root`

## Identity

- Final tip: `ee386c9` — Add a pointer shim for every known agent rule-file convention
- Merge commit / PR: `98a5dd4`
- History: [flatten-kit-to-root.history.md](flatten-kit-to-root.history.md)
- Closed: `2026-08-13`

## Goal and scope

Move the kit to the repository root so supported clients can discover its authoritative instructions, CI, scripts, and pointer shims.

## What landed

The nested kit was flattened, the default branch became `main`, entry-point shims redirect to root `AGENTS.md`, and repository-root validation/CI paths became functional.

## Validation

Repository validator and standard-library tool tests passed before and after the stacked merge; rename history was checked with `git log --follow`.

## Disposition

- Status: merged
- Remote branch deleted: not applicable; no remote configured
- Local branch deleted: no; separate authorization required
- Cleanup completed: branch records archived; local branch retained
