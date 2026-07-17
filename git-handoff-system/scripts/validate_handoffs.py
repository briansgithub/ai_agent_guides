#!/usr/bin/env python3
"""Validate the permanent branch handoff structure."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

MAX_CHARACTERS = 42_000
INDEX_ROW = re.compile(
    r"^\|\s*`(?P<branch>[^`]+)`\s*\|.*"
    r"\[(?:handoff|main\.md)\]\((?P<handoff>[^)]+)\)\s*\|"
    r"\s*\[history\]\((?P<history>[^)]+)\)\s*\|$"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\((?P<target>[^)]+)\)")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
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


def text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read as UTF-8: {exc}")
        return ""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    handoffs = root / "docs" / "handoffs"
    errors: list[str] = []
    required = [
        root / "AGENTS.md",
        handoffs / "MASTER_HANDOFF.md",
        handoffs / "REPOSITORY.md",
        handoffs / "README.md",
        handoffs / "HISTORY.md",
        handoffs / "templates" / "BRANCH_HANDOFF.md",
        handoffs / "templates" / "BRANCH_HISTORY.md",
        handoffs / "templates" / "ARCHIVED_HANDOFF.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"required file missing: {path.relative_to(root)}")

    markdown = sorted(handoffs.rglob("*.md"))
    for path in markdown:
        content = text(path, errors)
        if len(content) >= MAX_CHARACTERS:
            errors.append(f"{path}: must be strictly below {MAX_CHARACTERS:,} characters")
        for match in MARKDOWN_LINK.finditer(content):
            raw = match.group("target").strip().split(maxsplit=1)[0]
            if "<" in raw or ">" in raw:
                continue
            target = unquote(raw.split("#", 1)[0])
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path}: broken relative link: {target}")

    index = text(handoffs / "README.md", errors)
    entries: dict[str, tuple[Path, Path]] = {}
    for line in index.splitlines():
        match = INDEX_ROW.match(line)
        if match:
            entries[match.group("branch")] = (
                handoffs / match.group("handoff"),
                handoffs / match.group("history"),
            )
    if not entries:
        errors.append("docs/handoffs/README.md: no active branch rows found")

    refs = git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads")
    local = set(refs.stdout.splitlines()) if refs.returncode == 0 else set()
    for branch in sorted(set(entries) | local):
        handoff, history = entries.get(branch, branch_paths(handoffs, branch))
        if not handoff.is_file():
            errors.append(f"{branch}: missing active handoff")
        if not history.is_file():
            errors.append(f"{branch}: missing active history")
        if branch not in entries:
            errors.append(f"{branch}: missing from active index")

    archive = handoffs / "archive"
    archived = {
        path.relative_to(archive).as_posix()
        for path in archive.rglob("*.md")
        if path.name != "README.md"
    }
    for relative in archived:
        peer = (
            relative.removesuffix(".history.md") + ".md"
            if relative.endswith(".history.md")
            else relative.removesuffix(".md") + ".history.md"
        )
        if peer not in archived:
            errors.append(f"archive/{relative}: missing pair {peer}")

    base = f"origin/{os.environ['GITHUB_BASE_REF']}" if os.environ.get("GITHUB_BASE_REF") else None
    if base and git(root, "rev-parse", "--verify", base).returncode == 0:
        for path in markdown:
            if path.name != "HISTORY.md" and not path.name.endswith(".history.md"):
                continue
            relative = path.relative_to(root).as_posix()
            old = git(root, "show", f"{base}:{relative}")
            if old.returncode == 0 and not text(path, errors).startswith(old.stdout):
                errors.append(f"{relative}: prior append-only content changed")

    if errors:
        print("Handoff validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Handoff validation passed: {len(markdown)} files, {len(entries)} active branches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

