# yb-web-design-system: first matched runs (2026-11-02)

Three of the twelve `web-design-*` cases, one repetition each, three arms. This is a small qualitative check, not a benchmark.

## Conditions

- Skill and fixtures pinned at commit `2692621` (branch `claude/yb-web-design-system`).
- Runner: Claude Code background subagents (`general-purpose`), the same model as the host session (Opus 5.5), launched together in one batch. Each arm received the same task prompt and its own copy of the case fixtures, and was told not to read anything else, use a browser, or edit files.
- Arms: `with_skill` read this skill's Claude edition `SKILL.md` and followed it. `without_skill` was told not to use skills or read any `SKILL.md`. `uiux_pro_max` read the installed UI/UX Pro Max v2.15.0 `SKILL.md` and could run its search script (no `--persist`).
- The acceptance criteria were hidden from runners. Runners could not write report files, so their final messages were collected as the responses.
- Tokens, tool uses and durations are host-reported subagent totals. They include each runner's fixed system context, so differences are small relative to totals.

## Limitations

- One repetition per arm and case; no randomization of order beyond simultaneous launch.
- The author of the skill graded the responses, unblinded, against the catalog's acceptance criteria. Numeric claims were recomputed independently (all contrast ratios that runners reported were correct).
- Isolation was by instruction, not enforcement: the host could not disable other installed skills or plugins for subagents. No arm reported using the Skill tool.
- "Files read" for efficiency comes from each runner's own run record, cross-checked against the host's tool-use count, not from a tool trace.

## Results

| Case | Arm | Acceptance passed | Subagent tokens | Tool uses | Duration (s) | Skill files read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| button-spacing | with_skill | 5/5 | 67,876 | 4 | 30.7 | SKILL.md only |
| button-spacing | without_skill | 4/5 | 65,502 | 3 | 21.9 | none |
| button-spacing | uiux_pro_max | 4/5 | 74,679 | 6 | 41.3 | SKILL.md, 2 searches |
| type-hierarchy | with_skill | 5/5 | 73,252 | 6 | 60.5 | SKILL.md, typography.md |
| type-hierarchy | without_skill | 5/5 | 66,543 | 3 | 38.8 | none |
| type-hierarchy | uiux_pro_max | 5/5 | 80,035 | 8 | 67.8 | SKILL.md, 4 searches, quick-reference grep |
| trading | with_skill | 5/5 | 85,919 | 9 | 100.4 | SKILL.md, 5 references |
| trading | without_skill | 3/5 | 69,471 | 4 | 64.1 | none |
| trading | uiux_pro_max | 5/5 | 86,157 | 9 | 88.2 | SKILL.md, 8 searches incl. `--design-system` |
| **Total** | with_skill | **15/15** | 227,047 | 19 | 191.6 | |
| | without_skill | **12/15** | 201,516 | 10 | 124.8 | |
| | uiux_pro_max | **14/15** | 240,871 | 23 | 197.3 | |

## Failures and notable observations

- **button-spacing.** All arms found the 38px versus 40px cause and the `var(--space-2) var(--space-4)` fix, and left the secondary button's border compensation alone. The no-skill and UI/UX Pro Max arms gave no explicit verification step, failing the micro-output criterion. UI/UX Pro Max ran two searches; its runner reported neither result was on topic. The skill arm read no references, as Mode 1 intends.
- **type-hierarchy.** All three found at least seven of the eight seeded defects and flagged no trap. The skill arm stated Mode 2, loaded only `typography.md`, and computed text contrast. No arm differed materially in quality; the baseline was strong, as in earlier work.
- **trading.** All arms computed the key contrast values correctly (muted 3.13, down 3.47, up 5.41 against `#0e1117`) and kept the dark, dense layout. The no-skill arm did not add arrow or sign cues beyond those already present and did not propose an order confirmation summary (2 failures). The skill arm loaded five references, including all of `industry-playbooks.md`. That is more than the Mode 3 row lists and made it the slowest run; it is the main efficiency defect observed. UI/UX Pro Max's `--design-system` query returned the "Enterprise Gateway" marketing landing pattern for a trading terminal; its runner discarded it.

## What this does and does not show

On these three cases the skill arm met every criterion and the no-skill arm missed three, all on the trading screen. The skill cost more time and tokens than no skill on every case, and about the same as UI/UX Pro Max. Nine runs by an unblinded author-grader cannot establish superiority, reliability on the other nine cases, or behavior on other models. The remaining nine cases were not run.
