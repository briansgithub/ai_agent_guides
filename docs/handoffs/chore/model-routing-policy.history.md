# History: `chore/model-routing-policy`

Append-only milestones. Current state belongs in [model-routing-policy.md](model-routing-policy.md).

### 2026-08-13 — Branch created for model routing
- Commit/base: `ee386c9` on `chore/flatten-kit-to-root`
- Change: Began a post-flatten audit and a vendor-neutral policy for model identity, per-phase routing, and developer-approved switching.
- Validation/decision: Keep the trigger in `AGENTS.md` compact and route details on demand so plans gain model selection without charging routine tasks for the full policy.

### 2026-08-13 — Model routing policy implemented
- Commit/base: uncommitted working tree on `chore/model-routing-policy`
- Change: Added runtime-safe identity reporting, least-cost capable phase routes, the material-benefit switch gate, discovery caveats, and validator/test coverage.
- Validation/decision: Structural validation, 40 standard-library tests, and `git diff --check` passed. Avoid a literal “globally optimal” requirement because hosts may hide identity and alternatives; guessing would create unreliable recommendations and repeated pauses.
