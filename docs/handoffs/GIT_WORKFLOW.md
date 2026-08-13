# Git Workflow and Commit Policy

Follow these defaults unless the user's current request or narrower repository policy says otherwise. A request that names an exact destructive action and target is authorization for that action only; words such as “finish,” “clean up,” “sync,” or “commit” are not deletion or history-rewrite authorization.

## 1. Inspect and protect

1. Start with `git status --short --branch` and inspect the relevant diff before editing.
2. Treat every pre-existing change as someone else's work until proven otherwise. Never overwrite, restore, stash, stage, or commit unrelated paths.
3. Use `git diff --stat` before a full diff, scope commands with `-- <paths>`, and inspect `git diff --cached` before committing.
4. Never commit secrets, credentials, machine-local configuration, build products, generated artifacts, or large binaries unless the repository intentionally tracks them.

## 2. Branch by default

1. Keep the default branch for integration. Start new features on `feature/<purpose>`, fixes on `fix/<purpose>`, and maintenance on `chore/<purpose>` unless the repository defines another pattern.
2. Use one branch for one coherent purpose. Create a new branch autonomously when starting distinct work; do not mix unrelated changes to avoid another branch.
3. Start from the correct base. Prefer `git fetch` plus inspection over an implicit merge/rebase from `git pull`; integrating remote changes still follows repository authorization rules.
4. Use a separate sibling worktree for concurrent agents. Never switch or repurpose another agent's branch or dirty checkout.

## 3. Stage narrowly

1. Stage exact owned paths with `git add -- <paths>`. Avoid `git add .` or `git add -A` when the tree contains unrelated changes.
2. Review the staged names and diff. Split unrelated or independently reversible changes into separate commits.
3. Preserve useful formatting and line endings; avoid drive-by reformatting, generated churn, or dependency-lock changes unrelated to the task.

## 4. Commit automatically

Normal additive commits on the current task branch are standing-authorized. Do not ask for permission each time.

Commit after a reasonable checkpoint: the requested change or a coherent milestone is complete, the smallest relevant checks pass or limitations are recorded, conflicts are resolved, and the staged diff contains only intended files. Also make a recoverable WIP commit before long idle periods, handoffs, or risky experiments when losing the work would be costly.

Do not create a commit for read-only work, no-op sessions, every prompt, or an incoherent failed attempt. Do not hide known failures in an ordinary completion commit; use a clearly labeled `WIP:` commit only when recoverability justifies it.

Use a concise imperative subject that describes the outcome. Add a body when the reason, risk, migration, or verification is not obvious. After committing, report the commit ID and run `git status --short --branch` once.

## 5. Require explicit authorization for destructive or ancestry-changing Git

Do not perform any of the following without explicit authorization for the exact operation and target:

- Delete tracked files or directories, branches, tags, remotes, worktrees, stashes, refs, or reflog entries. This includes `git rm`, `git clean`, `git branch -d/-D`, `git tag -d`, `git stash drop/clear`, `git worktree remove/prune`, and remote branch deletion.
- Discard or replace uncommitted work with `restore`, `checkout --`, `reset`, clean operations, or equivalent filesystem actions.
- Rewrite, remove, reorder, or transplant history with `commit --amend`, rebase, reset, revert, cherry-pick, filter tools, replace refs, reflog expiration, aggressive pruning, or similar operations.
- Force-update refs with `push --force`, `--force-with-lease`, non-fast-forward pushes, or refspec deletion.
- Bypass safeguards such as hooks or signing requirements.

A normal new commit is the explicit exception: it appends history and is autonomous under section 4. Creating a task branch is also autonomous. Push, PR creation, merge, release/tag creation, and remote changes remain authorization-gated unless `REPOSITORY.md` contains a narrower standing permission.

## 6. Integrate and recover safely

1. Resolve conflicts deliberately; never choose “ours” or “theirs” across the repository merely to make a merge pass. Re-run affected checks.
2. Prefer additional corrective commits over rewriting published history.
3. Before any authorized cleanup, verify the feature tip is reachable from the intended default branch and that no dirty or unique work remains.
4. Keep a pushed-but-unmerged branch. Deletion is a separate authorized action, never an automatic consequence of completion or push.

## 7. Clean temporary artifacts with confirmation

A request such as “clean up” authorizes a bounded inventory and recommendation, not deletion. Find candidates locally, group them by purpose, and ask for confirmation before deleting anything.

Classify a file as disposable only when both are highly likely:

- It is temporary debug, scratch, research, experiment, generated diagnostic, or one-off testing material that is not part of the final deliverable.
- It will not provide future implementation, operational, audit, reproduction, or maintenance value.

Do **not** classify regression assets as temporary merely because they were created while debugging. Keep tests, fixtures, snapshots, scripts, and baselines that verify a fixed bug, confirm previously implemented behavior, prevent recurrence, or improve backward compatibility. If coverage is genuinely duplicated, recommend consolidation separately; deletion still requires exact authorization and equivalent retained coverage.

Before confirmation, provide:

1. Exact paths or tightly bounded patterns, separated into tracked, untracked, and ignored files.
2. Each group’s original purpose and why it is unlikely to be needed again.
3. Any residual value, dependency/reference check, recovery option, and relevant validation to run afterward.
4. Where the durable deletion note will be recorded.

After exact confirmation:

1. Recheck the resolved targets and delete only those approved. A changed or expanded list needs new confirmation.
2. Record a concise durable note in the active handoff/history or the repository's existing decision log. Include the date, grouped paths, original purpose, reason for deletion, and any retained conclusion or replacement. Do not preserve secrets or bulky deleted contents in the note.
3. Run `git status --short --branch`, search for broken references when relevant, and run the smallest check covering the cleanup.
4. Automatically commit tracked deletions and the durable note as one coherent cleanup checkpoint. Report separately any confirmed untracked/ignored deletions that Git cannot record.
