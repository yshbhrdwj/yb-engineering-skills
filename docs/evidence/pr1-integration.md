# PR #1 carryovers into the revised suite

Compared PR #1 head `6e967dcb600e897155956eb58a929bb5a3bcf6dc` with PR #2 head `d2ad6079298c9bad81d81e6319052b47d2dfd788`, which share base `95d978c6fbf52e5205018f63f65695dc5ff7be9a`. This record explains the selective carryover; it does not claim new model-backed validation.

## Preserved behavior

The revised roles retain the four state-change cases, short design notes for consequential changes, independent review from requirements and raw artifacts, meaningful verification, controlled browser harnesses, synthetic test data, disclosed evidence gaps, and complete requested deliverables.

This integration additionally preserves four useful details:

- The [product handoff](../../codex/skills/yb-product-strategist/references/handoff-document.md) creates new IDs only for requirements, using short names for assumptions, experiments, policies, and open decisions unless the project already numbers them. Accepted intent and actual verification remain separate.
- Each platform footer explicitly loads applicable named skills and passes the relevant skill path or instructions, requirements, and raw artifacts to delegated work. Mentioning a skill does not establish that its instructions were loaded.
- The shared-core mutation test asserts that its target was found before validating the changed file. It retains the revised footer-boundary mutation. All validator-fixture text reads and writes explicitly use UTF-8, preserving the PR #1 Windows encoding repair.
- The [September 28 evidence archive](2026-09-28-behavior-pass.md) preserves the original trial report and text counts with their limitations. Current [text counts](../../TOKEN-EFFICIENCY.md) are recomputed after these instruction changes; text size is not a runtime performance claim.

## Superseded procedures

The dedicated [merge workflow](../../codex/skills/yb-merge-pr/SKILL.md) replaces repeated merge instructions in other roles. It requires trusted, non-author formal approval on the exact head; a comment, reaction, or “no major issues” phrase is insufficient. Review requests and other external messages still require authorization. Report-only reviewers remain separate from implementation and landing.

Risk-based review and testing replace fixed reviewer chains and unconditional base-suite runs. Concise delivery preserves full requested artifacts without rigid word or line ceilings. Evidence-driven reassessment replaces an arbitrary patch-count threshold. Existing hook, installation, evaluation-accounting, and native reviewer configuration fixes remain in place. Automatic CI remains disabled at the user's request.

## Retired reviewer paths

Apply this mapping beneath either `codex/skills/` or `claude-code/skills/`; do not recreate the retired skill directories.

| Historical path | Current path |
| --- | --- |
| `yb-code-correctness-reviewer/SKILL.md` | `yb-code-reviewer/SKILL.md` |
| `yb-code-design-reviewer/SKILL.md` | `yb-code-reviewer/SKILL.md` |
| `yb-code-correctness-reviewer/references/state-failures.md` | `yb-code-reviewer/references/state-failures.md` |
| `yb-code-correctness-reviewer/references/algorithms-performance.md` | `yb-code-reviewer/references/algorithms-performance.md` |
| `yb-code-design-reviewer/references/design-lenses.md` | `yb-code-reviewer/references/design-lenses.md` |

The three references are unchanged by the reviewer consolidation. Codex discovery metadata now lives at `codex/skills/yb-code-reviewer/agents/openai.yaml`; both former metadata files are retired.

Shared evidence keeps repository-relative links to the canonical source edition. Packaging rewrites those Markdown skill links to each archive's root `skills/` layout; the existing extracted-bundle link check covers both editions.

## Encoding replay

A local replay supplied a UTF-8 Unicode skill fixture and simulated cp1252 defaults only for omitted `Path.read_text`/`Path.write_text` encodings. The existing shared-core test raised `UnicodeDecodeError` before the explicit-encoding repair. All 21 validator-fixture tests passed afterwards under that same simulation. This is not native Windows execution and changes no global locale or configuration.
