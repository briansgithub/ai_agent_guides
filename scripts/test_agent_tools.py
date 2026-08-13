#!/usr/bin/env python3
"""Tests for the agent context and validation tools.

Standard library only: an installing repository should not inherit a test
dependency. Run with `python -m unittest discover -s scripts -p "test_*.py"`.

Cases named `regression` cover defects that shipped once: miscalibrated token
bands, batch risk judged on single-file thresholds, size routing that rejected
the rollover filenames the documentation instructs authors to create, an index
regex pinned to literal link text, and a check wrapper that could not run the
command style its own README documented.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import compact_check  # noqa: E402
import context_probe  # noqa: E402
import validate_handoffs  # noqa: E402


class TempDirCase(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.tmp = Path(self._temp.name)

    def write(self, name: str, text: str) -> Path:
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class TokenEstimateTests(TempDirCase):
    def test_bounds_are_ordered(self) -> None:
        for ascii_count, wide_count in [(1000, 0), (0, 1000), (500, 500)]:
            low = context_probe.estimate_tokens(ascii_count, wide_count, "low")
            estimate = context_probe.estimate_tokens(ascii_count, wide_count, "estimate")
            high = context_probe.estimate_tokens(ascii_count, wide_count, "high")
            self.assertLessEqual(low, estimate, (ascii_count, wide_count))
            self.assertLessEqual(estimate, high, (ascii_count, wide_count))

    def test_regression_ascii_estimate_tracks_measured_rate(self) -> None:
        """Measured ASCII prose and code average ~4.47 characters per token.

        The original estimator classified on `ascii / 3`, roughly 50% high, which
        promoted ordinary files a whole risk band.
        """
        characters = 100_000
        estimate = context_probe.estimate_tokens(characters, 0, "estimate")
        measured = characters / 4.47
        self.assertLess(
            abs(estimate - measured) / measured,
            0.25,
            f"estimate {estimate} strays >25% from measured {measured:.0f}",
        )

    def test_regression_wide_text_is_not_forced_to_extreme(self) -> None:
        """CJK measured ~0.89 tokens/char; 10.8k characters is ~9.6k tokens.

        Charging 2 tokens per non-ASCII character banded that as `extreme`,
        whose documented action is to stop and ask the owner.
        """
        path = self.write("cjk.md", "这是一个测试文档。" * 1200)
        risk = context_probe.inspect_file(path)
        self.assertEqual(risk.risk, "high")
        self.assertLessEqual(risk.token_low, 9_600)
        self.assertGreaterEqual(risk.token_high, 9_600)

    def test_ascii_document_range_contains_truth(self) -> None:
        path = self.write("ascii.md", "word " * 4000)
        risk = context_probe.inspect_file(path)
        self.assertLessEqual(risk.token_low, 4_001)
        self.assertGreaterEqual(risk.token_high, 4_001)


class ClassifyTests(unittest.TestCase):
    def test_single_file_bands(self) -> None:
        self.assertEqual(context_probe.classify(1)[0], "low")
        self.assertEqual(context_probe.classify(context_probe.LOW_TOKEN_LIMIT)[0], "low")
        self.assertEqual(context_probe.classify(context_probe.LOW_TOKEN_LIMIT + 1)[0], "medium")
        self.assertEqual(context_probe.classify(context_probe.MEDIUM_TOKEN_LIMIT + 1)[0], "high")
        self.assertEqual(context_probe.classify(context_probe.HIGH_TOKEN_LIMIT + 1)[0], "extreme")

    def test_regression_batch_uses_its_own_scale(self) -> None:
        """A batch competes for the context window, not the single-file budget.

        Scanning eleven small documents totalled ~7.5k tokens and reported
        `TOTAL high [chunk; justify full read]` while every file in it was
        individually low or medium.
        """
        total = 7_500
        self.assertEqual(context_probe.classify(total)[0], "medium")
        self.assertEqual(context_probe.classify_batch(total)[0], "low")

    def test_batch_still_escalates_when_genuinely_large(self) -> None:
        self.assertEqual(
            context_probe.classify_batch(context_probe.BATCH_HIGH_TOKEN_LIMIT + 1)[0],
            "extreme",
        )


class RetrievalTests(TempDirCase):
    def test_tail_preserves_line_order(self) -> None:
        path = self.write("log.md", "".join(f"line {n}\n" for n in range(1, 51)))
        _header, recent, total = context_probe.read_tail(path, 5, 0)
        self.assertEqual(total, 50)
        self.assertEqual([n for n, _ in recent], [46, 47, 48, 49, 50])

    def test_bound_lines_keeps_newest_when_truncating(self) -> None:
        lines = [(n, f"{'x' * 50}\n") for n in range(1, 21)]
        selected, truncated = context_probe.bound_lines(lines, 160)
        self.assertTrue(truncated)
        self.assertEqual(selected[-1][0], 20)
        self.assertEqual(selected, sorted(selected))

    def test_binary_detection(self) -> None:
        path = self.tmp / "blob.bin"
        path.write_bytes(b"\x00\x01\x02binary\x00")
        self.assertTrue(context_probe.is_probably_binary(path))
        self.assertEqual(context_probe.inspect_file(path).risk, "binary")


class CompactCheckTests(TempDirCase):
    def run_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "compact_check.py"), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_pass_is_terse_and_quiet_is_silent(self) -> None:
        done = self.run_check("--name", "ok", "--", sys.executable, "-c", "print('x')")
        self.assertEqual(done.returncode, 0)
        self.assertIn("PASS ok", done.stdout)
        quiet = self.run_check("--name", "ok", "--quiet", "--", sys.executable, "-c", "print('x')")
        self.assertEqual(quiet.stdout.strip(), "")

    def test_failure_propagates_code_and_bounds_output(self) -> None:
        script = "import sys; [print('noise %d' % i) for i in range(500)]; sys.exit(7)"
        done = self.run_check("--name", "loud", "--", sys.executable, "-c", script)
        self.assertEqual(done.returncode, 7)
        self.assertIn("FAIL loud", done.stdout)
        self.assertLess(len(done.stdout), 9_000, "failure tail must stay bounded")
        self.assertIn("noise 499", done.stdout, "newest output must survive truncation")

    def test_regression_shell_mode_runs_pipelines(self) -> None:
        """`--shell` was absent, so the README's own `./gradlew` example could
        not launch and no pipeline or shell builtin was runnable at all."""
        done = self.run_check("--name", "pipe", "--shell", "--", "echo hi")
        self.assertEqual(done.returncode, 0, done.stdout)

    def test_launch_failure_suggests_shell(self) -> None:
        done = self.run_check("--name", "missing", "--", "./definitely-not-here")
        self.assertEqual(done.returncode, 127)
        self.assertIn("--shell", done.stdout)

    def test_timeout_reports_124(self) -> None:
        done = self.run_check(
            "--name", "slow", "--timeout-seconds", "1",
            "--", sys.executable, "-c", "import time; time.sleep(30)",
        )
        self.assertEqual(done.returncode, 124)
        self.assertIn("timeout", done.stdout)

    def test_prune_logs_keeps_newest(self) -> None:
        for index in range(10):
            (self.tmp / f"{index:02d}.log").write_text("x", encoding="utf-8")
        compact_check.prune_logs(self.tmp, 3)
        self.assertEqual(len(list(self.tmp.glob("*.log"))), 3)


class SizeRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handoffs = ROOT / "docs" / "handoffs"

    def limit(self, relative: str) -> int:
        return validate_handoffs.size_limit(self.handoffs / relative, self.handoffs)

    def test_regression_documented_rollover_names_get_history_budget(self) -> None:
        """HISTORY.md tells authors to continue in `HISTORY/<year>.md` and
        BRANCH_HISTORY.md to start numbered segments. Both landed on the 6,000
        handoff cap, so following the instructions failed validation."""
        history = validate_handoffs.HISTORY_MAX_CHARACTERS
        self.assertEqual(self.limit("HISTORY.md"), history)
        self.assertEqual(self.limit("HISTORY/2026.md"), history)
        self.assertEqual(self.limit("main.history.md"), history)
        self.assertEqual(self.limit("main.history.2.md"), history)
        self.assertEqual(self.limit("feature/foo.history.3.md"), history)

    def test_handoffs_and_policy_documents_keep_their_budgets(self) -> None:
        self.assertEqual(
            self.limit("feature/foo.md"), validate_handoffs.HANDOFF_MAX_CHARACTERS
        )
        self.assertEqual(
            self.limit("MASTER_HANDOFF.md"), validate_handoffs.POLICY_MAX_CHARACTERS
        )
        self.assertEqual(
            self.limit("MODEL_ROUTING.md"), validate_handoffs.POLICY_MAX_CHARACTERS
        )
        self.assertEqual(
            self.limit("templates/BRANCH_HANDOFF.md"),
            validate_handoffs.POLICY_MAX_CHARACTERS,
        )

    def test_entry_point_budgets_cover_shipped_shims(self) -> None:
        for shim in ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md"]:
            self.assertIn(shim, validate_handoffs.ENTRYPOINT_LIMITS)

    def test_shim_budgets_match_documented_limit(self) -> None:
        for shim, limit in validate_handoffs.ENTRYPOINT_LIMITS.items():
            if shim == "AGENTS.md":
                continue
            self.assertEqual(limit, 600, f"{shim} must match the documented shim budget")


class ShimConsistencyTests(unittest.TestCase):
    """Every per-tool entry point must redirect, never restate.

    Tool-specific files take precedence over AGENTS.md in clients that read
    both. A shim that carried its own copy of the rules would therefore win
    over the authoritative file and silently go stale.
    """

    def shims(self) -> list[tuple[str, int]]:
        return [
            (relative, limit)
            for relative, limit in validate_handoffs.ENTRYPOINT_LIMITS.items()
            if relative != "AGENTS.md"
        ]

    def present_shims(self) -> list[tuple[Path, int]]:
        found = [(ROOT / rel, limit) for rel, limit in self.shims() if (ROOT / rel).is_file()]
        self.assertTrue(found, "no shims found on disk; ROOT resolution is wrong")
        return found

    def test_every_shim_points_at_agents_md(self) -> None:
        for path, _limit in self.present_shims():
            text = path.read_text(encoding="utf-8")
            self.assertIn(
                "AGENTS.md", text, f"{path.name} does not redirect to AGENTS.md"
            )

    def test_no_shim_restates_the_rules(self) -> None:
        for path, limit in self.present_shims():
            text = path.read_text(encoding="utf-8")
            self.assertLess(len(text), limit, f"{path} exceeds its {limit}-character budget")
            body = [line for line in text.splitlines() if line.strip()]
            self.assertLessEqual(
                len(body), 6, f"{path} looks like a ruleset, not a pointer"
            )

    def test_shim_budgets_are_uniform(self) -> None:
        for relative, limit in self.shims():
            self.assertEqual(
                limit,
                validate_handoffs.SHIM_LIMIT,
                f"{relative} deviates from the shared shim budget",
            )

    def test_readme_documents_every_registered_shim(self) -> None:
        """A shim nobody can find is a shim nobody maintains."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        # assertTrue, not assertIn: a miss on an 8 KB haystack would dump the
        # whole README into the failure output.
        missing = [rel for rel, _ in self.shims() if rel not in readme]
        self.assertFalse(
            missing, f"registered but absent from README.md: {', '.join(missing)}"
        )

    def test_agents_md_is_the_only_authoritative_file(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertGreater(
            len(agents),
            validate_handoffs.SHIM_LIMIT,
            "AGENTS.md is shim-sized; the rules may have been moved out of it",
        )

    def test_agents_md_routes_formal_plans_to_model_policy(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("MODEL_ROUTING.md", agents)
        self.assertIn("runtime provider/model", agents)


class IndexRowTests(unittest.TestCase):
    def match(self, row: str):
        return validate_handoffs.INDEX_ROW.match(row)

    def test_regression_link_text_is_not_contractual(self) -> None:
        """The regex demanded literally `handoff`/`main.md` and lowercase
        `history`. Any other wording dropped the branch from the index and
        surfaced as a confusing 'missing from active index' error."""
        rows = [
            "| `main` | Integration | [main.md](main.md) | [history](main.history.md) |",
            "| `feature/foo` | Feature | [handoff](feature/foo.md) | [history](feature/foo.history.md) |",
            "| `feature/foo` | Feature | [feature/foo.md](feature/foo.md) | [History](feature/foo.history.md) |",
            "| `fix/bar` | Fix | [current](fix/bar.md) | [milestones](fix/bar.history.md) |",
        ]
        for row in rows:
            self.assertIsNotNone(self.match(row), row)

    def test_branch_and_targets_are_captured(self) -> None:
        found = self.match(
            "| `feature/foo` | Feature | [handoff](feature/foo.md) | [history](feature/foo.history.md) |"
        )
        assert found is not None
        self.assertEqual(found.group("branch"), "feature/foo")
        self.assertEqual(found.group("handoff"), "feature/foo.md")
        self.assertEqual(found.group("history"), "feature/foo.history.md")

    def test_non_rows_are_ignored(self) -> None:
        self.assertIsNone(self.match("| Branch | Role | Handoff | History |"))
        self.assertIsNone(self.match("|---|---|---|---|"))


class DocumentationIsolationTests(TempDirCase):
    """Examples must not be mistaken for live content.

    Documenting the index row format in the index itself made the validator
    parse the example as a real branch and resolve its sample links against the
    filesystem, inventing a branch that does not exist.
    """

    def test_fenced_example_row_is_not_an_active_branch(self) -> None:
        handoffs = self.tmp / "docs" / "handoffs"
        handoffs.mkdir(parents=True)
        (handoffs / "README.md").write_text(
            "| `main` | Integration | [handoff](main.md) | [history](main.history.md) |\n"
            "\n## Row format\n\n"
            "```markdown\n"
            "| `feature/example` | Feature | [handoff](feature/example.md) "
            "| [history](feature/example.history.md) |\n"
            "```\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        entries = validate_handoffs.parse_index(handoffs, errors)
        self.assertEqual(sorted(entries), ["main"])
        self.assertEqual(errors, [])

    def test_links_in_examples_are_not_resolved(self) -> None:
        path = self.write(
            "TEMPLATE.md",
            "Real: [ok](TEMPLATE.md)\n"
            "<!-- Example: [history](does-not-exist.history.md) -->\n"
            "```markdown\n[handoff](also-missing.md)\n```\n",
        )
        errors: list[str] = []
        validate_handoffs.validate_links([path], errors)
        self.assertEqual(errors, [])

    def test_broken_links_in_real_prose_still_fail(self) -> None:
        path = self.write("DOC.md", "See [gone](no-such-file.md).\n")
        errors: list[str] = []
        validate_handoffs.validate_links([path], errors)
        self.assertEqual(len(errors), 1)


class ArchivePairTests(TempDirCase):
    def archive_errors(self, names: list[str]) -> list[str]:
        # Fresh root per call so cases in one test cannot seed each other.
        root = self.tmp / f"case{len(list(self.tmp.iterdir()))}"
        handoffs = root / "docs" / "handoffs"
        (handoffs / "archive").mkdir(parents=True)
        for name in names:
            path = handoffs / "archive" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x", encoding="utf-8")
        errors: list[str] = []
        validate_handoffs.validate_archive_pairs(root, handoffs, errors)
        return errors

    def test_regression_numbered_segments_pair_with_their_branch(self) -> None:
        """Pairing derived the peer by string surgery, so a numbered segment
        demanded `foo.history.2.history.md` and always failed."""
        self.assertEqual(
            self.archive_errors(
                ["feature/foo.md", "feature/foo.history.md", "feature/foo.history.2.md"]
            ),
            [],
        )

    def test_plain_pair_passes(self) -> None:
        self.assertEqual(self.archive_errors(["fix/bar.md", "fix/bar.history.md"]), [])

    def test_unpaired_files_are_reported(self) -> None:
        self.assertTrue(self.archive_errors(["fix/bar.md"]))
        self.assertTrue(self.archive_errors(["fix/bar.history.md"]))


class PlaceholderTests(TempDirCase):
    def placeholder_errors(self, name: str, text: str) -> list[str]:
        handoffs = self.tmp / "docs" / "handoffs"
        path = handoffs / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        errors: list[str] = []
        validate_handoffs.validate_no_placeholders(self.tmp, handoffs, [path], errors)
        return errors

    def test_unfilled_branch_record_is_flagged(self) -> None:
        self.assertTrue(self.placeholder_errors("main.md", "Next action\n\n`<One action>`\n"))
        self.assertTrue(self.placeholder_errors("main.history.md", "### YYYY-MM-DD — init\n"))

    def test_filled_record_passes(self) -> None:
        self.assertEqual(
            self.placeholder_errors("main.md", "## Next action\n\nRun the migration.\n"), []
        )

    def test_policy_syntax_and_fenced_examples_are_not_placeholders(self) -> None:
        """`<branch>` in command syntax and dated examples inside fences are
        documentation, not unfilled fields."""
        self.assertEqual(
            self.placeholder_errors("REPOSITORY.md", "Use `feature/<purpose>`\n"), []
        )
        self.assertEqual(
            self.placeholder_errors(
                "HISTORY.md", "Format:\n\n```markdown\n### YYYY-MM-DD — `x`\n- Tip: `<sha>`\n```\n"
            ),
            [],
        )
        self.assertEqual(
            self.placeholder_errors("main.history.md", "<!-- ### YYYY-MM-DD — example -->\n"), []
        )


class EndToEndTests(unittest.TestCase):
    def test_kit_validates_clean(self) -> None:
        done = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_handoffs.py"), "--quiet"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_scan_reports_batch_band(self) -> None:
        done = subprocess.run(
            [
                sys.executable, str(SCRIPTS / "context_probe.py"), "scan",
                str(ROOT / "AGENTS.md"), str(ROOT / "README.md"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("TOTAL low", done.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
