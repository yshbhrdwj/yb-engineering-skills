# Text size and efficiency

Measured on 1 November 2026 against repository commit `95d978c6fbf52e5205018f63f65695dc5ff7be9a`. Counts are whitespace-delimited words in complete Codex `SKILL.md` files, including frontmatter and host footer. Claude has the same instructions with a small amount of extra runtime metadata.

| Role | Previous entrypoint words | Current entrypoint words |
| --- | ---: | ---: |
| `yb-code-reviewer` | 1464 | 508 |
| `yb-frontend-engineer` | 845 | 468 |
| `yb-frontend-reviewer` | 789 | 459 |
| `yb-merge-pr` | new | 479 |
| `yb-product-strategist` | 847 | 469 |
| `yb-qa-engineer` | 821 | 482 |
| `yb-release-operator` | 734 | 490 |
| `yb-security-privacy` | 737 | 441 |
| `yb-software-engineer` | 791 | 502 |
| `yb-solution-architect` | 784 | 425 |
| **Total** | **7,812** | **4,723** |

The two former code-review entrypoints are summed in the unified reviewer baseline. The new merge workflow is included in the current total. The complete entrypoints are **39.5% shorter** by this measure. [Machine-readable counts](docs/evidence/text-size.json) record the baseline and mapping.

Optional Markdown references total 5,374 words, versus 5,369 previously. They preserve useful conditional depth and are not loaded wholesale. Total main-plus-reference text is 10,097 words versus 13,181 previously, a 23.4% reduction.

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
