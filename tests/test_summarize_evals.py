"""Test evidence inclusion rules with synthetic run artifacts."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("summarize_evals", Path(__file__).resolve().parents[1] / "scripts/summarize_evals.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SummarizeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.case = self.root / "private-case-name"
        self.case.mkdir()
        (self.case / "eval_metadata.json").write_text('{"prompt":"private prompt"}')
        for arm in ("with_skill", "old_skill"):
            folder = self.case / arm
            (folder / "outputs").mkdir(parents=True)
            (folder / "outputs/report.md").write_text("private report")
            (folder / "transcript.md").write_text("private transcript")
            self.write(arm, "grading.json", {"expectations": [{"text": "private assertion", "passed": arm == "with_skill"}], "summary": {"passed": 999}})
            self.write(arm, "timing.json", {"total_tokens": 120 if arm == "with_skill" else 100, "duration_ms": 900 if arm == "with_skill" else 1000})

    def write(self, arm, file, value):
        (self.case / arm / file).write_text(json.dumps(value))

    def test_counts_use_assertions_not_untrusted_summary(self):
        result = MODULE.summarize(self.root)
        self.assertEqual(result["pairs"], 1)
        self.assertEqual(result["new"], {"passed": 1, "total": 1})
        self.assertEqual(result["baseline"], {"passed": 0, "total": 1})
        self.assertAlmostEqual(result["recorded_tokens"]["change_percent"], 20)
        self.assertAlmostEqual(result["recorded_seconds"]["change_percent"], -10)
        self.assertEqual(result["metadata_matched_pairs"], 0)

    def test_missing_transcript_excludes_grade_not_behavior_failure(self):
        (self.case / "old_skill/transcript.md").unlink()
        result = MODULE.summarize(self.root)
        self.assertEqual(result["pairs"], 0)
        self.assertEqual(result["new"]["total"], 0)
        self.assertIn("missing transcript", result["excluded"][0]["reason"])

    def test_empty_outputs_exclude_pair(self):
        (self.case / "old_skill/outputs/report.md").write_text("")
        self.assertEqual(MODULE.summarize(self.root)["pairs"], 0)

    def test_invalid_boolean_and_duplicate_assertion_rejected(self):
        for expectations in ([{"text": "x", "passed": "false"}], [{"text": "x", "passed": True}] * 2):
            with self.subTest(expectations=expectations):
                self.write("with_skill", "grading.json", {"expectations": expectations})
                self.assertEqual(MODULE.summarize(self.root)["pairs"], 0)

    def test_mismatched_assertions_excluded(self):
        self.write("old_skill", "grading.json", {"expectations": [{"text": "other", "passed": True}]})
        self.assertIn("assertions differ", MODULE.summarize(self.root)["excluded"][0]["reason"])

    def test_mismatched_metadata_excluded_and_matched_metadata_counted(self):
        base = dict.fromkeys(MODULE.COMPARISON_KEYS, "pinned")
        self.write("with_skill", "run_metadata.json", base)
        self.write("old_skill", "run_metadata.json", {**base, "model": "other"})
        self.assertEqual(MODULE.summarize(self.root)["pairs"], 0)
        self.write("old_skill", "run_metadata.json", base)
        self.assertEqual(MODULE.summarize(self.root)["metadata_matched_pairs"], 1)

    def test_missing_or_invalid_metrics_do_not_become_zero(self):
        self.write("old_skill", "timing.json", {"total_tokens": -1, "total_duration_seconds": float("nan")})
        result = MODULE.summarize(self.root)
        self.assertEqual(result["pairs"], 1)
        self.assertEqual(result["token_pairs"], 0)
        self.assertIsNone(result["recorded_tokens"]["change_percent"])
        self.assertEqual(result["time_pairs"], 0)

    def test_anonymous_output_does_not_contain_content_or_case_name(self):
        (self.case / "old_skill/transcript.md").unlink()
        output = json.dumps(MODULE.summarize(self.root, anonymous=True))
        self.assertNotIn("private", output)

    def test_absent_requested_baseline_is_separate(self):
        result = MODULE.summarize(self.root, baseline="without_skill")
        self.assertEqual(result["pairs"], 0)
        self.assertEqual(result["excluded"][0]["reason"], "requested baseline absent")


class CatalogIntegrityTests(unittest.TestCase):
    def test_public_cases_cover_each_current_skill_with_real_fixtures(self):
        root = Path(__file__).resolve().parents[1]
        cases = json.loads((root / "evals/cases.json").read_text())["cases"]
        skills = {p.name for p in (root / "codex/skills").iterdir() if p.is_dir()}
        self.assertEqual({case["skill"] for case in cases}, skills)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        fixture_root = (root / "evals").resolve()
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            self.assertGreaterEqual(len(case["acceptance"]), 2)
            for file in case["files"]:
                fixture = (fixture_root / file).resolve()
                self.assertTrue(fixture.is_relative_to(fixture_root))
                self.assertTrue(fixture.is_file())


if __name__ == "__main__":
    unittest.main()
