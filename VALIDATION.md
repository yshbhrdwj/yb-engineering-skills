# Validation and evidence

Updated 1 November 2026. Ten roles, each packaged for Claude Code and Codex. Evidence below distinguishes packaging and deterministic helper tests from observed reasoning behavior and host integration.

## Deterministic checks

The host-aware validator checks exact skill inventory, portable names/descriptions, Claude reviewer fork configuration, Codex UI metadata, matching task instructions and references, allowed payloads, and local Markdown links. It deliberately accepts a narrow authored YAML format rather than arbitrary YAML.

The 99 locally passing regression tests exercise safe skill updates, backups and explicit migration; malformed metadata and platform drift; hook approval/target/CI logic with a stub GitHub CLI; project-only reviewer trust; Stop recursion, timeout, content caching and failures; hook installation preserving unrelated settings; evaluation accounting; and extracted bundle installation. All GitHub calls in the hook tests are local mocks; no test merges a live PR.

The bundled skill-creator validator passes all ten Codex folders. Its generic Agent Skills schema rejects Claude Code runtime fields such as `argument-hint`, `context`, `agent` and `background`; the host-aware validator checks those fields against the [Claude Code reference](https://code.claude.com/docs/en/skills) instead. Passing these checks does not prove correct automatic selection or reasoning.

The GitHub workflow runs validation, tests and packaging on Linux, macOS and Windows. POSIX shell-hook integration tests are explicitly skipped on native Windows; installer, validator and accounting tests remain portable. The Stop script convention requires a POSIX shell. Consult the actual workflow for the pushed commit's CI outcome.

## Current behavioral checks

The [public catalog](evals/README.md) has one synthetic task per role, with outcome-based acceptance, a correct-code control and explicit authority/tool limits. A fresh runner receives the skill, task and raw fixtures with the grading rubric hidden. A separate evaluator inspects actual artifacts and command evidence. These are qualitative forward checks, not repeated matched comparisons. The [forward-check report](docs/evidence/2026-11-01-forward-checks.md) records outcomes and limitations.

## Native host smoke checks

Codex CLI `0.165.0-alpha.1.2` loaded the project `yb-code-reviewer` from the packaged project installation under a read-only sandbox. It identified the synthetic stock oversell and cross-account invoice access, produced no finding for the correct clamp control, and ran local in-memory reproductions. No live service or application fixture was modified. This is one review smoke test, not native execution of every role or automatic-trigger coverage.

Claude Code `2.1.301` listed all ten project skills with user hooks and unrelated installed plugins excluded. The attempted forked reviewer model call stopped before inference because the saved OAuth session had expired and could not refresh. Discovery was observed; successful native forked execution remains unverified. The command's final result text was checked rather than relying on exit status alone. Local manual-load behavior checks and schema validation cannot substitute for that missing host result.

## Historical interrupted trials

The earlier draft's saved and recovered trials are audited in [the historical report](docs/evidence/2026-11-01-eval-audit.md). Seventeen complete saved old/new comparisons passed 57/69 versus 58/69 assertions, with 4.21% more recorded tokens and 5.56% more summed time in the new arm. Weak assertions, one sample, plugin contamination and missing harness metadata prevent a causal performance claim. Those numbers do not score this revision.

No controlled result establishes superiority over Ponytail. [Text-size reductions](TOKEN-EFFICIENCY.md) are measured separately from runtime costs. No production deployment, real payment/message, external user study, live-data exploit or full accessibility-conformance test was performed.
