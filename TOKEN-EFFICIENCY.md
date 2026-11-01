# Token-efficiency design and measurements

Measurements use whitespace-delimited word counts of the authored skill files, including metadata. The historical baseline compares the original eight drafts immediately before the efficiency pass with their renamed versions after that pass, including their best-practices rule. Host footers are excluded consistently. These are exact text counts, not tokenizer measurements or runtime cost benchmarks.

| Skill | Main file before | Main file after | Reduction |
| --- | ---: | ---: | ---: |
| `yb-product-strategist` | 1,540 | 817 | 46.9% |
| `yb-solution-architect` | 1,592 | 754 | 52.6% |
| `yb-software-engineer` | 1,205 | 761 | 36.8% |
| `yb-qa-engineer` | 1,648 | 791 | 52.0% |
| `yb-code-design-reviewer` | 1,432 | 691 | 51.7% |
| `yb-code-correctness-reviewer` | 1,475 | 713 | 51.7% |
| `yb-security-privacy` | 1,666 | 707 | 57.6% |
| `yb-release-operator` | 1,845 | 704 | 61.8% |
| **Total** | **12,403** | **5,938** | **52.1%** |

Including every optional Markdown reference, the complete authored content changed from 14,026 to 9,866 words (29.7% reduction). The main files provide the common path; detailed references load only for relevant decisions. Each skill remains self-contained.

## Runtime habits encoded

- Read targeted artifacts and expand only when risk, evidence, or requested scope warrants it.
- Load applicable reference sections; do not load every specialist or checklist for every request.
- Use one authoritative requirements register, stable IDs, source revisions, and evidence links.
- Prefer compact findings and changed-decision updates over repeated source dumps, summaries, or rewritten unchanged documents.
- Scale planning, testing, research, delegation, and lifecycle routing to the task; avoid duplicate checks without a new reason.
- Preserve complete requested deliverables, accepted requirements, meaningful verification, scope/permission boundaries, and relevant best practices.

Actual token and cost savings depend on the tokenizer, model, task, tools, and which references are needed. Long or high-risk work may appropriately require more context. No proportional runtime saving is claimed from text counts alone.

The product handoff test decreased from 3,287 to 2,278 words after the efficiency pass in two separate qualitative runs. This is an observed example, not a controlled performance benchmark.

## Frontend additions — 25 September 2026

The two frontend skills start compact; there is no earlier verbose version for a reduction comparison. Counts exclude platform footers, consistent with the baseline above.

| Added skill | Main file | Optional references |
| --- | ---: | ---: |
| `yb-frontend-engineer` | 815 | 981 |
| `yb-frontend-reviewer` | 759 | 388 |

The 52.1% reduction above describes the original eight-skill compression, not all ten skills or measured runtime savings. The product workflow reference now includes the two frontend roles.

## Behavior pass — 28 September 2026

This pass made the main files longer, not shorter. Counts use the same method as above: words in the shared core, platform footers excluded.

Historical provenance: the table and account below record the initial published behavior pass at commit `6e967dcb600e897155956eb58a929bb5a3bcf6dc`. Later merge-gate corrections changed the wording and main-file sizes; these are historical counts, not counts of the corrected package. The corrections were not followed by a behavior-trial rerun, so the trial does not establish the behavior of the corrected wording.

| Skill | Main file before | Main file after | Change |
| --- | ---: | ---: | ---: |
| `yb-product-strategist` | 817 | 965 | +18.1% |
| `yb-solution-architect` | 754 | 813 | +7.8% |
| `yb-software-engineer` | 761 | 1,347 | +77.0% |
| `yb-frontend-engineer` | 815 | 1,241 | +52.3% |
| `yb-frontend-reviewer` | 759 | 1,053 | +38.7% |
| `yb-qa-engineer` | 791 | 992 | +25.4% |
| `yb-code-design-reviewer` | 691 | 1,045 | +51.2% |
| `yb-code-correctness-reviewer` | 713 | 1,107 | +55.3% |
| `yb-security-privacy` | 707 | 1,070 | +51.3% |
| `yb-release-operator` | 704 | 996 | +41.5% |
| **Total** | **7,512** | **10,629** | **+41.5%** |

The growth comes from new procedures, including:

- a merge gate
- four state-change cases
- independent review of your own code
- a short report shape

It also comes from one example output per skill and plainer wording. The product handoff reference grew from 693 to 757 words; it now gives IDs only to requirements.

In the small trial recorded in [VALIDATION.md](VALIDATION.md#behavior-pass--28-september-2026), the longer instructions produced shorter replies: 40–70% fewer words. Tokens per run were about the same. That trial has two runs per version, so it is not evidence of runtime savings.
