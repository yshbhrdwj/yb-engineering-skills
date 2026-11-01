# Validation and evidence

Updated 1 November 2026; `yb-web-design-system` added 2 November 2026 (see the dated section at the end). Twelve roles, each packaged for Claude Code and Codex. Evidence below distinguishes packaging and deterministic helper tests from observed reasoning behavior and host integration.

## Deterministic checks

The host-aware validator checks exact skill inventory, portable names/descriptions, Claude reviewer fork configuration, Codex UI metadata, matching task instructions and references, allowed payloads, and local Markdown links. It deliberately accepts a narrow authored YAML format rather than arbitrary YAML.

The 138 locally passing regression tests exercise safe skill updates, backups and explicit migration; malformed metadata and platform drift; hook approval/target/CI logic with a stub GitHub CLI; project-only reviewer trust; Stop recursion, timeout, content caching and failures; hook installation preserving unrelated settings; evaluation accounting; and extracted bundle installation. All GitHub calls in the hook tests are local mocks; no test merges a live PR.

The bundled skill-creator validator passes all ten Codex folders. Its generic Agent Skills schema rejects Claude Code runtime fields such as `argument-hint`, `context`, `agent` and `background`; the host-aware validator checks those fields against the [Claude Code reference](https://code.claude.com/docs/en/skills) instead. Passing these checks does not prove correct automatic selection or reasoning.

Automatic GitHub CI is disabled at the user’s request. The retained manual workflow defines validation, tests and packaging on Linux, macOS and Windows; its last run for commit `a026ec3` passed on all three. POSIX shell-hook integration tests are explicitly skipped on native Windows; installer, validator and accounting tests remain portable. The Stop script convention requires a POSIX shell. Consult the actual workflow for the pushed commit's CI outcome.

## Current behavioral checks

The [public catalog](evals/README.md) has one synthetic task per role, with outcome-based acceptance, a correct-code control and explicit authority/tool limits. A fresh runner receives the skill, task and raw fixtures with the grading rubric hidden. A separate evaluator inspects actual artifacts and command evidence. These are qualitative forward checks, not repeated matched comparisons. The [forward-check report](docs/evidence/2026-11-01-forward-checks.md) records outcomes and limitations.

## Mobile design system check

`yb-mobile-design-system` adds twelve synthetic cases with an Expo fixture app. A [two-arm forward check](docs/evidence/2026-11-01-mobile-design-forward-check.md) ran four of them once each with and without the skill. Both arms met all 16 assertions; the skill arm loaded no reference on the micro task but used 15.9% more tokens and more time overall. A rerun of three cases on the refined revision again showed parity on assertions, fewer references loaded, and 10.7% more tokens; both arms found a real defect in the intended clean control, which has since been fixed. These are routing and cost samples, not evidence of a quality or speed advantage. A discriminating six-file audit with 13 seeded defects and three traps then ran twice per arm: the skill found 26/26 and the control 25/26, neither reported a trap, and the skill used 31.6% more tokens. Two runs per arm do not establish a quality advantage. Thirteen of the seventeen mobile cases have never been run.

## Native host smoke checks

Codex CLI `0.165.0-alpha.1.2` loaded the project `yb-code-reviewer` from the packaged project installation under a read-only sandbox. It identified the synthetic stock oversell and cross-account invoice access, produced no finding for the correct clamp control, and ran local in-memory reproductions. No live service or application fixture was modified. This is one review smoke test, not native execution of every role or automatic-trigger coverage.

Claude Code `2.1.301` listed all ten project skills with user hooks and unrelated installed plugins excluded. The attempted forked reviewer model call stopped before inference because the saved OAuth session had expired and could not refresh. Discovery was observed; successful native forked execution remains unverified. The command's final result text was checked rather than relying on exit status alone. Local manual-load behavior checks and schema validation cannot substitute for that missing host result.

## Historical interrupted trials

The [September 28 behavior-pass record](docs/evidence/2026-09-28-behavior-pass.md) preserves PR #1’s reported trial and text counts with their original limits. Its raw trial artifacts were not regraded or rerun during integration; it does not validate the current candidate.

The [PR #1 integration record](docs/evidence/pr1-integration.md) distinguishes preserved intent from superseded procedures and records the validator fixture's local encoding replay. Simulated cp1252-default I/O reproduced a Unicode decoding failure before explicit UTF-8 fixture I/O; all 21 fixture tests passed after the repair. This was not a native Windows run.

The earlier draft's saved and recovered trials are audited in [the historical report](docs/evidence/2026-11-01-eval-audit.md). Seventeen complete saved old/new comparisons passed 57/69 versus 58/69 assertions, with 4.21% more recorded tokens and 5.56% more summed time in the new arm. Weak assertions, one sample, plugin contamination and missing harness metadata prevent a causal performance claim. Those numbers do not score this revision.

No controlled result establishes superiority over Ponytail. [Text-size reductions](TOKEN-EFFICIENCY.md) are measured separately from runtime costs. No production deployment, real payment/message, external user study, live-data exploit or full accessibility-conformance test was performed.

## Local remediation after independent review

The later [evidence audit](docs/evidence/gemini-review-audit.md) distinguishes reproducible findings from reporting and accounting errors. Remediation covers current-branch CLI lookup, typed bot/human identity, chronological decisive reviews, adversarial Bash cases, verified macOS system aliases, installed/project Stop configuration, Windows Bash dispatch and bounded termination, and evaluation metadata/metric handling. Tests use hermetic Git configuration, local stubs and disposable output directories. Native Bash oracle tests establish shell behavior without live GitHub calls. Packaging tests no longer update the checkout's dist directory.

The merged code reviewer now explicitly checks authorization, tenant isolation and sensitive-data exposure. Claude frontend review uses a foreground general-purpose fork so browser-capable tools can be available; it remains report-only by instructions and host permissions, not a tool-enforced read-only sandbox. The validator checks this per-role configuration. Code/security forks remain Explore. Generic skill invocation defaults are unchanged; discovery does not authorize an external action, and allowed-tools is not a restrictive allowlist.

Earlier forward checks and native smoke results above identify their original candidate. They have not been replayed as a full native-host matrix for these instruction changes. The current local regression pass is on macOS; Windows runner/process changes have mocked coverage and need native confirmation. CI remains disabled. No new model-backed benchmarking, GitHub mutation or live PR merge was part of remediation.

## yb-web-design-system addition (2 November 2026)

Validated on macOS at branch `claude/yb-web-design-system`, base `4fd5548`.

- `python3 scripts/validate.py`: `Validated 11 skills for each platform: names, metadata, footers, shared content, references, payloads, and local Markdown links.`
- `python3 -m unittest discover -s tests`: `Ran 138 tests` … `OK`. The test count is unchanged; the package test now expects eleven skills, and the catalog test requires the new skill's cases and fixtures.
- `python3 -m pytest tests -q`: not run, because pytest is not installed (`No module named pytest`). No dependency was added.
- `python3 scripts/package.py --output-dir <scratch>`: both archives were created with 11 `SKILL.md` files and the skill's 13 references (plus `agents/openai.yaml` in Codex).
- `python3 scripts/install.py --target claude-code --project <scratch>` installed the skill under `.claude/skills/yb-web-design-system`. A headless Claude Code 2.1.301 listing in that project stopped with `OAuth session expired and could not be refreshed`, so native discovery of the new skill was not observed.
- Behavior: nine matched runs (three cases, three arms, one repetition) are recorded in the [evidence file](docs/evidence/2026-11-02-web-design-evals.md), with failures and limitations. The other nine new cases have fixtures and hidden criteria but were not run. No browser rendering, screenshot, screen-reader, or performance measurement was taken for this skill.
- After merging `main` at `51d8c62` (which added `yb-mobile-design-system`), the validator reported `Validated 12 skills for each platform`, the 138 unittest tests passed, and `scripts/package.py` built both archives with 12 skills. The web skill does not reference the mobile skill; how they should relate is an open decision.

