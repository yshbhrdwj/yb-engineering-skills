# Historical evaluation audit — 1 November 2026

This is a sanitized audit of interrupted private trials of the earlier draft. It does **not** score the revised skills committed with this report. Raw prompts, project code, personal paths, transcripts, and application-specific design documents are intentionally excluded from this public repository.

## Evidence recovered

The saved workspace contained 20 cases and 40 registered run arms: 18 new-versus-old comparisons and two new-versus-no-skill comparisons. It contained 38 grades and 38 compact transcripts. One architecture pair had no grades; the old arm lacked a saved transcript and timing. One no-skill merge arm had a grade based entirely on missing output rather than observed behavior.

The raw session logs still contained both missing transcripts and final reports. These were reconstructed into a separate private audit copy without modifying the original workspace. Their provenance is retained privately. The recovered merge report shows the no-skill runner also correctly stopped on an already-merged PR, so the original apparent 3-to-0 advantage reflected missing evidence. The architecture runners produced design artifacts, but a worktree guard affected saving; the old arm worked around that guard. Those runs need an environment-equivalent replay before treating their saving behavior as a skill-quality difference. Recovered model-usage records were not substituted into the original timing metric because they use a different accounting boundary.

## Descriptive result from complete saved old/new pairs

| Measure | New draft | Old skills |
| --- | ---: | ---: |
| Complete graded pairs | 17 | 17 |
| Assertions passed | 57 / 69 | 58 / 69 |
| Recorded tokens | 1,735,315 | 1,665,212 |
| Sum of recorded run time | 2,432.0 s | 2,303.9 s |

The new draft used 4.21% more recorded tokens and 5.56% more summed run time in these pairs. These data do not establish an accuracy or speed gain. Summed run time is not end-to-end wall-clock completion time for parallel runs.

## Limits that prevent a causal claim

- One sample per arm and case; small project-specific task set.
- No Ponytail comparison arm or length-matched context control. Ponytail instructions were reportedly injected into both conditions.
- The runs manually loaded instructions; they did not verify automatic selection, frontmatter, hooks, or reviewer isolation.
- No complete pinned model/effort/harness metadata accompanied the saved arms. All 17 pairs lack the full comparison metadata required by the new protocol.
- Compact tool transcripts truncated some inputs and outputs. Graders could see arm names despite a stated intent to blind them.
- Several assertions reward report length or checklist wording rather than discriminating task outcomes. Some failed checks describe missing evidence rather than shown defects.

The public [behavioral catalog](../../evals/README.md) replaces those weaknesses with synthetic tasks, outcome assertions, pinned-run requirements, and explicit missing-evidence handling. The aggregator's tests verify accounting and inclusion rules; they do not prove the skills' reasoning quality. No superiority claim is made.
