# Text size and efficiency

Measured on 1 November 2026 against repository commit `95d978c6fbf52e5205018f63f65695dc5ff7be9a`. Counts are whitespace-delimited words in complete Codex `SKILL.md` files, including frontmatter and host footer. Claude has the same instructions with a small amount of extra runtime metadata.

| Role | Previous entrypoint words | Current entrypoint words |
| --- | ---: | ---: |
| `yb-code-reviewer` | 1464 | 529 |
| `yb-frontend-engineer` | 845 | 489 |
| `yb-frontend-reviewer` | 789 | 480 |
| `yb-merge-pr` | new | 500 |
| `yb-product-strategist` | 847 | 490 |
| `yb-qa-engineer` | 821 | 503 |
| `yb-release-operator` | 734 | 511 |
| `yb-security-privacy` | 737 | 462 |
| `yb-software-engineer` | 791 | 523 |
| `yb-solution-architect` | 784 | 446 |
| **Total** | **7,812** | **4,933** |

The two former code-review entrypoints are summed in the unified reviewer baseline. The new merge workflow is included in the current total. The complete entrypoints are **36.9% shorter** by this measure. [Machine-readable counts](docs/evidence/text-size.json) record the baseline and mapping.

Optional Markdown references total 5,417 words, versus 5,369 previously. They preserve useful conditional depth and are not loaded wholesale. Total main-plus-reference text is 10,350 words versus 13,181 previously, a 21.5% reduction.

## Behaviors intended to reduce unnecessary work

- Batch independent, targeted reads; expand when evidence warrants it.
- Prefer reuse and the smallest complete implementation.
- Skip routine design documents and extra reviewers for small corrections.
- Use one code reviewer for behavior and consequential design concerns.
- Run affected checks first; repeat or broaden after changes, failures or unresolved risk.
- Keep routine narration brief while delivering requested artifacts completely.
- Leave model and effort selection to the host/user; avoid unconditional model overrides.
- Run opted-in Stop checks once per stable successful content state and session.

These are design choices and text measurements, not a demonstrated runtime speedup. The historical one-shot trials of an earlier draft did not show lower time or token use; see [their audit](docs/evidence/2026-11-01-eval-audit.md). New qualitative checks establish specific observed behavior only. A controlled repeated comparison is still needed to estimate latency/cost and precision across tasks. The [evaluation protocol](evals/README.md) defines that comparison.

The separate [independent-review evidence audit](docs/evidence/gemini-review-audit.md) checks the newer Gemini trials. Its narrow implementation-task result is not a native-host or whole-suite performance claim.

The [September 28 behavior-pass archive](docs/evidence/2026-09-28-behavior-pass.md) preserves PR #1’s historical counts and author-reported trial separately; its footer-excluding method and tested instructions differ from this measurement. No historical trial was rerun for this integration.

## yb-web-design-system (measured 2 November 2026)

Same method (whitespace-delimited words with `wc -w`, complete Codex files), on branch `claude/yb-web-design-system`, measured on commit `2692621`. The table above is unchanged and still describes its own commit.

| File | Words |
| --- | ---: |
| `SKILL.md` | 536 |
| `references/components.md` | 1,674 |
| `references/industry-playbooks.md` | 1,188 |
| `references/color-surfaces.md` | 1,011 |
| `references/accessibility-design.md` | 940 |
| `references/layout-responsive.md` | 935 |
| `references/typography.md` | 932 |
| `references/design-foundations.md` | 898 |
| `references/frameworks-feasibility.md` | 823 |
| `references/audit-redesign.md` | 704 |
| `references/source-registry.md` | 653 |
| `references/website-vs-webapp.md` | 650 |
| `references/interaction-motion.md` | 590 |
| `references/integration-handoffs.md` | 585 |
| **References total** | **11,583** |

The entrypoint is 7 words above the largest existing one (`yb-code-reviewer`, 529). References are loaded by mode, never all at once. Whole-file reads are the unit of cost: Mode 1 needs the entrypoint plus at most `components.md` (2,210 words if read whole); a Mode 3 page task listed in the entrypoint loads about 2,374 words (entrypoint, `website-vs-webapp.md`, `industry-playbooks.md`). In one observed Mode 3 run the runner read five references (see the [evaluation record](docs/evidence/2026-11-02-web-design-evals.md)). `yb-frontend-engineer`'s entrypoint changed from 489 to 493 words with its description cross-reference. These are text sizes, not runtime measurements.

