# Changelog

The kit is distributed by copying its contents into a repository root, so an
installed copy cannot be upgraded by a package manager. Record the installed
version in that repository's handoff history, and consult this file when
upgrading.

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
