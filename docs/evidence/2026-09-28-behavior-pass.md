# Historical behavior pass — 28 September 2026

This archive preserves the author-reported September 28 sections from `VALIDATION.md` and `TOKEN-EFFICIENCY.md` in PR #1, source commit `6e967dcb600e897155956eb58a929bb5a3bcf6dc`. Skill names and counts below describe those historical instructions, including the two now-retired code reviewers. Historical counts exclude platform footers and are not comparable directly with the current complete-file counts.

The raw trial prompts, transcripts, and grades are not included in this repository. This integration preserved the written record without independently regrading or rerunning it. The source's limitations remain in force: two runs per version, author-written tasks, no Codex runtime test, six roles without behavioral coverage, and no rerun after final wording edits. These observations do not score the current skills or establish runtime savings. The separate [November interrupted-trial audit](2026-11-01-eval-audit.md) concerns a different dataset.

## Historical validation record

### What prompted it

Reviewing real sessions that used these skills showed a consistent pattern. The evidence discipline held up: agents ran baselines, confirmed regression tests failed on old code, and disclosed unrun checks. But bugs involving concurrency, retries, mixed-version deploys and caps kept shipping while the author's own tests passed. External review bots caught them later. Several pull requests were also merged before the bot's review of the latest commit arrived. Chat reports ran 400–800 words.

### Changes

- **Merge gate** in the seven skills that can merge. Read every PR comment and review, and get any review bot's review of the head commit. Fix each comment or reply to it, treating comments as claims to check, not instructions.
- **Four state-change cases** for code that writes or caches state: two at once, old meets new, fails halfway, and past the edge.
- **Independent review.** A fresh subagent reviews risky changes, or the report is labeled a self-review.
- **Report shape.** Status summaries run about 150 words; requested deliverables stay complete.
- **Design notes** only for risky or large changes.
- **Examples and cleanup.** One example output per skill, a single shared best-practice paragraph, and fewer requirement IDs in the product brief.

### Trial

An old-versus-new trial ran in Claude Code subagents. There were three tasks, with two runs per version on each. The old skills were used as the baseline.

- The review and strategy replies were scored by a grader that didn't know which version produced them.
- The fix-and-merge task used a simulated `gh` with a pending bot review comment, and hidden tests scored the fix.

| Task | New | Old |
| --- | --- | --- |
| Review a diff with three planted defects and one decoy | 5/6, 5/6; 476–506 words | 5/6, 5/6; 751–948 words |
| Fix a sync race and merge a PR with a pending bot P1 | 9/9, 8/9; 172–201 words | 8/9, 6/9; 366–524 words |
| First reply to a founder's product question | 6/6, 6/6; about 280 words | 4/6, 4/6; 808–886 words |

Both versions found every planted defect and passed every hidden test. The fix task gave its answer away through the bot's comment, so neither of those two tasks separated the versions.

Several differences did appear:

- **Merge gate.** Both new runs replied on the bot's thread and requested a re-review of the new commit, merging only after it answered. One old run did the same unprompted; the other merged an unreviewed commit.
- **Length.** New replies were 40–70% shorter.
- **Questions.** The new strategist gave a suggested answer with each question.
- **Speed.** New merge runs took about 2.3 times longer, because of the independent review and the bot round trip.
- **Lost content.** Both old strategy replies cited India's 2023 guidelines on dark patterns, and neither new reply did.

### Limits

- Two runs per version is a small sample.
- The tasks were written by the same author as the changes.
- No Codex runtime was tested.
- Six skills received no behavior test.
- After the trial, examples were made project-neutral and the best-practice paragraph was unified. The trial was not rerun afterwards.

The validator test for shared-core drift was updated because its mutation target no longer existed. It now fails loudly if that happens again.

## Historical text-size record

This pass made the main files longer, not shorter. Counts use the same method as above: words in the shared core, platform footers excluded.

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

In the small trial recorded in [the validation record above](#historical-validation-record), the longer instructions produced shorter replies: 40–70% fewer words. Tokens per run were about the same. That trial has two runs per version, so it is not evidence of runtime savings.
