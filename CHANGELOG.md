# Changelog

The kit is distributed by copying its contents into a repository root, so an
installed copy cannot be upgraded by a package manager. Record the installed
version in that repository's handoff history, and consult this file when
upgrading.

## Unreleased

### Added

- Formal plans now identify the runtime-reported provider/model, route each phase
  to the least-cost capable model, and pause before a phase when a known available
  alternative is materially better. The on-demand `MODEL_ROUTING.md` policy
  defines capability classes, total-token accounting, and a developer switch gate
  without hard-coding model catalogs that will go stale.
- Normal task-branch commits and branch creation are now standing-authorized.
  `GIT_WORKFLOW.md` requires automatic coherent checkpoint commits, exact-path
  staging, narrow feature/fix/chore branches, and explicit authorization for
  deletion, discarded work, ancestry changes, pushes, PRs, and merges.

### Clarified

- Root-level pointer shims improve discovery only when the client supports that
  convention and opens this directory as its workspace. Agents working elsewhere
  still need an installed copy or a global/user instruction pointing here.

## 2.1.0

Flattens the kit to the repository root so agent rules are discoverable without
per-tool configuration. **The install procedure changed** — see below.

### Fixed

- **No agent-instruction file was discoverable.** `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `.cursor/`, and `.github/` all sat one directory below the
  repository root, where no tool looks. They are now at the root.
- **CI had never run.** GitHub only executes `<repo-root>/.github/workflows/`;
  the workflow was one level down and therefore inert.
- **`validate_append_only` had never run.** It builds paths with
  `relative_to(root)`; with `root` as the nested kit directory those paths did
  not exist in the repository, so `git show` failed and every history file was
  silently skipped. Append-only enforcement is live for the first time.
- **The validator did not know it was in a repository.** `git rev-parse
  --show-toplevel` did not match its computed root, so `in_repo` was false and
  the checked-out branch was never required to have a handoff record. The
  repository now validates itself.

### Changed

- **Install is no longer "copy this directory's contents."** That instruction is
  now actively destructive: it would drag `.git/`, `file_purposes.md`, and this
  repository's own branch records into the target, producing an install that
  *passes validation while carrying this repository's history as its own*.
  `README.md` now leads with an explicit exclusion list, and `file_purposes.md`
  carries a `Ships` column (`yes` / `no` / `seeded`) for every file.
- **`AGENTS.md` works when read from another repository.** Rules that depend on
  kit files are marked *if present* so the principle survives where the mechanism
  does not; universal rules stay unconditional. Added a precedence rule: where an
  ancestor-directory or global instruction file conflicts, follow the narrower
  repository-scoped rule and name the instruction set aside rather than silently
  choosing.
- **Default branch renamed `master` → `main`**, matching the kit's own docs,
  templates, and CI trigger.
- This repository now keeps live branch records under `docs/handoffs/`, so the
  end-to-end test is coupled to repository state: a new branch needs its records
  before the suite passes. That is the kit applying to itself.

### Added

- Per-tool shims for every known convention beyond the original five: Cline,
  Windsurf, Zed, Aider, JetBrains Junie, Amazon Q, Roo Code, Qodo, and several
  plausible-but-unverified ones. A wrong guess costs one unread 185-byte file; a
  miss means a tool silently applies no rules. Each is a pointer to `AGENTS.md`,
  never a copy — tool-specific files take precedence over `AGENTS.md` in clients
  that read both, so a pointer redirects to the single source.
- A test asserting every shim present points at `AGENTS.md` and stays under budget.
- `.claude/settings.local.json` added to `.gitignore`; it was excluded only by a
  user-level global ignore and would otherwise become tracked for a second contributor.

## 2.0.0

Corrects defects that made documented workflows fail validation, recalibrates
the context estimator against measured tokenizer output, and adds the test suite
that now covers all three tools.

### Fixed

- **Token estimates were roughly 50% high and routed on the pessimistic end.**
  Bands are now computed from a calibrated midpoint (ASCII ~4.5 characters per
  token, CJK ~1.1), measured against `cl100k_base`. Previously a CJK document of
  ~9,600 real tokens was banded `extreme`, whose documented action is to stop and
  ask the owner; ordinary English files were promoted a full band by smart quotes
  and em dashes alone.
- **Batch `TOTAL` risk used single-file thresholds.** Scanning eleven small
  documents reported `TOTAL high [chunk; justify full read]` while every file in
  the set was individually low or medium. `TOTAL` now has its own larger scale.
- **Documented history rollover names failed validation.** `HISTORY/<year>.md`
  and numbered segments such as `feature/foo.history.2.md` received the 6,000
  character handoff limit instead of the 12,000 history limit, and archive
  pairing demanded a peer named `foo.history.2.history.md`. Both forms are now
  recognised, and `MASTER_HANDOFF.md` states the naming convention explicitly.
- **The active-index regex required literal link text.** A row reading
  `[History](...)` or `[feature/foo.md](...)` was silently dropped from the
  index and surfaced later as a confusing "missing from active index" error.
  Link text is now free; only the branch name and both targets are contractual.
  The format is documented in `docs/handoffs/README.md`.
- **`compact_check.py` could not run its own documented example.** `./gradlew
  build` failed to launch and no pipeline or shell builtin was runnable. Added
  `--shell`; a launch failure without it now suggests the flag.
- **A timeout orphaned child processes.** The command now runs in its own
  process group and a timeout reaps the whole tree.
- **Shim size limits contradicted the documentation.** `MASTER_HANDOFF.md`
  specified 600 characters while the validator enforced 400 for `GEMINI.md`.

### Changed

- **`AGENTS.md` budget raised from 3,500 to 5,000 characters** and the file
  rewritten as one imperative rule per line. It had 18 characters of headroom,
  and the pressure to compress had produced dense comma-packed clauses that are
  followed less reliably than short directives.
- **The context probe is scoped to generated and unfamiliar artifacts** — logs,
  build output, data dumps, vendored trees — rather than any unknown file. A
  preflight on ordinary source costs a round trip that a targeted read avoids.
- **Only `AGENTS.md` is required.** Per-tool shims are optional and deleting an
  unused one no longer fails validation. Any shim present is still size-checked.
- **Android Studio guidance moved out of `MULTI_AGENT.md`** into a customizable
  toolchain section in `REPOSITORY.md`. The portable guide is toolchain-neutral;
  the always-loaded file no longer spends its budget naming one IDE.
- Failure logs are pruned to the most recent 20 per artifact directory.

### Added

- `scripts/test_agent_tools.py` — 31 standard-library tests covering all three
  tools. Every fix above has a regression test that fails against the old code.
- CI runs the tests on Linux and Windows; several fixed defects were
  platform-specific.
- `--installed` mode rejects unfilled template placeholders in live branch
  records. The kit's own repository ships those placeholders deliberately and
  does not use the flag.
- `CLAUDE.md` and `.github/copilot-instructions.md` shims.
- `.gitignore`, so an installing repository does not commit tool bytecode.
- `VERSION` and this changelog.
- Efficiency rules in `AGENTS.md`: search before reading, batch independent
  calls, do not re-read a just-written file, cite `path:line` rather than pasting
  contents, `git diff --stat` before `git diff`, report the exact command run.
- An operational test for the vocabulary that carries every append/update
  decision: record something only if an agent resuming the branch would act
  differently without it.
- Filled worked examples in the branch handoff and history templates, including
  history entries that are *not* worth appending.
- Install steps now cover renaming the default-branch records when the default
  branch is not `main`, which previously failed validation on first run.

## 1.0.0

Initial portable handoff framework: permanent branch handoffs, append-only
histories, archive lifecycle, worktree isolation, templates, structural
validator, and CI.
