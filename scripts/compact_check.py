#!/usr/bin/env python3
"""Run one check while keeping complete logs off the AI context path."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import tempfile
import time
from collections import deque
from datetime import datetime
from pathlib import Path


def positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def safe_name(value: str) -> str:
    cleaned = "".join(character if character.isalnum() or character in "-_" else "-" for character in value)
    return cleaned.strip("-") or "check"


def tail_lines(path: Path, count: int, max_characters: int) -> tuple[list[str], bool]:
    recent: deque[str] = deque(maxlen=count)
    total_lines = 0
    with path.open("r", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            total_lines += 1
            recent.append(line.rstrip("\r\n"))
    selected: list[str] = []
    remaining = max_characters
    truncated = total_lines > len(recent)
    for line in reversed(recent):
        cost = len(line) + 1
        if cost <= remaining:
            selected.append(line)
            remaining -= cost
            continue
        truncated = True
        if remaining > 16:
            selected.append("..." + line[-(remaining - 4) :])
        break
    selected.reverse()
    return selected, truncated


def relative_or_absolute(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="check", help="short label used in summaries and log names")
    parser.add_argument("--cwd", default=".", help="working directory for the command")
    parser.add_argument("--artifact-dir", help="failure-log directory (default: system temporary directory)")
    parser.add_argument("--failure-lines", type=positive_integer, default=40)
    parser.add_argument("--failure-characters", type=positive_integer, default=8_000)
    parser.add_argument("--timeout-seconds", type=positive_integer)
    parser.add_argument("--keep-success-log", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="emit nothing when the command passes")
    parser.add_argument(
        "--shell",
        action="store_true",
        help="run through the platform shell, enabling pipelines, builtins, and "
        "wrapper scripts such as ./gradlew or gradlew.bat",
    )
    parser.add_argument(
        "--keep-logs",
        type=positive_integer,
        default=20,
        help="failure logs to retain per artifact directory (default: 20)",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="command and arguments after --")
    return parser


def prune_logs(directory: Path, keep: int) -> None:
    """Bound unattended growth of the failure-log directory."""
    try:
        logs = sorted(directory.glob("*.log"), key=lambda item: item.stat().st_mtime)
    except OSError:
        return
    for stale in logs[: max(0, len(logs) - keep)]:
        try:
            stale.unlink()
        except OSError:
            pass


def terminate_tree(process: subprocess.Popen[bytes]) -> None:
    """Kill the command and any children it spawned (build daemons, test runners)."""
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            capture_output=True,
            check=False,
        )
        return
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except (OSError, ProcessLookupError):
        process.kill()


def main() -> int:
    args = build_parser().parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        print("compact check failed: command required after --", file=sys.stderr)
        return 2

    working_directory = Path(args.cwd).resolve()
    if args.artifact_dir:
        artifact_directory = Path(args.artifact_dir)
        if not artifact_directory.is_absolute():
            artifact_directory = working_directory / artifact_directory
    else:
        artifact_directory = (
            Path(tempfile.gettempdir())
            / "ai-agent-checks"
            / safe_name(working_directory.name)
        )
    artifact_directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    log_path = artifact_directory / f"{stamp}-{safe_name(args.name)}.log"

    start = time.monotonic()
    return_code = 1
    timed_out = False
    launch_error: OSError | None = None
    # A shell run takes the command as one string so pipelines and wrapper
    # scripts behave as typed; the caller owns any quoting inside that string.
    # Otherwise argv is passed through unchanged.
    target: str | list[str] = " ".join(command) if args.shell else command
    # New process group so a timeout can reap the whole tree, not just the child.
    isolation: dict[str, object] = (
        {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        if sys.platform == "win32"
        else {"start_new_session": True}
    )
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        try:
            process = subprocess.Popen(
                target,
                cwd=working_directory,
                stdout=log,
                stderr=subprocess.STDOUT,
                shell=args.shell,
                env=os.environ.copy(),
                **isolation,
            )
        except OSError as exc:
            launch_error = exc
            return_code = 127
            log.write(f"\nFailed to launch command: {exc}\n")
            if not args.shell:
                log.write(
                    "Hint: this runs without a shell. Use --shell for pipelines, "
                    "shell builtins, or wrapper scripts such as ./gradlew.\n"
                )
        else:
            try:
                return_code = process.wait(timeout=args.timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                return_code = 124
                terminate_tree(process)
                process.wait()
                log.write(f"\nTimed out after {args.timeout_seconds} seconds.\n")

    elapsed = time.monotonic() - start
    shown_path = relative_or_absolute(log_path, working_directory)
    if return_code == 0:
        if not args.keep_success_log:
            log_path.unlink(missing_ok=True)
        if not args.quiet:
            suffix = f"; log: {shown_path}" if args.keep_success_log else ""
            print(f"PASS {args.name} ({elapsed:.1f}s{suffix})")
        return 0

    prune_logs(artifact_directory, args.keep_logs)
    reason = "timeout" if timed_out else "launch error" if launch_error else f"exit {return_code}"
    print(f"FAIL {args.name} ({reason}, {elapsed:.1f}s)")
    print(f"Full log: {shown_path}")
    recent, truncated = tail_lines(log_path, args.failure_lines, args.failure_characters)
    print(
        f"--- bounded failure tail: up to {args.failure_lines} lines / "
        f"{args.failure_characters:,} characters ---"
    )
    if truncated:
        print("--- earlier or oversized output omitted; inspect the log selectively if needed ---")
    for line in recent:
        print(line)
    return return_code


if __name__ == "__main__":
    sys.exit(main())
