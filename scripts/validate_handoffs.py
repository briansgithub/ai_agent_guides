#!/usr/bin/env python3
"""Validate the permanent branch handoff structure."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

POLICY_MAX_CHARACTERS = 20_000
HANDOFF_MAX_CHARACTERS = 6_000
HISTORY_MAX_CHARACTERS = 12_000
# Always-loaded entry points. AGENTS.md carries every default an agent applies
# without being asked, so it gets room for one imperative rule per line; dense
# comma-packed prose fits a smaller budget but is followed less reliably.
ENTRYPOINT_LIMITS = {
    "AGENTS.md": 5_000,
    "CLAUDE.md": 600,
    "GEMINI.md": 600,
    ".cursor/rules/handoff-maintenance.mdc": 600,
    ".github/copilot-instructions.md": 600,
}
POLICY_FILES = {
    "MASTER_HANDOFF.md",
    "REPOSITORY.md",
    "MULTI_AGENT.md",
    "README.md",
}
# Link text is presentational; only the branch name and the two targets are
# contractual. Pinning the label to a literal `handoff`/`history` silently
# dropped naturally worded rows out of the index.
INDEX_ROW = re.compile(
    r"^\|\s*`(?P<branch>[^`]+)`\s*\|[^|]*\|"
    r"\s*\[[^\]]*\]\((?P<handoff>[^)]+)\)\s*\|"
    r"\s*\[[^\]]*\]\((?P<history>[^)]+)\)\s*\|$"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\((?P<target>[^)]+)\)")
# `<branch>.history.md` plus the documented rollover forms: `<branch>.history.2.md`
# for per-branch segments and `HISTORY/<year>.md` for the global ledger.
HISTORY_SEGMENT = re.compile(r"^(?P<stem>.+)\.history(?:\.\d+)?\.md$")
# Unfilled template text. Only applied to live branch records, and only after
# fenced blocks and HTML comments are stripped, because policy documents use
# `<branch>` and `<path>` legitimately as command syntax.
PLACEHOLDER = re.compile(r"<[^<>\n]{2,}>|YYYY-MM-DD")
FENCED_BLOCK = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def branch_paths(handoffs: Path, branch: str) -> tuple[Path, Path]:
    return handoffs / f"{branch}.md", handoffs / f"{branch}.history.md"


def strip_documentation(text: str) -> str:
    """Drop fenced blocks and HTML comments.

    Format examples and commented-out templates are documentation, not live
    content: an example index row must not register as an active branch, and a
    sample link must not be resolved against the filesystem.
    """
    return FENCED_BLOCK.sub("", HTML_COMMENT.sub("", text))


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read as UTF-8: {exc}")
        return ""


def is_history_file(path: Path, handoffs: Path) -> bool:
    """True for any append-only record, including documented rollover segments."""
    relative = path.relative_to(handoffs)
    parts = relative.parts
    if path.name == "HISTORY.md":
        return True
    # Global ledger rollover: docs/handoffs/HISTORY/2026.md
    if "HISTORY" in parts[:-1]:
        return True
    return bool(HISTORY_SEGMENT.match(path.name))


def size_limit(path: Path, handoffs: Path) -> int:
    relative = path.relative_to(handoffs)
    if is_history_file(path, handoffs):
        return HISTORY_MAX_CHARACTERS
    if path.name in POLICY_FILES and len(relative.parts) == 1:
        return POLICY_MAX_CHARACTERS
    if relative.parts[:1] == ("templates",):
        return POLICY_MAX_CHARACTERS
    if relative.as_posix() == "archive/README.md":
        return POLICY_MAX_CHARACTERS
    return HANDOFF_MAX_CHARACTERS


def validate_sizes(handoffs: Path, markdown_files: list[Path], errors: list[str]) -> None:
    for path in markdown_files:
        text = read_text(path, errors)
        limit = size_limit(path, handoffs)
        if len(text) >= limit:
            errors.append(
                f"{path}: {len(text):,} characters; must be strictly below "
                f"{limit:,}"
            )


def validate_entrypoint_sizes(root: Path, errors: list[str]) -> None:
    for relative, limit in ENTRYPOINT_LIMITS.items():
        path = root / relative
        if not path.is_file():
            continue
        text = read_text(path, errors)
        if len(text) >= limit:
            errors.append(
                f"{path}: {len(text):,} characters; always-loaded entry point "
                f"must be strictly below {limit:,}"
            )


def validate_links(markdown_files: list[Path], errors: list[str]) -> None:
    ignored_prefixes = ("http://", "https://", "mailto:", "#", "<")
    for path in markdown_files:
        text = strip_documentation(read_text(path, errors))
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group("target").strip().split(maxsplit=1)[0]
            if "<" in raw_target or ">" in raw_target:
                continue
            target = raw_target.strip("<>")
            target = unquote(target.split("#", 1)[0])
            if not target or target.startswith(ignored_prefixes):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}: broken relative link: {target}")


def parse_index(handoffs: Path, errors: list[str]) -> dict[str, tuple[Path, Path]]:
    index = handoffs / "README.md"
    text = strip_documentation(read_text(index, errors))
    entries: dict[str, tuple[Path, Path]] = {}
    for line in text.splitlines():
        match = INDEX_ROW.match(line)
        if not match:
            continue
        branch = match.group("branch")
        entries[branch] = (
            handoffs / match.group("handoff"),
            handoffs / match.group("history"),
        )
    if not entries:
        errors.append(f"{index}: no active branch rows found")
    return entries


def validate_active_pairs(
    root: Path,
    handoffs: Path,
    entries: dict[str, tuple[Path, Path]],
    errors: list[str],
    verbose: bool,
) -> None:
    """Require handoffs for indexed branches and the current checkout only.

    Other local branches may live in sibling worktrees; their handoff files are
    not required to exist in this working tree until those branches merge.
    """
    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    toplevel = run_git(root, "rev-parse", "--show-toplevel")
    in_repo = (
        inside.returncode == 0
        and inside.stdout.strip() == "true"
        and toplevel.returncode == 0
        and Path(toplevel.stdout.strip()).resolve() == root.resolve()
    )

    current_branch = ""
    local_branches: set[str] = set()
    if in_repo:
        current = run_git(root, "branch", "--show-current")
        current_branch = current.stdout.strip() if current.returncode == 0 else ""
        branches = run_git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads")
        local_branches = set(branches.stdout.splitlines()) if branches.returncode == 0 else set()

    required = set(entries)
    if current_branch:
        required.add(current_branch)

    for branch in sorted(required):
        handoff, history = entries.get(branch, branch_paths(handoffs, branch))
        if not handoff.is_file():
            errors.append(f"{branch}: missing active handoff {handoff.relative_to(root)}")
        if not history.is_file():
            errors.append(f"{branch}: missing active history {history.relative_to(root)}")
        if branch not in entries:
            errors.append(f"{branch}: missing from docs/handoffs/README.md active index")
            if branch == current_branch and set(entries) == {"main"} and branch != "main":
                errors.append(
                    f"  hint: the kit ships an index for `main`. If `{branch}` is this "
                    f"repository's default branch, rename docs/handoffs/main.md and "
                    f"main.history.md to `{branch}.md` / `{branch}.history.md` and update "
                    f"the index row and REPOSITORY.md."
                )

    for branch, (handoff, history) in entries.items():
        expected_handoff, expected_history = branch_paths(handoffs, branch)
        if handoff.resolve() != expected_handoff.resolve():
            errors.append(f"{branch}: index handoff does not mirror branch path")
        if history.resolve() != expected_history.resolve():
            errors.append(f"{branch}: index history does not mirror branch path")

    if in_repo and verbose:
        for branch in sorted(local_branches - required):
            print(
                f"note: local branch `{branch}` not required in this worktree's "
                f"active index (ok when owned by another worktree)",
                file=sys.stderr,
            )


def validate_archive_pairs(root: Path, handoffs: Path, errors: list[str]) -> None:
    archive = handoffs / "archive"
    if not archive.is_dir():
        errors.append(f"{archive.relative_to(root)}: archive directory missing")
        return

    files = {
        path.relative_to(archive).as_posix()
        for path in archive.rglob("*.md")
        if path.name != "README.md"
    }
    # Group by branch stem so that `foo.md`, `foo.history.md`, and any numbered
    # rollover segment `foo.history.2.md` count as one archived branch. Requiring
    # a literal `<name>.history.md` peer for every file rejected the segment
    # naming that BRANCH_HISTORY.md instructs authors to use.
    handoffs_by_stem: dict[str, str] = {}
    histories_by_stem: dict[str, list[str]] = {}
    for relative in sorted(files):
        match = HISTORY_SEGMENT.match(Path(relative).name)
        if match:
            stem = (Path(relative).parent / match.group("stem")).as_posix()
            histories_by_stem.setdefault(stem, []).append(relative)
        else:
            handoffs_by_stem[relative.removesuffix(".md")] = relative

    for stem, relative in sorted(handoffs_by_stem.items()):
        if stem not in histories_by_stem:
            errors.append(
                f"archive/{relative}: missing paired archive history {stem}.history.md"
            )
    for stem, segments in sorted(histories_by_stem.items()):
        if stem not in handoffs_by_stem:
            errors.append(
                f"archive/{segments[0]}: missing paired archive handoff {stem}.md"
            )


def report_parallel_state(
    root: Path,
    handoffs: Path,
    entries: dict[str, tuple[Path, Path]],
) -> None:
    """Print worktree / tracking / stash hints (ledger via git, not a new doc)."""
    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    toplevel = run_git(root, "rev-parse", "--show-toplevel")
    in_repo = (
        inside.returncode == 0
        and inside.stdout.strip() == "true"
        and toplevel.returncode == 0
        and Path(toplevel.stdout.strip()).resolve() == root.resolve()
    )
    if not in_repo:
        return

    print("Parallel-state ledger (git):")
    worktrees = run_git(root, "worktree", "list", "--porcelain")
    if worktrees.returncode == 0 and worktrees.stdout.strip():
        path = branch = None
        for line in worktrees.stdout.splitlines():
            if line.startswith("worktree "):
                path = line[len("worktree ") :]
            elif line.startswith("branch "):
                ref = line[len("branch ") :]
                branch = ref.removeprefix("refs/heads/") if ref.startswith("refs/") else ref
            elif line == "":
                if path:
                    label = branch or "(detached)"
                    print(f"- worktree: {path} -> {label}")
                path = branch = None
        if path:
            print(f"- worktree: {path} -> {branch or '(detached)'}")
    else:
        listing = run_git(root, "worktree", "list")
        for line in listing.stdout.splitlines():
            print(f"- worktree: {line}")

    branches = run_git(
        root,
        "for-each-ref",
        "--format=%(refname:short)%09%(upstream:short)%09%(upstream:track)",
        "refs/heads",
    )
    if branches.returncode == 0:
        for line in branches.stdout.splitlines():
            name, upstream, track = (line.split("\t") + ["", ""])[:3]
            if name == "main":
                continue
            if not upstream:
                print(f"- warning: branch `{name}` has no upstream (push with -u to back up)")
            elif track:
                print(f"- note: branch `{name}` tracking {upstream} {track}".rstrip())

    stash = run_git(root, "stash", "list")
    if stash.returncode != 0 or not stash.stdout.strip():
        print("- stash: (none)")
        return

    print("- stash entries:")
    wip_msg = re.compile(r"^wip\s+(?P<branch>[^:]+):\s*(?P<reason>.+)$", re.I)
    for line in stash.stdout.splitlines():
        # stash@{N}: On <branch>: <rest>  OR  stash@{N}: WIP on <branch>: <rest>
        print(f"  - {line}")
        body = line.split(": ", 1)[-1] if ": " in line else line
        # Prefer explicit wip <branch>: format inside the message tail
        named = None
        for part in (body, line):
            match = wip_msg.search(part)
            if match:
                named = match.group("branch").strip()
                break
        if named is None:
            on_match = re.search(r"^(?:WIP on|On)\s+(\S+):", body)
            if on_match:
                named = on_match.group(1)
                print(
                    f"    hint: rename to `wip {named}: <reason>` for ownership clarity"
                )
        if not named:
            print("    warning: stash message missing `wip <branch>: <reason>` ownership format")
            continue
        handoff, _history = entries.get(named, branch_paths(handoffs, named))
        if not handoff.is_file():
            print(f"    warning: no active handoff file for stash branch `{named}` in this checkout")
            continue
        text = handoff.read_text(encoding="utf-8", errors="replace")
        if named not in text and "stash" not in text.lower():
            print(
                f"    warning: handoff `{handoff.relative_to(root)}` does not mention stash/`{named}`"
            )


def validate_no_placeholders(
    root: Path, handoffs: Path, markdown_files: list[Path], errors: list[str]
) -> None:
    """Reject unfilled template text in live handoffs (`--installed` only).

    The kit ships `main.md` / `main.history.md` with placeholders on purpose, so
    this runs opt-in: a repository that has installed the kit turns it on, the
    kit's own repository does not.
    """
    for path in markdown_files:
        relative = path.relative_to(handoffs)
        if relative.parts[:1] == ("templates",):
            continue
        # Policy documents legitimately show `<branch>`-style command syntax.
        if path.name in POLICY_FILES or relative.as_posix() == "archive/README.md":
            continue
        text = strip_documentation(read_text(path, errors))
        found = sorted({match.group(0) for match in PLACEHOLDER.finditer(text)})
        if found:
            shown = ", ".join(found[:4]) + ("..." if len(found) > 4 else "")
            errors.append(
                f"{path.relative_to(root)}: unfilled template placeholder(s): {shown}"
            )


def resolve_base_ref(root: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    github_base = os.environ.get("GITHUB_BASE_REF")
    if github_base:
        return f"origin/{github_base}"
    return None


def validate_append_only(
    root: Path,
    handoffs: Path,
    markdown_files: list[Path],
    base_ref: str | None,
    errors: list[str],
) -> None:
    if not base_ref:
        return
    if run_git(root, "rev-parse", "--verify", base_ref).returncode != 0:
        errors.append(f"base ref not found for append-only check: {base_ref}")
        return

    for path in markdown_files:
        relative = path.relative_to(root).as_posix()
        if not is_history_file(path, handoffs):
            continue
        previous = run_git(root, "show", f"{base_ref}:{relative}")
        if previous.returncode != 0:
            continue
        current = read_text(path, errors)
        if not current.startswith(previous.stdout):
            errors.append(f"{relative}: append-only history changed or removed prior content")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-ref",
        help="Git ref used to verify append-only histories (default: origin/$GITHUB_BASE_REF)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print worktree, branch-tracking, and stash diagnostics",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="emit nothing when validation passes",
    )
    parser.add_argument(
        "--installed",
        action="store_true",
        help="also reject unfilled template placeholders (use in repositories that "
        "have installed the kit, not in the kit's own repository)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    handoffs = root / "docs" / "handoffs"
    errors: list[str] = []

    # AGENTS.md is authoritative. The per-tool shims that point at it are
    # optional: a shop that uses only one agent should be able to delete the
    # others without failing validation. Any shim that is present is still
    # budget-checked by validate_entrypoint_sizes.
    required = [
        root / "AGENTS.md",
        root / "scripts" / "context_probe.py",
        root / "scripts" / "compact_check.py",
        handoffs / "MASTER_HANDOFF.md",
        handoffs / "REPOSITORY.md",
        handoffs / "MULTI_AGENT.md",
        handoffs / "README.md",
        handoffs / "HISTORY.md",
        handoffs / "templates" / "BRANCH_HANDOFF.md",
        handoffs / "templates" / "BRANCH_HISTORY.md",
        handoffs / "templates" / "ARCHIVED_HANDOFF.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"required file missing: {path.relative_to(root)}")

    markdown_files = sorted(handoffs.rglob("*.md"))
    validate_entrypoint_sizes(root, errors)
    validate_sizes(handoffs, markdown_files, errors)
    validate_links(markdown_files + [root / "AGENTS.md"], errors)
    entries = parse_index(handoffs, errors)
    validate_active_pairs(root, handoffs, entries, errors, args.verbose)
    validate_archive_pairs(root, handoffs, errors)
    if args.installed:
        validate_no_placeholders(root, handoffs, markdown_files, errors)
    validate_append_only(
        root, handoffs, markdown_files, resolve_base_ref(root, args.base_ref), errors
    )
    if args.verbose:
        report_parallel_state(root, handoffs, entries)

    if errors:
        print("Handoff validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if not args.quiet:
        branch_label = "branch" if len(entries) == 1 else "branches"
        print(
            f"Handoff validation passed: {len(markdown_files)} Markdown files, "
            f"{len(entries)} active {branch_label}."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

