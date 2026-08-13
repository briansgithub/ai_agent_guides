#!/usr/bin/env python3
"""Estimate context risk locally and emit bounded, recency-first text slices."""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

READ_CHUNK = 1024 * 1024

# Single-file risk bands, applied to the calibrated point estimate.
LOW_TOKEN_LIMIT = 2_000
MEDIUM_TOKEN_LIMIT = 8_000
HIGH_TOKEN_LIMIT = 20_000

# Batch (TOTAL) risk bands. A batch competes for the whole context window, so it
# is judged on a different scale than one file. Using the single-file thresholds
# here made any handful of small documents report "high", which pushed agents
# into asking permission to read files that were individually safe.
BATCH_LOW_TOKEN_LIMIT = 10_000
BATCH_MEDIUM_TOKEN_LIMIT = 30_000
BATCH_HIGH_TOKEN_LIMIT = 75_000

# Calibrated against cl100k_base over Markdown, Python, and YAML sources:
# ASCII text measured 3.8-5.1 characters per token (mean 4.47); CJK measured
# about 1.12 characters per token. ESTIMATE is the classification signal; LOW
# and HIGH bound the reported range. Estimating from the high end (the previous
# behaviour) inflated every file by roughly 50% and promoted whole bands.
ASCII_DIVISOR_ESTIMATE = 4.2
ASCII_DIVISOR_LOW = 5.1
ASCII_DIVISOR_HIGH = 3.7
WIDE_DIVISOR_ESTIMATE = 1.1
WIDE_DIVISOR_LOW = 1.45
WIDE_DIVISOR_HIGH = 0.95

DEFAULT_SKIPS = {".git", ".agent-artifacts", "__pycache__", "node_modules"}


@dataclass
class FileRisk:
    path: str
    bytes: int
    lines: int | None
    token_low: int | None
    token_estimate: int | None
    token_high: int | None
    risk: str
    note: str


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path.resolve())


def is_probably_binary(path: Path) -> bool:
    with path.open("rb") as stream:
        sample = stream.read(8192)
    if b"\x00" in sample:
        return True
    if not sample:
        return False
    controls = sum(byte < 9 or 13 < byte < 32 for byte in sample)
    return controls / len(sample) > 0.20


def estimate_tokens(ascii_characters: int, wide_characters: int, bound: str) -> int:
    """Estimate tokens for a character mix. `bound` is low, estimate, or high."""
    divisors = {
        "low": (ASCII_DIVISOR_LOW, WIDE_DIVISOR_LOW),
        "estimate": (ASCII_DIVISOR_ESTIMATE, WIDE_DIVISOR_ESTIMATE),
        "high": (ASCII_DIVISOR_HIGH, WIDE_DIVISOR_HIGH),
    }
    ascii_divisor, wide_divisor = divisors[bound]
    return math.ceil(ascii_characters / ascii_divisor + wide_characters / wide_divisor)


def classify(token_estimate: int) -> tuple[str, str]:
    """Band one file from its calibrated point estimate."""
    if token_estimate <= LOW_TOKEN_LIMIT:
        return "low", "full read usually safe"
    if token_estimate <= MEDIUM_TOKEN_LIMIT:
        return "medium", "search or chunk first"
    if token_estimate <= HIGH_TOKEN_LIMIT:
        return "high", "chunk; justify full read"
    return "extreme", "confirm before full read"


def classify_batch(token_estimate: int) -> tuple[str, str]:
    """Band a whole scan. A batch is judged against the context window."""
    if token_estimate <= BATCH_LOW_TOKEN_LIMIT:
        return "low", "reading this set is usually safe"
    if token_estimate <= BATCH_MEDIUM_TOKEN_LIMIT:
        return "medium", "prefer the files you actually need"
    if token_estimate <= BATCH_HIGH_TOKEN_LIMIT:
        return "high", "select a subset; justify reading all"
    return "extreme", "confirm before reading this set"


