# History: `chore/flatten-kit-to-root`

Append-only milestones. Current state belongs in [flatten-kit-to-root.md](flatten-kit-to-root.md).

### 2026-08-13 — Branch created for the flatten
- Commit/base: `bf63b00` on `main`
- Change: Created `chore/flatten-kit-to-root` after renaming `master` to `main` and merging the agent ruleset optimization work.
- Validation/decision: Investigation established that four global agent configs already pointed at this repository's root and named `AGENTS.md` as the entry point, while every discovery file sat one directory below it.

### 2026-08-13 — Kit flattened to the repository root
- Commit/base: `a860b1d`
- Change: Moved all kit entries up one level with `git mv`, naming each explicitly so the dot-directories were not skipped. Moves only, no content edits, to keep rename detection clean.
- Validation/decision: Repaired three latent defects in the process — CI had never run because the workflow was not at the repository root; `validate_append_only` had never compared anything because `relative_to(root)` produced paths that did not exist in the repository; and the allowlisted validator command could not resolve. The validator immediately began reporting this branch's missing records, confirming it now recognises the repository.

### 2026-08-13 — Merged into `main`
- Commit/base: final tip `ee386c9`; merge `98a5dd4`
- Change: Landed the flattened root layout as the base of the coordinated ruleset stack.
- Validation/decision: The complete 47-test tool suite passed on merged `main`; records archived without deleting the local branch.
