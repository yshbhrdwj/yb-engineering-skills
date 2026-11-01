# Unified web and mobile frontend: forward check

Run on 2 November 2026 from base `51d8c62` with the unified frontend changes uncommitted on the working branch. Two of the sixteen new cases ran once per arm. Arm A used this branch's `yb-frontend-engineer`/`yb-frontend-reviewer` (Claude edition); arm B used the same skills at `51d8c62`. Runners were general-purpose subagents on the same model and host session. Each got the same prompt, a copy of the case's input files, and the path to its arm's skill folder. They were told not to use the Skill tool or read other skills, and the acceptance criteria were hidden from them. Runners were not told which arm they were in. The author graded the runs against `evals/cases.json` and knew the arm labels, so grading was **not blind**. Plugins and hooks active in the parent session may also have reached the runners. Runner transcripts are not saved in this repository; the token and time figures come from the host's task notifications.

| Case | Arm | Result | References read | Tokens | Seconds |
| --- | --- | --- | --- | ---: | ---: |
| `fe-rn-style-fast-path` | A (new) | One line: `paddingVertical: 3` → `theme.space.md`; said it was not rendered and tests were not run. Met all 3 criteria | none | 68,045 | 22.9 |
| `fe-rn-style-fast-path` | B (old) | Identical diff and disclosures. Met all 3 criteria | none | 68,034 | 24.0 |
| `rev-native-order-detail` | A (new) | 6/6 seeded defects; Android-only behavior distinguished; no device evidence claimed; files unchanged. **One trap reported:** flagged the Close target as smaller than it looks, although it reaches 44 points through hitSlop | `native-probes.md` | 75,384 | 70.0 |
| `rev-native-order-detail` | B (old) | 6/6 seeded defects (the SafeAreaView finding is listed as an unconfirmed concern); explicitly cleared the Close trap; no device evidence claimed; files unchanged. No trap reported | `interaction-probes.md` | 76,944 | 83.9 |

## Reading

- On the fast path, both arms behaved the same. The new paths, routing, and mobile references were not loaded for a one-line fix. That is the intended efficiency outcome, but it is not an improvement over the old skill.
- On native review, the old skill already found every seeded defect. The new skill loaded the native probe reference as routed and had one false positive (low severity). One run per arm shows no quality advantage, and the false positive came from the "Touch targets and gestures" probe. After this run, the probe gained "(an extended hit area counts)". The committed text has not been rerun.
- Single runs and author grading cannot support a causal quality, cost, or speed claim. After the second round below, twelve of the sixteen new cases have still not run.

## Second round, after merging `yb-web-design-system` (main `ec9969a`)

Same method and limits as above: one run per arm, author-graded with arm labels known, transcripts not saved. Arm B is the skills at `ec9969a`. Both arms' installed-skills folders contained the engineer, reviewer, QA, web design, and mobile design skills.

| Case | Arm | Result | Files read beyond `SKILL.md` | Tokens | Seconds |
| --- | --- | --- | --- | ---: | ---: |
| `rev-native-order-detail` | A (rerun with the clarified touch-target probe) | 6/6 seeded defects; explicitly cleared the 44-point Close trap; no false positive; files unchanged | `native-probes.md`, `interaction-probes.md` | 78,040 | 88.0 |
| `qa-critical-transfer` | A | 4/4 criteria: 22 tests, 1 pass (a guard that a new transfer gets a new key), 21 fail. Exact counterexamples (19.99 → 1998; a sweep found 4,586 of 100,000 two-decimal amounts wrong); not ready; product hash unchanged. Ran the file twice, giving the reason (assertion order) | `testing-depth.md` | 80,607 | 94.6 |
| `qa-critical-transfer` | B | 4/4 criteria: 27 tests, 5 pass, 22 fail; the same counterexamples; not ready; product hash unchanged | `testing-depth.md` | 82,576 | 66.1 |
| `fe-design-authority-integration` | A1 (branch text before the fix below) | Computed 3.04:1 and flagged it, but **shipped the failing approved color**. Opened no routing reference or design skill | `mobile-implementation.md` | 74,464 | 71.8 |
| `fe-design-authority-integration` | B | Computed 3.04:1; used `#9CA3AF` (5.78:1), flagged for design sign-off; built both badges. Opened the mobile design skill, not the web one | `yb-mobile-design-system/SKILL.md` | 74,767 | 67.1 |
| `fe-design-authority-integration` | A2 (first fix: "unless it fails accessibility") | Computed and flagged the conflict, then **stopped without implementing** and asked for a color | none | 70,144 | 41.4 |
| `fe-design-authority-integration` | A3 (committed text: build around an accessibility failure and flag it) | Computed 3.04:1; used `#9CA3AF` (5.78:1), flagged for sign-off, DESIGN.md untouched; built both badges | `platform-routing.md`, both design skills' `SKILL.md` | 80,174 | 88.3 |

**Answer-key change.** The original first criterion required consulting both design skills. That contradicts the routing precedence: an approved project design document outranks specialized design guidance. After seeing these runs, the criterion was revised to "treats the approved DESIGN.md and shared tokens as the authority, loading a design skill only for an open question". Scores under the original key: A1 3/4, B 3/4, A2 2/4, A3 4/4. Under the revised key: A1 4/4, B 4/4, A2 3/4, A3 4/4. Neither key credits A1's choice to ship a known failure. That is a rubric gap, and it is why the engineer text was changed twice.

**Reading.** QA parity: both arms found every defect. The native review false positive did not recur after the probe clarification. On the authority case, the first branch text regressed against the old skill: it shipped a failing approved color. The committed wording fixed that in one run, but one run cannot show the fix is reliable.