def inspect_file(path: Path) -> FileRisk:
    size = path.stat().st_size
    if is_probably_binary(path):
        return FileRisk(
            display_path(path), size, None, None, None, None, "binary", "do not submit as text"
        )

    characters = ascii_characters = newlines = 0
    non_ascii_characters = 0
    last_character = ""
    with path.open("r", encoding="utf-8", errors="replace", newline="") as stream:
        while chunk := stream.read(READ_CHUNK):
            characters += len(chunk)
            ascii_count = sum(ord(character) < 128 for character in chunk)
            ascii_characters += ascii_count
            non_ascii_characters += len(chunk) - ascii_count
            newlines += chunk.count("\n")
            last_character = chunk[-1]

    lines = 0 if characters == 0 else newlines + (0 if last_character == "\n" else 1)
    # Tokenization varies by model and content, so report a range. Routing uses
    # the calibrated midpoint: banding on the pessimistic end promotes ordinary
    # files into "confirm before reading" and manufactures needless round trips.
    token_low = estimate_tokens(ascii_characters, non_ascii_characters, "low")
    token_estimate = estimate_tokens(ascii_characters, non_ascii_characters, "estimate")
    token_high = estimate_tokens(ascii_characters, non_ascii_characters, "high")
    risk, note = classify(token_estimate)
    return FileRisk(
        display_path(path), size, lines, token_low, token_estimate, token_high, risk, note
    )


def iter_files(paths: list[Path], recursive: bool) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for candidate in paths:
        resolved = candidate.resolve()
        if resolved.is_file():
            if resolved not in seen:
                files.append(resolved)
                seen.add(resolved)
            continue
        if not resolved.is_dir():
            raise FileNotFoundError(candidate)
        if not recursive:
            raise IsADirectoryError(f"{candidate} (use --recursive to scan a directory)")
        for root, directories, names in os.walk(resolved):
            directories[:] = [name for name in directories if name not in DEFAULT_SKIPS]
            for name in names:
                path = (Path(root) / name).resolve()
                if path not in seen:
                    files.append(path)
                    seen.add(path)
    return files


def token_text(low: int | None, high: int | None) -> str:
    if low is None or high is None:
        return "n/a"
    return f"{low:,}-{high:,}"


def sort_key(item: FileRisk) -> tuple[int, int]:
    return (item.token_estimate if item.token_estimate is not None else -1, item.bytes)


def run_scan(args: argparse.Namespace) -> int:
    try:
        paths = iter_files([Path(value) for value in args.paths], args.recursive)
    except (OSError, ValueError) as exc:
        print(f"context probe failed: {exc}", file=sys.stderr)
        return 2

    results: list[FileRisk] = []
    errors: list[str] = []
    for path in paths:
        try:
            results.append(inspect_file(path))
        except OSError as exc:
            errors.append(f"{display_path(path)}: {exc}")

    results.sort(key=sort_key, reverse=True)
    visible = results if args.top == 0 else results[: args.top]
    for result in visible:
        line_text = "n/a" if result.lines is None else f"{result.lines:,}"
        print(
            f"{result.risk:<7} {token_text(result.token_low, result.token_high):>15} tok "
            f"{result.bytes:>10,} B {line_text:>8} lines  {result.path}  [{result.note}]"
        )

    text_results = [item for item in results if item.token_low is not None]
    total_low = sum(item.token_low or 0 for item in text_results)
    total_estimate = sum(item.token_estimate or 0 for item in text_results)
    total_high = sum(item.token_high or 0 for item in text_results)
    total_risk, total_note = classify_batch(total_estimate)
    print(
        f"TOTAL {total_risk} {len(results)} files, "
        f"{sum(item.bytes for item in results):,} B, "
        f"~{total_low:,}-{total_high:,} text tokens "
        f"[{total_note}]"
    )
    if len(visible) < len(results):
        print(f"OUTPUT limited to {len(visible)} largest files; use --top 0 to list all")
    for error in errors:
        print(f"warning: {error}", file=sys.stderr)
    return 1 if errors else 0


def read_tail(path: Path, line_count: int, header_count: int) -> tuple[list[str], list[tuple[int, str]], int]:
    header: list[str] = []
    recent: deque[tuple[int, str]] = deque(maxlen=line_count)
    total = 0
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for total, line in enumerate(stream, start=1):
            if total <= header_count:
                header.append(line)
            recent.append((total, line))
    recent_lines = list(recent)
    while len(recent_lines) > 1 and not recent_lines[-1][1].strip():
        recent_lines.pop()
    return header, recent_lines, total


def bound_lines(
    lines: list[tuple[int, str]], max_characters: int
) -> tuple[list[tuple[int, str]], bool]:
    selected: list[tuple[int, str]] = []
    remaining = max_characters
    truncated = False
    for number, line in reversed(lines):
        text = line.rstrip("\r\n")
        cost = len(text) + 1
        if cost <= remaining:
            selected.append((number, text))
            remaining -= cost
            continue
        truncated = True
        if remaining > 16:
            selected.append((number, "..." + text[-(remaining - 4) :]))
        break
    if len(selected) < len(lines):
        truncated = True
    selected.reverse()
    return selected, truncated


