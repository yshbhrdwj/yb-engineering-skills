# Independent-review evidence audit — 1 November 2026

The submitted review contains useful, reproducible tooling findings. Its benchmark conclusions require narrower wording and several corrections. This audit read the submitted dataset, trial manifest, saved source artifacts and all 18 completed full model/tool logs. No model-backed evaluation was rerun. Original reports and logs were preserved; private paths, prompts, source and conversation identifiers are not copied here.

## What the records support

The benchmark contains two tasks with three repetitions in each of three arms: candidate instructions, previous instructions, and no-skill control. These are Gemini/Antigravity sessions manually reading skill files, rather than native Claude Code or Codex executions. The captured planner records expose token counts and tool activity but do not independently establish the exact model/effort pins reported in the summary. Native-host permissions, triggering, browser access and reviewer isolation therefore remain separate questions.

For the implementation task, an isolated probe of the saved pure calculation functions confirmed numeric-string compatibility in all three candidate artifacts and one of three previous-version artifacts. The same probe succeeded in all three no-skill artifacts. The submitted dataset incorrectly marks the third no-skill artifact as losing that compatibility, although its function still converts the numeric fields with `int()` and returns the expected result. This is a narrow contract check, not proof of universal backward compatibility.

Candidate gross output tokens on that task average 19,879.7 versus 28,801.3 for the previous instructions: 30.98% fewer in these three recorded trials. The corresponding mean elapsed times are 317.7 and 338.7 seconds. The no-skill control averages 222.0 seconds and 16,676.7 output tokens. These observations do not establish a general advantage over the no-skill control, other tasks/models, or Ponytail.

For the review task, submitted grades report all four planted defects and no finding on the clean-code control in every arm. This audit checked the saved records and accounting, rather than performing a new blinded recall/false-positive evaluation. One explicit fixture with four named contracts cannot establish general reviewer recall.

## Measurements that do not reconcile

All 18 submitted elapsed totals match first-to-last timestamps in the current full logs. Several other values differ:

| Record | Submitted value | Current full-record check |
| --- | --- | --- |
| First previous-version implementation trial, cache-read tokens | 522,381 | 512,381 |
| Second previous-version review trial, gross output tokens | 35,386 | 39,877 |
| Same review trial, input / cache-read tokens | 81,367 / 194,881 | 87,589 / 256,641 |
| Third candidate review trial, startup plus workspace phases | 12 + 334 = 346 seconds | Recorded total is 416 seconds; 70 seconds are unallocated |

The review task's roughly 7% adjusted-output reduction consequently does not reconcile with the current full logs. Applying the submitted interruption-subtraction convention to those logs would give about 10.9%; this audit does not promote either adjusted number as a validated cost estimate. Gross tokens include interrupted attempts and must remain visible. The service accounting boundary, phase definition and transcript snapshots need reconciliation before publishing a precise aggregate cost claim.

The trials overlapped in time, encountered stream interruptions, and include a reported command-queue delay. Summed run durations are not experiment wall time. Three repetitions per arm/task provide descriptive observations, not a robust effect estimate. Later tasks stopped at an API quota limit; they are missing coverage, not successful role tests.

## Review dispositions that require care

- The actual suite contains product strategist, solution architect and security/privacy roles. `yb-product-architect` is not a current skill. The submitted scorecard mixes retired roles into its claimed ten-role coverage and omits current ones.
- A recommendation to re-enable CI conflicts with the user's explicit instruction to disable it. Local validation remains available; no CI re-enable is implied by remediation.
- The repository already disclaims measured superiority over Ponytail. A claim that its current documentation promises such superiority is unsupported.
- Claude's `allowed-tools` is a permission pre-approval mechanism, not a restrictive tool allowlist, as described in the [official skill reference](https://code.claude.com/docs/en/skills). It cannot supply the proposed non-mutation guarantee. Implicit skill selection also does not itself authorize a merge or deployment; invocation policy and action authorization are distinct controls.
- The current Stop implementation has no PID-stamped lock directory. Its cache and concurrency behavior should be reviewed from the actual implementation rather than that reported mechanism.

## Evaluation-helper remediation

The saved-run aggregator now excludes asymmetric comparison metadata instead of admitting an incompletely pinned arm alongside a fully pinned one. Equally incomplete historical metadata remains explicitly descriptive, with a separate incomplete-pair count. Full matching pins require nonempty strings; this still verifies recorded configuration only.

The helper excludes the documented TSV header from registration counts, rejects malformed case markers, and gives a clear CLI error when the required `eval_metadata.json` case markers are missing. The [run guide](../../evals/README.md) now documents exact arm names, file schemas and one flat case directory per repetition. Regression tests exercise these failures; they do not validate model reasoning or the sufficiency of grading criteria.

The implementation-task output reduction is a useful lead for further controlled testing. The evidence does not support treating the entire suite as universally faster, more accurate, natively validated in both hosts, or ready merely because its prose was shortened.
