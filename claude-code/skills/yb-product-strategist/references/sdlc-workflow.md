# SDLC routing and handoffs

Use for end-to-end coordination. Route to the smallest useful set of specialists; the lifecycle is iterative, not a mandatory ceremony.

## Shared contract

Carry artifact version/source, outcome/scope, stable requirement IDs, accepted/proposed decisions, actual evidence, unresolved assumptions, dependencies, and next role. Preserve project IDs or `FR-`, `NFR-`, `UX-`, `MET-`, `RISK-`; architecture adds `ADR-`. Link requirements to design, implementation, tests, and release evidence rather than duplicating stale tables.

**Accepted decision**, **implemented behavior**, **verified behavior**, and **authorized release** are separate states. Readiness reports evidence, not a new permission requirement. User scope and host permissions still govern execution.

| Stage | Skill | Principal handoff |
| --- | --- | --- |
| Discover, validate, define UX/scope | `yb-product-strategist` | Idea/evidence → product brief, journeys, requirements, metrics, assumptions |
| Design system | `yb-solution-architect` | Brief/current system → contracts, data/failure model, decisions, delivery increments |
| Implement | `yb-software-engineer` | Requirements/design → working slices, migrations, tests, actual checks |
| Design/build frontend | `yb-frontend-engineer` | Journeys/brand/contracts → visual system, interactive UI, responsive/accessibility evidence |
| Review frontend | `yb-frontend-reviewer` | Rendered UI/code/criteria → grounded UX, visual, accessibility, interaction findings |
| Verify quality | `yb-qa-engineer` | Requirements/build/risks → test evidence, defects, UX/NFR coverage, residual gaps |
| Review design | `yb-code-design-reviewer` | Diff/design → maintainability and architectural findings |
| Review correctness | `yb-code-correctness-reviewer` | Diff/workload → behavior, algorithm, concurrency, failure findings |
| Assess trust/data risks | `yb-security-privacy` | Relevant lifecycle artifacts → threat/privacy findings and remediation evidence |
| Release and operate | `yb-release-operator` | Candidate/evidence → rollout/recovery, executed checks if authorized, operational record |
| Learn, maintain, retire | Product + operations + affected specialists | Outcomes/incidents/cost → revised brief, maintenance, deprecation/export/deletion plan |

Check skill availability; missing specialists remain explicit gaps, with bounded fallback work assigned by competence. No hard dependencies or automatic orchestration are implied.

## Apply proportionately

- Small fixes may start at diagnosis/testing; new products benefit from discovery/design. Incidents start with authorized containment, not a product workshop.
- Security, privacy, accessibility, and operability start early. Product acceptance, code review, and test execution serve different purposes.
- Independent reviewers form initial findings from raw artifacts, then reconcile duplicate causes and conflicting evidence. Delegate only when useful.
- Contradictory requirements return to product/architecture. Implementation convenience does not authorize dropping accepted behavior.
- Release planning does not authorize deployment, external messages, or destructive data changes. Do not create unrequested monitors.
- Feed real usage, support, incidents, reliability, and cost back to product decisions. Explicitly assign monitoring, recovery, support, and retirement owners; unknown ownership is a gap.

Frontend specialization preserves product intent and architecture boundaries. Use the frontend engineer for surface design and implementation; the frontend reviewer independently checks experience and interaction evidence. QA consolidates acceptance coverage. Reuse checks and deduplicate root causes instead of running every reviewer automatically.