def emit_lines(lines: list[tuple[int, str]], numbered: bool) -> None:
    for number, text in lines:
        print(f"{number:>7} {text}" if numbered else text)


def run_tail(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        if is_probably_binary(path):
            raise ValueError("binary file cannot be emitted as text")
        header, recent, total = read_tail(path, args.lines, args.header_lines)
    except (OSError, ValueError) as exc:
        print(f"context tail failed: {exc}", file=sys.stderr)
        return 2

    start = recent[0][0] if recent else 0
    print(f"--- {display_path(path)} recent lines {start}-{total} of {total} ---")
    if header and start > len(header) + 1:
        header_budget = min(2_000, max(1, args.max_characters // 4))
        bounded_header, header_truncated = bound_lines(
            list(enumerate(header, start=1)), header_budget
        )
        print(f"--- header lines 1-{len(header)} ---")
        if header_truncated:
            print(f"--- header bounded to {header_budget:,} characters ---")
        emit_lines(bounded_header, args.number)
        print(f"--- recent lines {start}-{total} ---")
        recent_budget = max(1, args.max_characters - header_budget)
    else:
        recent_budget = args.max_characters
    bounded_recent, recent_truncated = bound_lines(recent, recent_budget)
    if recent_truncated:
        print(f"--- recent output bounded to {recent_budget:,} characters ---")
    if start > 1:
        print(f"--- older context available: chunk --end-line {start - 1} --lines {args.lines} ---")
    emit_lines(bounded_recent, args.number)
    return 0


def count_lines(path: Path) -> int:
    total = 0
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for total, _line in enumerate(stream, start=1):
            pass
    return total


def run_chunk(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        if is_probably_binary(path):
            raise ValueError("binary file cannot be emitted as text")
        total = count_lines(path)
        end = min(args.end_line, total)
        start = max(1, end - args.lines + 1)
        selected: list[tuple[int, str]] = []
        with path.open("r", encoding="utf-8", errors="replace") as stream:
            for number, line in enumerate(stream, start=1):
                if number < start:
                    continue
                if number > end:
                    break
                selected.append((number, line))
    except (OSError, ValueError) as exc:
        print(f"context chunk failed: {exc}", file=sys.stderr)
        return 2

    if total == 0:
        print(f"--- {display_path(path)} is empty ---")
        return 0
    print(f"--- {display_path(path)} lines {start}-{end} of {total} ---")
    bounded, truncated = bound_lines(selected, args.max_characters)
    if truncated:
        print(f"--- output bounded to {args.max_characters:,} characters ---")
    if start > 1:
        print(f"--- older context available: chunk --end-line {start - 1} --lines {args.lines} ---")
    emit_lines(bounded, args.number)
    return 0


def positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    scan = commands.add_parser("scan", help="estimate file/context risk without emitting contents")
    scan.add_argument("paths", nargs="+", help="files, or directories with --recursive")
    scan.add_argument("--recursive", action="store_true", help="scan directories recursively")
    scan.add_argument("--top", type=int, default=20, help="show N largest files; 0 shows all")
    scan.set_defaults(handler=run_scan)

    tail = commands.add_parser("tail", help="emit the most recent text lines first")
    tail.add_argument("path")
    tail.add_argument("--lines", type=positive_integer, default=120)
    tail.add_argument("--header-lines", type=int, default=0)
    tail.add_argument("--max-characters", type=positive_integer, default=12_000)
    tail.add_argument("--number", action="store_true", help="include line numbers")
    tail.set_defaults(handler=run_tail)

    chunk = commands.add_parser("chunk", help="page backward from an inclusive line number")
    chunk.add_argument("path")
    chunk.add_argument("--end-line", type=positive_integer, required=True)
    chunk.add_argument("--lines", type=positive_integer, default=120)
    chunk.add_argument("--max-characters", type=positive_integer, default=12_000)
    chunk.add_argument("--number", action="store_true", help="include line numbers")
    chunk.set_defaults(handler=run_chunk)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if getattr(args, "top", 0) < 0 or getattr(args, "header_lines", 0) < 0:
        print("counts cannot be negative", file=sys.stderr)
        return 2
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
