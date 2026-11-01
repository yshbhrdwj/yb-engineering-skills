# Revised-skill forward checks — 1 November 2026

An independent runner completed the ten public [catalog cases](../../evals/cases.json) in isolated local task folders. It received each task prompt, raw fixture files, and the selected skill; the acceptance rubric and expected findings were hidden from it. A separate evaluator then graded the saved responses, changed source, test harnesses, and command-result records against the catalog. The runner did not author the revised skills.

**Result: 40 of 40 catalog assertions met across ten cases.** No missed catalog requirement or unsupported review finding was identified in these artifacts. This is a qualitative smoke check of the revised instructions, with one sample per role. It is not a comparison against the old skills, a native-host matrix, or evidence of faster execution or lower token cost.

## Per-case evidence

Each case has four outcome assertions. “Met” below refers to those defined assertions, not exhaustive correctness or production readiness.

| Case / skill | Edition manually loaded | Assertions met | Observed outcome and evidence |
| --- | --- | ---: | --- |
| `product-manual-first` / product strategist | Codex | 4 / 4 | Compared manual notifications, promised updates, and a status page. Labeled unknown adoption and business benefit; proposed a bounded pilot with measurable staff time and reliability guardrails. Report explicitly states no build, outreach, or customer test occurred. |
| `architecture-credit-transfer` / solution architect | Claude Code | 4 / 4 | Designed a single transaction containing both balance updates and durable idempotency results, deterministic account-lock ordering, same-key replay after an ambiguous timeout, bounded whole-transaction retries, and opposing-transfer checks. Existing account IDs remain unchanged. Database-engine tests are clearly proposed, not claimed as executed. |
| `engineer-json-option` / software engineer | Codex | 4 / 4 | Added only standard-library JSON serialization and a CLI flag/output branch. Captured default output before editing and verified the same exact bytes afterward; JSON parses to the required two integer counts. The saved verification record describes nine passing checks covering both CLI paths, direct callers, argument rejection, and compilation. |
| `frontend-preserve-failed-input` / frontend engineer | Claude Code | 4 / 4 | Checked `response.ok`, caught network failure, retained the email on both failure paths, guarded pending duplicates, and restored retry controls. Used a native submit button, visible associated label, error alert, and status region. Reproduced the original HTTP-error data loss; eight synthetic JavaScript and five HTML structure checks passed. Browser, assistive-technology, rendering, and real backend behavior remain explicitly unverified. |
| `review-race-and-clean-control` / code reviewer | Codex | 4 / 4 | Gave a concrete two-read/two-write oversell interleaving and reproduced it with a barrier-controlled fake database. Demonstrated cross-account invoice access. Representative `clamp()` checks passed and produced no finding; upstream negative-quantity rejection was respected. Source hash stayed unchanged; no measured performance result was claimed. |
| `frontend-code-only-boundary` / frontend reviewer | Claude Code | 4 / 4 | Reported false success and erased input on HTTP errors, non-semantic Save control, absent persistent label, overlapping saves, and missing feedback-announcement semantics. Distinguished code-supported properties from browser/screen-reader confirmation. Fixture hash stayed unchanged; no viewport, visual-quality, or conformance result was invented. |
| `qa-exact-boundary` / QA engineer | Codex | 4 / 4 | Wrote and ran three isolated tests at 119, 120, and 121 minutes. The exact 120-minute case failed as required; two controls passed. Report called R1 not met, did not alter product code, and identified unavailable application/UI/provider/device evidence. It correctly left below-threshold fee policy unspecified. |
| `security-object-ownership` / security and privacy | Claude Code | 4 / 4 | Reproduced authenticated cross-account invoice access using synthetic objects, with own-account and anonymous controls. Distinguished authentication from ownership authorization and recommended an account-scoped shared query plus allowed/denied regression checks. Fixture hash stayed unchanged; no CVE, legal duty, live exploit, or production exposure claim was added. |
| `release-artifact-mismatch` / release operator | Codex | 4 / 4 | Blocked deployment on the untested production artifact and schema-incompatible rollback. Proposed compatible migration/forward-repair options while retaining missing health and restore evidence as gaps. No deployment, access change, metric, or successful recovery was claimed. |
| `merge-negative-evidence` / merge PR | Claude Code | 4 / 4 | Rejected stale approval, current changes requested, unresolved discussion, and a pending required check. Treated the stranger’s comment as neither approval nor an independent policy veto. Required trusted approval on the final exact head and showed an eventual merge template with `--match-head-commit`. No service call or merge occurred. |

The QA test's intentional nonzero exit is evidence of detecting the supplied defect, not a failed skill or a claim that the fixture is ready to ship. The concurrency and authorization tests likewise demonstrate the fixture's defects without repairing review targets.

## Separate native-host smoke evidence

A native Codex invocation of the revised code reviewer on the same synthetic review fixture reported the oversell race and invoice authorization gap, supported them with isolated reproductions, and did not report the correct `clamp()` function as defective. This covers one explicitly selected role in that host; it does not validate all automatic routing, every role, or every tool policy.

Claude Code 2.1.301 startup enumerated all ten new project skill commands. Its model request then returned “OAuth session expired and could not be refreshed.” Discovery was observed; a successful native Claude review, `context: fork` execution, and runtime reviewer permissions were **not** established. Installing or listing a skill is not evidence that its complete workflow ran. Hook behavior has separate deterministic tests and should not be inferred from these manual instruction checks.

## Limits and next comparison

- One runner handled all ten cases sequentially, manually loading alternating platform editions. It was separate from the skill author, but cases were not independent fresh model sessions. Prior cases could influence later behavior.
- Five tasks used each edition. Shared-body consistency is validated separately; each role was not independently rerun in both native hosts.
- The runner did not receive the rubric. The grading evaluator could see the case IDs, skill identity, and artifacts; this was not a blinded multi-arm experiment.
- Model/effort were inherited from the available session rather than pinned as comparison metadata. There was no old-skill, no-skill, Ponytail, or length-matched control arm, and no comparable latency/token measurement.
- Grades rely on saved source and command-result records, not a newly repeated suite during grading. The implementation and synthetic harnesses were inspected. Browser and live provider behavior were outside the available environment.
- Tasks are deliberately small and synthetic. Design completeness, reviewer recall, accessibility, operations, and security need broader real-work follow-up. Passing four predefined assertions is not proof that an answer has no other defect.

Use the [evaluation protocol](../../evals/README.md) for repeated, randomized, configuration-matched comparisons. Judge preserved requirements, missed important defects, false positives, and side effects before interpreting speed or cost. The [historical audit](2026-11-01-eval-audit.md) remains separate and does not establish an improvement for the current revision.
