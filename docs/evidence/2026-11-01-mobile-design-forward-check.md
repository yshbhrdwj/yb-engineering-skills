# Mobile design system forward check — 1 November 2026

A matched two-arm smoke comparison of `yb-mobile-design-system` against a no-skill control on four of the twelve public [mobile cases](../../evals/cases.json). It establishes specific observed behavior and one sample of cost. It is not a repeated, blinded benchmark, and it does not show a quality or speed advantage.

## Setup

- Cases: `mobile-micro-icon-gap` (mode 1), `mobile-reuse-approved-authority` (mode 2), `mobile-full-app-cards` (mode 4), `mobile-no-device-fallback` (mode 3).
- Arms: `with_skill` (Claude Code edition, `SKILL.md` SHA-256 `ef3417e4…ca5e`, base commit `4fd5548` plus uncommitted skill files) and `without_skill`. One run per case and arm, all eight launched in parallel as fresh general-purpose subagents with the same inherited model and effort.
- Each runner received only the case prompt and its fixture files in its own temporary directory; the skill arm also received the skill folder. Acceptance criteria were hidden from runners.
- Tokens, tool calls, and duration come from the host's per-subagent usage report. Reference loading comes from each runner's self-reported file list, not a transcript audit.
- Grading was done by the skill author against the catalog assertions, not blinded. Contrast ratios cited by runners were recomputed independently and matched.

## Results

| Case | Arm | Assertions | Skill references read | Tokens | Tool calls | Seconds |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| micro icon gap | with skill | 4 / 4 | 0 | 71,715 | 7 | 35.9 |
| micro icon gap | without | 4 / 4 | — | 69,108 | 6 | 33.2 |
| reuse authority | with skill | 4 / 4 | 3 (sections) | 88,315 | 9 | 152.6 |
| reuse authority | without | 4 / 4 | — | 73,336 | 5 | 78.6 |
| card drift audit | with skill | 4 / 4 | 3 | 86,946 | 7 | 114.3 |
| card drift audit | without | 4 / 4 | — | 73,318 | 4 | 69.1 |
| no-device fallback | with skill | 4 / 4 | 3 | 84,939 | 9 | 86.3 |
| no-device fallback | without | 4 / 4 | — | 70,519 | 5 | 45.8 |
| **Total** | with skill | **16 / 16** | | **331,915** | **32** | **389.0** |
| **Total** | without | **16 / 16** | | **286,281** | **20** | **226.7** |

The skill arm used 15.9% more tokens, 60% more tool calls, and 72% more summed subagent time. Summed durations of parallel runs are not end-to-end wall time.

## Observations

- **Routing worked for the micro task.** The skill arm loaded no reference, made a one-line token change (`marginEnd: gap.inlineIcon`), and reported in a few lines. The overhead was about 2,600 tokens, consistent with loading the entrypoint.
- **The rubric did not discriminate.** Both arms met every assertion. Four assertions per case are too coarse for a capable baseline model on small synthetic fixtures.
- **Beyond the rubric, the skill arm found more.** In the card audit it reported that `GoalCard`'s `#6B7280` on `#F5F7F6` is 4.49:1, below the 4.5:1 text minimum, and named the non-concentric nested radius explicitly; the control reported the radius only as a rule violation and missed the contrast failure. In the reuse case it flagged that `color.border` field outlines (about 1.4:1) fail non-text contrast and gave reorder accessibility actions. These are single observations, not established recall differences.
- **One labeling error.** The no-device skill run labeled "dark mode is ignored" as **Required**; supporting dark appearance is not a platform requirement. The entrypoint now limits **Required** to claims with a named criterion.
- **Reference loading exceeded need.** Three runs read three references although the fixtures' authority and code settled most decisions. The entrypoint now says to read a reference only for a decision the authority, code, and context do not settle. This revision has not been rerun.
- Runners could not write report files (the host blocks subagent report writes), so responses were graded from their returned text.

## Refinement rerun

After the first run, the skill was refined: an entrypoint that reads references only for unsettled decisions and limits **Required** to failed criteria; new direction, adaptive-layout, and audit/QA references; deeper typography, color, component, flow, platform, and source coverage; and four new cases, including a subtle-craft fixture and a clean control. Three cases were then rerun once per arm with the same setup (refined `SKILL.md` SHA-256 prefix `8cb7580c`).

