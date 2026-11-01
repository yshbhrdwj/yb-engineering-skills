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

## Mobile design system addition

Measured on 1 November 2026 with the same word-count method. `yb-mobile-design-system` adds an 845-word entrypoint and seventeen references totaling 16,150 words (current revision; the first revision had 963 and 11,674). The entrypoint is larger than other roles because it carries the mode routing table and reference map; the domain knowledge stays in references that are read one section or file at a time. A one-line fix is designed to load the entrypoint only, or one reference. Adding the routing sentence grew `yb-frontend-engineer` from 489 to 501 words and `yb-frontend-reviewer` from 480 to 494. The table above is unchanged because it records the earlier revision.

## Unified web and mobile frontend

Measured on 2 November 2026 with the same whitespace word count over complete Codex `SKILL.md` files. The first figure is base `51d8c62`; the second is this branch after merging `ec9969a` (main had moved `yb-frontend-engineer` to 505). Entrypoints: `yb-frontend-engineer` 501 → 528, `yb-frontend-reviewer` 494 → 529, `yb-qa-engineer` 503 → 530. Existing references: `experience-design.md` 474 → 489, `implementation-verification.md` 507 → 509, `interaction-probes.md` 388 → 498, `testing-depth.md` 247 → 416. New references, each loaded only when routing selects it: `platform-routing.md` 509, `mobile-implementation.md` 510, `native-probes.md` 364, `platform-testing.md` 358. The three roles' entrypoint text grew by 89 words (5.9%), and their optional references by 2,037 words (1,616 → 3,653). Runtime cost is unmeasured except for the two single-run samples in the [forward check](docs/evidence/2026-11-02-frontend-unified-forward-check.md). There, the fast-path case read no reference in either arm at near-identical token counts (68,045 versus 68,034), and the transfer QA case used 80,607 tokens with the new skill versus 82,576 with the old one, in single runs.

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

