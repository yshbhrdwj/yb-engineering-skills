# Validation of the YB SDLC suite

Updated: 25 September 2026. Ten core skills, each packaged for Claude Code and Codex. Original eight-skill evaluation: 24 September 2026.

## Public repository tooling

The repository adds a standard-library validator, installer, and packaging command. Before publication, 31 helper tests passed locally: 14 validator tests and 17 installer tests. They exercise invalid metadata, missing links, platform drift, payload restrictions, safe installation, explicit updates and backups, dry runs, and preservation of unrelated files. Platform bundles build and pass archive integrity checks. These checks validate packaging and helper behavior; they do not establish skill reasoning quality or UI accessibility.

The GitHub Actions workflow runs the same checks on Linux, macOS, and Windows. Consult the workflow run for the current commit's actual CI results; the historical local skill trials below are separate evidence.

## Structural checks

The final 20 skill files are checked with the skill-creator validator, plus checks for matching yb-prefixed directory/manifest names, descriptions under 200 characters, correct Codex invocation metadata, valid local reference links, complete ZIP contents, and matching core rules across platforms. The shared practice standard is present in every skill. Installed copies are hash-checked against their package sources; superseded personal skill names are backed up before retirement.

## Forward tests and observed behavior

Independent subagents performed small synthetic tasks in local scratch folders. These are qualitative behavior checks, not production assurance or a benchmark against another plugin.

| Skill/check | Observed result |
| --- | --- |
| Product discovery, pre-efficiency | Offered alternative receptionist-product directions and validation questions; did not invent clinic interviews or build the product |
| Compact product handoff | Created one invoice-reminder brief preserving review-before-send, single-owner, INR/timezone, CSV/pause/history, and exclusions; separated accepted capabilities from proposed policies and open architecture choices |
| Compact QA | Existing fixture tests passed 2/2; focused tests exposed the exact two-hour cancellation boundary defect. Combined run: 4 passed, 1 failed. Application code remained unchanged; proposed HTTP performance target stayed unverified |
| Compact release/operations | Rejected readiness based on mismatched commit/digest evidence, schema-incompatible rollback, missing journey checks, and unproven restore; produced an actionable plan without production access or fabricated results |
| Original engineer workflow | Planned a minimal TTL-cache fix, reproduced two failures, and finished with five passing regression tests |
| Original correctness reviewer | Found three seeded contract defects and repeated catalog scans; distinguished derived complexity from measured latency |
| Original design reviewer | Reported no actionable defects in a sound module, retained a justified interface seam, and ran two passing tests |
| Original security/privacy reviewer | Confirmed unauthorized profile export and sensitive logging; identified missing downstream deletion propagation without claiming a statutory or active-incident finding |

The last four behavior tests occurred before compression. Their final compact rules and references were reviewed for preserved scope, contextual SOLID/DSA, evidence, requirements, privacy, and authority. They were not independently replayed in every final platform edition. The best-practices paragraph and yb naming pass were applied after the forward tests and covered by structural/content checks.

## Scope of evidence

The tests ran within this Codex session, not a separate Claude Code runtime. Package installation and content verification do not demonstrate invocation behavior in every host. No real deployments, user interviews, external email, continuous monitoring, or production load tests were performed. The QA fixture's failing test demonstrates defect detection; it is not a claim that the fixture is ready to ship.

The original eight skills’ core instruction text was reduced by 52.1% by word count; [measurement details](TOKEN-EFFICIENCY.md) distinguish this from runtime token savings. The product document became less repetitive while retaining separate architect and engineer handoffs. The workflow preserves stable requirement IDs and distinguishes accepted intent, implementation progress, verification, and authorization.

For real adoption, try a clean diff, a known-defect diff, a small change, a product idea, and a deployment plan in your environment. Correct demonstrated failures with targeted changes rather than adding blanket rules. A [Ponytail scope comparison](PONYTAIL-COMPARISON.md) is included; no head-to-head superiority claim is made.

## Frontend additions — 25 September 2026

The frontend engineer and reviewer received independent qualitative forward tests in isolated scratch folders. The evaluator for each skill received the skill, a user brief, and raw artifacts without an expected answer. The review fixture explicitly required code-only work; the engineering fixture explicitly lacked browser access.

The reviewer identified five code-supported defects: success displayed on HTTP 503, a non-keyboard Save control, input erased on network failure, a fixed-width narrow-screen constraint, and a missing persistent label. It identified focus and status-announcement concerns for runtime verification, preserved the accepted indigo direction, and correctly distinguished HTTP rejection from network failure. It did not invent rendered, assistive-technology, performance, or full-conformance evidence.

The engineer created a compact dependency-free HTML/CSS/JavaScript support form after recording its design and state plan. Native Node tests passed 14/14 for the JSON contract, HTTP status handling, network failure, pending duplicate protection, and retries. Module syntax and static HTML/asset checks passed. Tests establish submission-module behavior; actual DOM input preservation/reset, rendered appearance, keyboard interaction, assistive technology, and live backend integration remain unverified. The result explicitly retained those limits rather than claiming a fully validated UI.

A separate instruction review prompted an explicit rule to use authorized test environments and designated data, preserving the boundary around live payments, destructive changes, and outbound actions. Final frontend cores and their references passed structural validation alongside the existing suite. All ten installed skills in each host were hash-checked against their platform package sources.
