# Behavioral checks

The cases in [cases.json](cases.json) are small, public, synthetic tasks. They exercise observable outcomes for every role, including a correct-code control inside the review fixture. They are separate from private historical trials and contain no customer code or prompts.

| Skill | Cases |
| --- | --- |
| Ten original roles | One each: the first ten cases in the file |
| `yb-frontend-engineer`, `yb-frontend-reviewer`, `yb-qa-engineer` | Sixteen web and mobile delivery cases: `fe-*`, `rev-*`, and the `qa-*` cases other than `qa-exact-boundary`, described below |
| `yb-web-design-system` | Twelve `web-design-*` cases: button spacing, type hierarchy, responsive navigation, premium landing page, SaaS dashboard, trading screen, site redesign, checkout form, modal, layout failure, cross-page consistency, greenfield system |
| `yb-mobile-design-system` | Seventeen `mobile-*` cases, described below |

The web-design fixtures under `fixtures/web-design/` are multi-file and seed real defects beside traps (correct code that looks wrong). The hidden acceptance list is the answer key: score recall of seeded defects, false positives on traps, and an efficiency outcome (mode chosen, references loaded, no invented evidence, no unrequested changes). Some keys are numeric, such as computed contrast ratios; recompute them rather than trusting a runner's arithmetic.

The seventeen `yb-mobile-design-system` cases use a synthetic Expo app in [fixtures/mobile](fixtures/mobile). They span a one-line spacing fix, typography hierarchy, a reusable component, iOS navigation, Android back and insets, a screen redesign, app-wide card drift, text scaling, high-density trading, a premium family-wellness direction, reuse of an approved design authority, a missing-device fallback, subtle craft defects, a clean control that should produce no defect, a gloved field-work form, and a mixed-age family screen. Each records its intended `mode` (1 micro to 4 system). Small cases also set `max_skill_references`, and their acceptance criteria require that no audit, playbook, or delegation runs; large cases require the analysis that efficiency must not drop. The summary helper compares two arms per workspace, so run the three baseline comparisons as separate workspaces: `old_skill` is `yb-frontend-engineer` in one and the UI/UX Pro Max-assisted workflow in another, and `without_skill` is the no-skill control. Count reference files and tool calls from transcripts, not from self-reports. `mobile-seeded-app-audit` is the discriminating case: a six-file app with 13 `seeded_defects` and three `traps` that look wrong but are correct. Score recall (seeded defects reported), false positives (traps reported, or factually wrong claims), and whether contrast was computed; valid extra findings are not false positives.

The sixteen frontend delivery cases (`fe-*`, `rev-*`, and `qa-*` for web and mobile) use [fixtures/frontend](fixtures/frontend): a Next.js app, an Expo app, a web-plus-Expo monorepo, and a runnable transfer module. Engineer cases record the intended `path` (fast, standard, comprehensive) and reviewer cases a `review_mode`; fast cases set `max_skill_references`. Each case pairs a quality outcome with an efficiency or honesty outcome, such as staying on the fast path, not loading an absent design authority, or claiming no simulator evidence. The three reviewer cases carry `seeded_defects` and `traps`; score them like the mobile audit. `qa-critical-transfer` runs with `node --test`; the defects were confirmed by direct execution on 2026-11-02, not by a model run.

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