| Case | Arm | Result | Skill references read | Tokens | Tool calls | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: |
| subtle craft defects | with skill | 6 / 6 | 3 (sections) | 78,892 | 7 | 71.0 |
| subtle craft defects | without | 6 / 6 | — | 69,328 | 3 | 36.8 |
| clean control | with skill | see below | 1 (sections) plus heading searches | 77,702 | 7 | 77.3 |
| clean control | without | see below | — | 70,311 | 3 | 49.4 |
| no-device fallback | with skill | 4 / 4 | 1 (sections) | 74,786 | 6 | 50.8 |
| no-device fallback | without | 4 / 4 | — | 69,355 | 3 | 34.8 |
| **Total** | with skill | | | **231,380** | **20** | **199.2** |
| **Total** | without | | | **208,994** | **9** | **121.0** |

- **No measurable quality difference.** Both arms found all six seeded craft defects and the same extra issues.
- **The clean control was not clean.** Both arms independently found a real defect: the value's natural width can squeeze the `flex: 1` title to nothing at long values or large text. The fixture's first assertion was therefore invalid for this run. The fixture now caps the value at half the row. Only the skill arm labeled the finding's strength, tradeoff, and retest.
- **Reference loading improved.** On the repeated no-device case the skill arm read one reference section instead of three files, and tokens fell from 84,939 to 74,786. The skill still cost 10.7% more tokens than the control across these three cases.
- **Label discipline is still imperfect.** The no-device skill run called missing dark-theme support "Required for this request" and a 30 pt target "Required", although 30 pt passes WCAG 2.5.8. The entrypoint and finding format now define Required as a named criterion that is actually failed and show how to split such findings. This change has not been rerun.
- Grading was again by the author, without blinding.

## Discriminating round

The skill was rebuilt around a mandatory review procedure (static sweep, computed contrast, finding gate with authority exceptions checked first), a shorter entrypoint, a Mode 4 checkpoint after the direction brief, and a stricter **Required** rule. A new case, `mobile-seeded-app-audit`, gives six files with 13 seeded defects and three traps (correct code that looks suspicious). Each arm ran twice; refined `SKILL.md` SHA-256 prefix `2772e561`.

| Run | Seeded defects found | Traps reported | Contrast | Tokens | Tool calls | Seconds |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| with skill, rep 1 | 13 / 13 | 0 | computed | 98,181 | 8 | 150.9 |
| with skill, rep 2 | 13 / 13 | 0 | computed | 100,183 | 5 | 154.3 |
| without, rep 1 | 13 / 13 | 0 | stated as "about 3.9:1" | 75,984 | 3 | 64.0 |
| without, rep 2 | 12 / 13 | 0 | computed | 74,780 | 4 | 59.0 |

- **Recall** 26/26 with the skill versus 25/26 without; the miss was color-only tab selection. Two runs per arm cannot establish a difference.
- **Precision**: no arm reported a trap. Both skill runs explicitly cleared all three traps in a "Checked and fine" section; the control runs cleared the accepted exception but left the hit-slop targets mostly implicit.
- **Additional valid findings**: one skill run found that the edit field's only visible boundary is a 1.40:1 underline (fails WCAG 1.4.11), which neither control run reported, and correctly cited WCAG 2.2.2 for the endless pulse.
- **Labels**: skill findings carried strength, evidence, root cause, and retest. A separate no-device skill run under the stricter rule labeled every finding correctly (dark-mode support as Guideline, contrast as Required with WCAG 1.4.3, target size as Guideline), fixing the earlier mislabels; one run only.
- **Answer-key correction**: seeded defect 11 originally said backdrop dismissal discards edits. The control runs instead reported that the sheet keeps stale state; both readings are true (edits are not saved, and the field persists on reopen), so the key now accepts either.
- **Cost**: the skill used 31.6% more tokens (198,364 versus 150,764) and about 2.5 times the summed subagent time, mostly from reading two references and writing fuller reports. Afterward the entrypoint stopped routing ordinary reviews to `visual-quality.md`; that saving has not been measured.
- The control model is strong on code-only audits. The skill's largest expected gain, driving simulators and emulators for rendered evidence, could not be exercised without a runnable app.

## Limits

One run per arm; four of twelve cases; author grading; inherited and unpinned model metadata; possible influence of the host's session-level plugins on all arms. No `yb-frontend-engineer` or UI/UX Pro Max-assisted arm was run, no rendered verification was available, and native skill triggering was not exercised (skills were loaded by path). The eight unrun cases, including the trading, typography, iOS, Android, text-scaling, redesign, component, and premium-direction cases, have fixtures and assertions but no results.

Use the [evaluation protocol](../../evals/README.md) for repeated, blinded, configuration-matched comparisons with a stronger rubric (defect recall, false positives, and label accuracy) before claiming a quality or efficiency advantage.
