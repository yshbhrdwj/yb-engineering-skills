# Behavioral checks

The ten cases in [cases.json](cases.json) are small, public, synthetic tasks. They exercise observable outcomes for every role, including a correct-code control inside the review fixture. They are separate from private historical trials and contain no customer code or prompts.

## Run a controlled comparison

1. Pin repository/fixture revision, host and version, exact model, effort, tool policy, and timeout before starting. Use the same values in every arm. Disable unrelated skills and plugins, including Ponytail, in isolated test configuration. Keep environments and tools equivalent.
2. Copy only a case's input files into a fresh temporary directory. Give each runner its `prompt`, the selected skill, and those raw files. Keep `acceptance` hidden from the runner. Do not share the author's reasoning or the baseline's answer.
3. Run current skill, prior skill, and no-skill control in randomized order with multiple repetitions. An irrelevant length-matched control can test context overhead. Preserve failed and timed-out runs; never rerun only the losers. Predeclare important failure criteria and reporting thresholds.
4. Save the artifacts in the exact layout below. Record full commands and exits. Measure elapsed time and tokens consistently at the host boundary; do not remove interrupted work from a cost measure without retaining gross cost separately.
5. Have a separate evaluator grade task outcomes against actual files and command results. Hide arm names and randomize identifiers for grading. Preserve false positives, missed defects, scope changes, and uncertainty. A missing transcript is missing evidence, not a demonstrated behavioral failure. Do not grade response length as correctness.
6. Aggregate saved pairs. The helper checks accounting and inclusion rules; it does not verify that the grader covered all task requirements or that self-reported model/tool settings were actually enforced.

## Saved-run layout

Use one flat case directory for each task and repetition. The required `eval_metadata.json` is a JSON object directly inside that directory; it marks the directory for discovery. Fields below preserve provenance but are not a runner configuration.

```text
workspace/
  task-a-rep1/
    eval_metadata.json
    with_skill/
      transcript.md
      outputs/report.md
      grading.json
      timing.json
      run_metadata.json
    old_skill/
      transcript.md
      outputs/report.md
      grading.json
      timing.json
      run_metadata.json
    without_skill/            optional third arm, same files
  task-a-rep2/                next independent repetition, same layout
  runs.tsv                    optional registration index
```

Use the arm names exactly: `with_skill` is the candidate, `old_skill` is the previous version, and `without_skill` is the no-skill control. The helper does not search nested `run-1/` folders. Instead, make `task-a-rep1`, `task-a-rep2`, etc. separate case directories. The CLI reports an error if no case markers exist; a case with incomplete artifacts is listed under `excluded`.

Example `eval_metadata.json`:

```json
{
  "eval_name": "task-a-rep1",
  "prompt": "The task given to every arm",
  "assertions": ["Default CLI output is unchanged"]
}
```

Every arm needs a nonempty `transcript.md` with the actual model/tool record, nonempty files in `outputs/`, and `grading.json`. A report alone is not an execution transcript. Include full commands, results and the final response in the record, preserving failed attempts.

Example `grading.json`:

```json
{
  "expectations": [
    {
      "text": "Default CLI output is unchanged",
      "passed": true,
      "evidence": "Captured CLI bytes matched the baseline fixture"
    }
  ]
}
```

Use unique, nonempty assertion strings and actual JSON booleans. Copy the catalog's acceptance criteria verbatim into both arms' grades; matching grades do not establish that the criteria themselves were sufficient. The helper recomputes totals from these booleans and ignores any supplied summary count.

Example `run_metadata.json`:

```json
{
  "host": "host-name@exact-version",
  "model": "exact-model-id",
  "effort": "high",
  "harness_revision": "harness-commit-or-content-hash",
  "fixture_revision": "fixture-commit-or-content-hash",
  "tool_policy": "isolated-policy-config-hash"
}
```

All six pins must be nonempty strings, identical between arms, to count in `metadata_matched_pairs`. A value mismatch or a key present in only one arm excludes the pair. Equally missing/incomplete metadata can remain in descriptive totals but is counted separately in `metadata_incomplete_pairs`; it cannot support a configuration-matched benchmark claim. These checks compare recorded pins, not the host's actual enforcement.

Optional `timing.json`:

```json
{
  "total_tokens": 1500,
  "total_duration_seconds": 12.5
}
```

`duration_ms` is also accepted when seconds are absent. Values must be finite, nonnegative numbers. Missing/invalid metrics remain unknown; only pairs with both measurements enter that metric's totals. Use the same definition of total tokens and timing boundaries in every arm; a sum of parallel run durations is not end-to-end wall time.

Optional `runs.tsv` uses `run_id`, `case_id`, `arm`, separated by tabs. That exact header is excluded from registration counts, as are blank rows. Headerless legacy indexes are accepted. Registration counts are informational and do not make an incomplete run usable.

```sh
python3 scripts/summarize_evals.py /path/to/workspace --baseline old_skill --anonymous
python3 scripts/summarize_evals.py /path/to/workspace --baseline without_skill --anonymous
```

## Interpret results

Prioritize preserved requirements, important bugs missed, false positives, and unauthorized effects. Compare speed or cost after quality passes the predefined bar. Report task distribution and run count, raw and adjusted measurements, failures, and exclusions. Three repetitions of one task do not establish reliability on other tasks or models.

A one-off smoke check cannot establish superiority. Manually loading a skill does not validate native triggering, permissions, hook installation, or subagent isolation. Test those integrations separately and name unavailable native-host coverage explicitly.
