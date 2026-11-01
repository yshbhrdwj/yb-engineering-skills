#!/usr/bin/env python3
"""Summarize saved eval arms, excluding incomplete or mismatched evidence.

Input: <case>/eval_metadata.json, <case>/<arm>/{grading,timing}.json,
transcript.md, outputs/. Optional run_metadata.json pins comparison settings.
Output never includes prompts, assertions, transcript text, or source paths.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

COMPARISON_KEYS = ("host", "model", "effort", "harness_revision", "fixture_revision", "tool_policy")


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def load_arm(folder):
    """A grade is usable only with nonempty transcript/output and real assertions."""
    result = {"usable": False, "reason": None}
    transcript = folder / "transcript.md"
    outputs = folder / "outputs"
    if not transcript.is_file() or not transcript.stat().st_size:
        result["reason"] = "missing transcript"
        return result
    if not outputs.is_dir() or not any(p.is_file() and p.stat().st_size for p in outputs.rglob("*")):
        result["reason"] = "missing output"
        return result
    grade = read_json(folder / "grading.json")
    expectations = grade.get("expectations") if isinstance(grade, dict) else None
    if not isinstance(expectations, list) or not expectations:
        result["reason"] = "missing or invalid grade"
        return result
    checks = {}
    for item in expectations:
        if not isinstance(item, dict) or not isinstance(item.get("text"), str) or not item["text"].strip() or type(item.get("passed")) is not bool:
            result["reason"] = "invalid assertion"
            return result
        if item["text"] in checks:
            result["reason"] = "duplicate assertion"
            return result
        checks[item["text"]] = item["passed"]
    result.update(usable=True, checks=checks, passed=sum(checks.values()), total=len(checks))
    timing = read_json(folder / "timing.json")
    timing = timing if isinstance(timing, dict) else {}
    tokens = timing.get("total_tokens")
    seconds = timing.get("total_duration_seconds")
    if seconds is None and number(timing.get("duration_ms")):
        seconds = timing["duration_ms"] / 1000
    result["tokens"] = tokens if number(tokens) else None
    result["seconds"] = seconds if number(seconds) else None
    metadata = read_json(folder / "run_metadata.json")
    result["metadata"] = metadata if isinstance(metadata, dict) else {}
    return result


def summarize(workspace, baseline="old_skill", anonymous=False):
    cases = sorted(p for p in Path(workspace).iterdir() if p.is_dir() and (p / "eval_metadata.json").is_file())
    result = {"cases": len(cases), "registered_runs": 0, "grading_files": 0, "pairs": 0,
              "metadata_matched_pairs": 0, "new": {"passed": 0, "total": 0},
              "baseline": {"passed": 0, "total": 0}, "token_pairs": 0, "time_pairs": 0,
              "recorded_tokens": {"new": 0, "baseline": 0}, "recorded_seconds": {"new": 0, "baseline": 0},
              "excluded": [], "interpretation": "Descriptive saved-run summary; not proof of a causal improvement or host integration."}
    runs = Path(workspace) / "runs.tsv"
    if runs.is_file():
        result["registered_runs"] = sum(bool(line.strip()) for line in runs.read_text().splitlines())
    for index, case in enumerate(cases, 1):
        result["grading_files"] += sum((case / arm / "grading.json").is_file() for arm in ("with_skill", "old_skill", "without_skill"))
        label = f"case-{index:02d}" if anonymous else case.name
        if not (case / baseline).is_dir():
            result["excluded"].append({"case": label, "reason": "requested baseline absent"})
            continue
        new, old = load_arm(case / "with_skill"), load_arm(case / baseline)
        if not new["usable"] or not old["usable"]:
            result["excluded"].append({"case": label, "reason": "new: " + str(new["reason"]) + "; baseline: " + str(old["reason"])})
            continue
        if new["checks"].keys() != old["checks"].keys():
            result["excluded"].append({"case": label, "reason": "assertions differ"})
            continue
        metadata = [new["metadata"], old["metadata"]]
        mismatch = any(key in metadata[0] and key in metadata[1] and metadata[0][key] != metadata[1][key] for key in COMPARISON_KEYS)
        if mismatch:
            result["excluded"].append({"case": label, "reason": "comparison metadata differs"})
            continue
        result["pairs"] += 1
        if all(all(key in m and m[key] not in (None, "") for key in COMPARISON_KEYS) for m in metadata):
            result["metadata_matched_pairs"] += 1
        for name, arm in (("new", new), ("baseline", old)):
            for key in ("passed", "total"):
                result[name][key] += arm[key]
        for field, target, count in (("tokens", "recorded_tokens", "token_pairs"), ("seconds", "recorded_seconds", "time_pairs")):
            if new[field] is not None and old[field] is not None:
                result[count] += 1
                result[target]["new"] += new[field]
                result[target]["baseline"] += old[field]
    for metric in ("recorded_tokens", "recorded_seconds"):
        values = result[metric]
        values["change_percent"] = ((values["new"] / values["baseline"] - 1) * 100) if values["baseline"] else None
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--baseline", choices=("old_skill", "without_skill"), default="old_skill")
    parser.add_argument("--anonymous", action="store_true", help="Replace case names with numbered labels")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not args.workspace.is_dir():
        parser.error("workspace must be an existing directory")
    output = json.dumps(summarize(args.workspace, args.baseline, args.anonymous), indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
