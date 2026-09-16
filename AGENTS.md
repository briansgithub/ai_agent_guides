# Agent Defaults

Use minimal reliable context/planning/validation. Narrower repo rules win; name overrides. Absent kit files: keep principles, skip mechanisms.

## Work and coaching

- Locate root, read applicable instructions, inspect branch/tree: `git status --short --branch`. Start with requested files.
- Preserve staged, unstaged, untracked, ignored, stashed, and worktree-specific work. Determine ownership/intent before touching it. Never discard/hide work for clean status; leave unrelated work.
- Make narrow changes; name exclusions. Plan only for requests, ambiguity, risk, dependencies, cross-system work, or continuity; reuse until approach changes.
- For plans, report runtime model or `unknown`; tag least-cost capable routes; use `docs/handoffs/MODEL_ROUTING.md` if present. Request known materially better switches; never guess identity, availability, or price.
- For consequential Git or explicit teaching, ask one concise repo-informed question only if safety, scope, or learning depends on it: predict outcome, identify ownership, end state, or recovery. Inspect first; ask only undiscoverable intent/tradeoffs/authority. After the answer, explain and continue. Skip routine read-only/reversible quizzes and repeat approvals; finish authorized work.

## Context

- Search first; read relevant lines, whole files if structure matters. Batch independent reads/commands. Reread for consistency, not redundancy. Cite `path:line`, do not paste files.
- Probe unfamiliar/generated artifacts, not ordinary source/docs. If present: `python scripts/context_probe.py scan <paths>`. Per file/batch TOTAL: low, read; medium, search/chunk; high, justify full read; extreme, ask unless exhaustive review is authorized.
- For logs/history, search identifiers, then recent end, then older pages. Never read source tail-first.
- Ask before unrequested repo-wide/exhaustive history/log inspection or major expansion; give reason and bounded alternative.

## Files and secrets

- Classify before adding/removing: source, tests, schemas, migrations, build definitions, lockfiles, intentional fixtures, config examples, maintained tools often belong in Git; installed dependencies, caches, build products, local databases, process state, ordinary logs, diagnostic exports, credentials, machine settings normally do not.
- For generated files/large datasets, establish producers, consumers, authority, reproducibility, update frequency, licensing, reviewability, offline needs. Names temp/trash/archive/generated/debug never prove disposability.
- Ignores prevent accidental untracked selection; they do not untrack or erase history. Before making tracked content local-only, identify producers/consumers, confirm clean-checkout recreation or operation without it, add precise ignores, and validate. Avoid broad ignores hiding source/fixtures/config.
- Never expose secrets in prompts, logs, tool output, issues/comments, commit messages, shell history, or commands. Treat possibly committed credentials as exposed; direct revocation/rotation before history cleanup without repeating values. Removal/ignores prevent recurrence, not earlier exposure.

## Git changes and recovery

- If present, follow `docs/handoffs/GIT_WORKFLOW.md`. Use narrow branches; autonomously commit coherent, validated in-scope checkpoints. Require explicit authorization for deletion, discard, or history/ancestry changes beyond normal commits; honor exact prior grants unless fresh approval is required.
- Distinguish working tree, index, history. Before staging/committing review staged/unstaged changes: `git diff --stat`/`git diff --cached --stat` before detailed diffs; scope with `-- <paths>`. Inspect untracked candidates.
- Stage named paths/hunks for mixed tasks; verify full scope before bulk staging. Commit one coherent change with required tests/docs. Verify staged work stands alone without unstaged work; do not clean the checkout to prove it.
- Distinguish local branches, remote-tracking refs, actual remote branches. Fetch relevant refs before server conclusions; inspect upstream/divergence. Tracking refs may be stale/incomplete. Rejected pushes signal other work, not barriers to bypass.
- Choose integration by ownership/history. Merges are not inherently mistakes. Rebase unpublished work for clarity. Squash logical changes without erasing valuable steps. Analyze dependencies/duplicate patches before cherry-picks. Explain history shape affecting collaboration.
- Force-pushing shared branches, rebasing shared commits, or overwriting remote history requires explicit authorization, current remote verification, recovery plan, and collaborator coordination.
- Unstage preserving working content. Discard only confirmed disposable/preserved edits. Normally amend/reset private work; revert shared commits. Destructive reset, branch/worktree/stash deletion, and cleanup require authorization, exact target inspection, and proof valuable work stays reachable or preserved.
- Recommend repo-wide rewriting only as a coordinated last-resort migration: define problem, measure benefit, inventory paths/renames, branches, tags, PRs, releases, forks, caches, worktrees, collaborators/clones; preserve a recovery copy, rehearse in an isolated clone, verify, and prevent old clones reintroducing history through explicit instructions. Prevent non-sensitive bloat forward unless measured costs justify disruption.
- Distinguish author/committer; confirm identity ownership before consolidation; prefer mailmap for presentation.

## Verification and delivery

- Run smallest covering checks; broaden for failures, interfaces, dependencies, builds, schemas, migrations, security, concurrency, persistence, PRs/releases. Rerun passing checks only for relevant changes.
- If present, bound noisy output with `python scripts/compact_check.py --name <label> -- <command>`; `--quiet` silences success; `--shell` handles pipelines/wrappers.
- Report exact commands/results and what they establish; distinguish passed from skipped/unrun. After two diagnose/fix/retest cycles per failure, summarize and ask before expanding.
- Make PRs testable proposals: problem, behavior, validation, risks. Review actual diffs; update descriptions with scope. Validate the exact proposed revision; inspect path filters/revision selection when relevant. Workflow files do not prove host branch protection/required-check settings.
- Link releases to immutable source, artifact/build, checks, platform, distribution event, stable release ref. Branch names/build numbers are incomplete provenance.

## Handoffs

- Record only what affects resumption, in existing durable context. Get transient status from Git.
- Before parallel branch/stash/clone/worktree creation, handoff, consolidation, or removal, record dated branch, commit, dirty/untracked state, validation, risks, next action. Check worktrees even for merged branches. Stashes/reflogs/local recovery refs are not shared backups.
- If `docs/handoffs/` exists: routine localized/single-session work uses Git; durable multi-session/material/risky/decision-heavy work adds branch handoff/history; concurrent adds separate sibling worktrees per agent.
- Route on demand: `MASTER_HANDOFF.md` lifecycle/recovery, `REPOSITORY.md` standing permissions/checks, `MULTI_AGENT.md` concurrency only. Read only needed active/recent records.
- Update durable/concurrent handoffs once at end for changed objective/decisions/blockers/risks/validation/next action; append only milestones. No routine/read-only/no-op records.
- Close durable work from primary checkout: verify reachability, archive records; obtain removal authorization unless `REPOSITORY.md` grants it. Stop on dirty/unmerged work; never force-delete or overwrite another agent's work.
- After structural changes, if present: `python scripts/validate_handoffs.py --quiet`; add `--require-current-handoff` for durable/concurrent branches. Never delete branch documentation.

If `python` is missing, use `python3` or `py`.
