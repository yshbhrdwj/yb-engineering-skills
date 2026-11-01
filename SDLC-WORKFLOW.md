# Handoffs from idea to operation

Use the smallest relevant set of roles. Stages can overlap; a simple fix does not need a product brief, architecture document and three reviewers.

| Stage | Owner | Input → output |
| --- | --- | --- |
| Shape | `yb-product-strategist` | Evidence and idea → user journey, choices, scope and brief |
| Design | `yb-solution-architect` | Intent and current system → contracts, data, decisions and delivery slices |
| Web design | `yb-web-design-system` | Accepted goals and current UI → web direction, tokens, component contracts and a persisted design document |
| Visual design | `yb-mobile-design-system` | Product intent and current app → direction, tokens, component contracts and acceptance checks |
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

## Frontend routing

Design authorities (`yb-web-design-system`, `yb-mobile-design-system`) are consulted for direction; `yb-frontend-engineer` implements; `yb-frontend-reviewer` inspects independently; `yb-qa-engineer` validates behavior and regressions. The engineer's `references/platform-routing.md` picks the platform and authority, falls back to project design sources when an authority is not installed, and holds the handoff field lists (design → engineering, engineering → reviewer, reviewer → engineering, engineering → QA).

| Scenario | Route |
| --- | --- |
| Unattractive UI that needs a redesign | Design authority for direction → engineer → review and QA by scope |
| Find UI defects | Reviewer first; design authority only if a new direction is needed |
| New web page | Engineer (standard path) with the web authority or project design document; review and QA by risk |
| New mobile screen | Engineer (standard path) with the mobile authority or project design document; simulator/emulator evidence where available |
| Small visual fix | Engineer with existing tokens; nothing else |
| Complex functional change | Engineer → QA; review by risk |
| Complete redesign | Authority → incremental implementation → independent review → QA → targeted recheck |

A skill is a capability, not an agent. Delegate only when the work is separable, independent judgment matters, scope is bounded, the tools exist, and the value exceeds the cost. A self-check is never reported as independent review.
