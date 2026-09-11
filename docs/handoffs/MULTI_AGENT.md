# Multi-Agent Parallel Work (Git Worktrees)

Use this only when two or more agents are actually working on the same repository at once. Merely using an IDE or considering future parallel work does not require loading this guide.

## Rule

**Do not run parallel agents in one shared working directory.**

One folder + one checkout forces branch switching, stashing, file overwrites, lock conflicts, and stale agent context.

**Isolate each agent with its own Git worktree:** a separate folder checked out to that agent’s branch, linked to the same underlying `.git` database.

## Why worktrees

| Shared single folder | One worktree per agent |
|---|---|
| Agents fight over the same files | Each agent edits only its checkout |
| Constant `checkout` / stash | No branch swapping to “make room” |
| Dirty WIP blocks other agents | Dirty trees stay local to each worktree |
| Context drifts after switches | Each IDE window stays pinned to one branch |

## Standard workflow

1. Fetch and inspect the intended base in the primary clone:
   ```bash
   git checkout main
   git fetch origin
   git status --short --branch
   git log --oneline main..origin/main
   ```
   Update `main` only when authorized by the current request or an exact standing grant in `REPOSITORY.md`; prefer an explicit fast-forward when appropriate instead of an implicit pull merge/rebase.
2. Create one worktree per agent/task (new branch):
   ```bash
   git worktree add -b feature/<purpose> <path-to-new-folder> main
   ```
   Example:
   ```bash
   git worktree add -b feature/foo ../repo-wt-foo main
   ```
3. Open **that folder** as the agent’s workspace (not the primary clone unless this agent owns it).
4. In that worktree: create the mirrored handoff + `.history.md`, implement, validate with `--require-current-handoff`, and commit on that branch only.
5. When finished: push/PR from that branch, then after merge follow the normal archive + branch-delete protocol.
6. After explicit authorization, remove the worktree when done:
   ```bash
   git worktree remove <path-to-new-folder>
   ```

### Layout, history, and ownership

- Put worktrees beside the primary clone (for example `../repo-wt-foo`); a repository or another worktree must never contain one. Use the repository's configured sibling root and naming pattern.
- A worktree is another checkout of a normal branch, not a disposable copy. Its commits are visible through `git log --all`/`git branch -a`; `git push` publishes that branch only. Merge/PR from the primary/default checkout is what makes the work part of `main`. If “sync” direction is unclear, ask before changing branches or deleting worktrees.
- Record the worktree path, branch, and owned/no-go paths in the active handoff. If another agent has changed an overlapping path, stop before overwriting, notify the owner, and let an authorized Git merge/review resolve it. Never reset, stash, or delete another agent's WIP.

### Completion and cleanup

From the primary/default checkout, after an authorized merge or PR landing:

1. Confirm the feature tip or merge commit is reachable from the remote default branch (`git merge-base --is-ancestor`).
2. Archive the branch handoff/history and update the close ledger/index as required.
3. Run `git worktree list`, then request explicit authorization before removing the sibling worktree or deleting its local branch.
4. Delete the remote branch only with separate owner authorization and after reachability is verified.

If the worktree is dirty or the feature is not merged into the default branch, stop and preserve it—even if its branch was pushed. Do not use `git worktree remove --force`, `git branch -D`, or delete a worktree owned by another agent without explicit authorization.

List worktrees anytime:

```bash
git worktree list
```

## Handoff rules with worktrees

- Handoffs remain in `docs/handoffs/` and are committed **on the branch that owns the work**.
- Each agent updates only its own branch handoff/history in its worktree.
- The active index (`README.md`) on a branch should list that branch (and `main` when present); do not expect every sibling worktree’s branch files to exist in every checkout until those branches merge.
- `python scripts/validate_handoffs.py --require-current-handoff` must pass **in the worktree where the agent is working**. It requires:
  - every branch listed in that checkout’s active index;
  - the currently checked-out branch;
  - size limits, links, and archive pairs.
- It does **not** fail solely because another local branch is checked out in a different worktree and its handoff files are not present here yet.

## Pointing agents at worktrees

- **Cursor:** File → Open Folder on the worktree path; one chat/agent per worktree folder.
- **Google Antigravity / Gemini:** point the agent at the worktree folder (Antigravity often creates worktrees under its own path—treat that folder as the workspace and keep handoffs updated there).
- Keep `AGENTS.md` and the per-tool shims (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.grok/rules/`, `.grok/GROK.md`, `.github/copilot-instructions.md`) in the repo so every worktree inherits the same protocol after checkout.
- Opening an IDE or receiving a routine follow-up does not itself require a formal implementation plan. Use the planning thresholds in `AGENTS.md` and reuse any existing plan instead of proposing one on every prompt.

## IDE-specific worktree notes

Git allows only one checkout of a given branch, so any IDE whose branch switcher targets a branch held by another worktree will refuse it. Open the worktree folder as its own project instead of switching branches.

Toolchains that need gitignored machine-local files (SDK paths, credentials, editor state) require copying those files into each new worktree, and their first index or sync will be slow. Record the specific files and any per-IDE steps for this repository in [REPOSITORY.md](REPOSITORY.md) rather than here — this guide stays toolchain-neutral.

## What not to do

- Do not tell Agent B to `git checkout` Agent A’s branch in the same folder.
- Do not stash Agent A’s WIP so Agent B can run (unless the owner explicitly requests a stash).
- Do not share uncommitted working trees across agents.
- Do not delete another agent’s worktree or branch without owner authorization and reachability checks.

## Anti-loss (keep work findable)

- Commit meaningful WIP on its branch before leaving a worktree idle (`WIP:` commits are fine).
- After the first meaningful commit, push the living branch with authorization: `git push -u origin HEAD`.
- Prefer commits in the branch worktree over long-lived stashes.
- Before requesting `git worktree remove` or `git branch -d`: confirm commits are pushed or merged; do not delete unpushed unique work. Both deletion actions require explicit authorization.
- Discover other work with `git worktree list`, `git branch -vv`, `git stash list`, and `python scripts/validate_handoffs.py` — not a separate inventory doc.

## Stash ownership

- Prefer **no stash** when using worktrees.
- If a stash is unavoidable, message must be: `wip <exact-branch-name>: <short reason>`.
- Record that exact message in the branch handoff Current status.
- Apply only when checked out on the named branch **and** the current handoff lists that stash. Because `pop` deletes on success, use it only with explicit deletion authorization; otherwise use `apply`.
- Never pop/drop a stash named for another branch, or one not listed in the current handoff.
- Drop only with explicit authorization after the work is committed on the named branch or the owner abandons it.
- Do not trust `stash@{N}` alone — indexes shift; ownership is **message branch name + handoff note**.

## Optional alternatives (usually secondary)

1. **Remote/cloud agents** with isolated sandboxes — fine when the product provides full clone isolation; still use one branch per task and keep handoffs updated.
2. **Separate clones** of the same remote — works but wastes disk and duplicates fetches; prefer worktrees for local parallelism.

For this repository’s branch naming, merge, and permission policy, see [REPOSITORY.md](REPOSITORY.md). For handoff lifecycle, see [MASTER_HANDOFF.md](MASTER_HANDOFF.md).
