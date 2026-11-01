# Behavioral checks

The ten cases in [cases.json](cases.json) are small, public, synthetic tasks. They exercise observable outcomes for every role, including a correct-code control inside the review fixture. They are separate from the private historical trials and contain no customer code or prompts.

## Run a controlled comparison

1. Pin repository/fixture revision, host and version, exact model, effort, tool policy, and timeout before starting. Use the same values in every arm. Disable unrelated skills and plugins, including Ponytail. Keep test environments and tools equivalent.
2. Copy only a case's files into a fresh temporary directory. Give each runner its `prompt`, the selected skill, and those raw files. Keep the `acceptance` rubric hidden from the runner. Do not share the author's reasoning or the baseline's answer. Code-review and security fixtures explicitly authorize synthetic local work only.
3. Run the current skill, prior skill, and no-skill control in randomized order with multiple repetitions. An irrelevant length-matched control can test context overhead. Record failed and timed-out runs; never rerun only the losers. Predeclare important failure criteria and reporting thresholds.
4. Store `<case>/<arm>/transcript.md`, nonempty `outputs/`, `grading.json`, `timing.json`, and `run_metadata.json`. Pin `host`, `model`, `effort`, `harness_revision`, `fixture_revision`, and `tool_policy` in every run's metadata. Record full commands and exits; measure elapsed time and tokens consistently at the host boundary.
5. Have a separate evaluator grade acceptance outcomes against the actual files and command results. Hide arm names and randomize identifiers. Preserve false positives, missed defects, scope changes, and uncertainty. A missing transcript is missing evidence, not a demonstrated behavioral failure. Do not grade response length as correctness.
6. Aggregate with `python3 scripts/summarize_evals.py <workspace> --anonymous`. It recomputes assertion totals, rejects mismatched assertions and known configuration differences, excludes missing evidence, and aggregates metrics only for pairs that have both measurements. Absence of metadata remains visible; descriptive output is not a causal benchmark.

A compatible grade contains `expectations`, each with a unique `text` and boolean `passed` (plus optional evidence). A timing file uses `total_tokens` and `total_duration_seconds` or `duration_ms`. Write the catalog's acceptance strings verbatim into both arms' grades.

## Interpret results

Prioritize preserved requirements, important bugs missed, false positives, and unauthorized effects. Compare speed or cost only after quality passes the predefined bar. Report both task distribution and run count. A one-off smoke check cannot establish superiority, and manually loading a skill does not validate host triggering, permissions, hook installation, or subagent isolation. Test those host integrations separately.
