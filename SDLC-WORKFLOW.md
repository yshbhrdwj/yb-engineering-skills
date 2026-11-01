# Handoffs from idea to operation

Use the smallest relevant set of roles. Stages can overlap; a simple fix does not need a product brief, architecture document and three reviewers.

| Stage | Owner | Input → output |
| --- | --- | --- |
| Shape | `yb-product-strategist` | Evidence and idea → user journey, choices, scope and brief |
| Design | `yb-solution-architect` | Intent and current system → contracts, data, decisions and delivery slices |
| Build | `yb-software-engineer` or `yb-frontend-engineer` | Agreed behavior → code and actual verification |
| Review | `yb-code-reviewer`, `yb-frontend-reviewer`, `yb-security-privacy`, as relevant | Raw artifacts and requirements → grounded findings |
| Verify | `yb-qa-engineer` | Exact candidate and criteria → acceptance evidence and gaps |
| Merge | `yb-merge-pr` | Authorized PR → reviewed, checked and head-pinned merge |
| Operate | `yb-release-operator` | Authorized target and evidence → rollout/recovery and observed results |
| Learn | Relevant roles | Outcomes and incidents → revised decisions and focused improvements |

## Carry only what the next role needs

Pass scope, exact artifact revision, accepted behavior, existing requirement IDs, consequential decisions, actual evidence and unresolved questions. Keep one source of product intent. Reuse existing IDs; do not create a new register for a small task.

Independent reviewers receive the requirements, raw diff/source and target revision, without the author's proposed findings or rationale. They check candidates against real guards and callers, distinguish introduced issues from existing ones, and merge duplicate root causes. A clean report is valid. Unavailable rendering, devices, commands or measurements stay explicit.

Accepted intent, implemented behavior, verified behavior, merge permission and deployment permission are separate facts. Passing tests do not authorize a release. Planning does not authorize external communications or production changes. Prior authorization remains valid within its scope.

## Stop when the evidence is sufficient

Run targeted checks first. Expand tests or investigation when the change, a failure or an unresolved risk warrants it. Fix confirmed findings; do not cycle reviewers until they invent no more suggestions. A new commit invalidates old head-specific review evidence. Recheck the changed scope and project-required gates, then finish or report the concrete blocker.

For interfaces, rendering and interaction evidence complement code review. For state changes, include concurrency, compatibility, interrupted operation/retry and boundary cases that apply. For operations, pin the artifact and environment and verify user behavior and data, not just a successful command.
