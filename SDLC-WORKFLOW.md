# Workflow from idea to operation

Use the smallest relevant set of roles. New products need more discovery and design than small fixes; incidents start with diagnosis and authorized containment. Stages can iterate or overlap.

| Stage | Owner | Input → output |
| --- | --- | --- |
| Discover and shape | `yb-product-strategist` | Idea/evidence → concepts, validation, UX journeys, scope, product brief |
| Design architecture | `yb-solution-architect` | Brief/current system → contracts, data/failure model, decisions, delivery plan |
| Build | `yb-software-engineer` | Requirements/design → implementation, tests, actual verification |
| Design and build frontend | `yb-frontend-engineer` | Product journeys/architecture/brand → visual and interaction design, working UI, verification |
| Review frontend experience | `yb-frontend-reviewer` | UI/code/criteria → evidenced UX, visual, accessibility, responsive, interaction findings |
| Verify quality | `yb-qa-engineer` | Candidate/acceptance criteria → test evidence, defects, UX/NFR gaps, QA recommendation |
| Review maintainability | `yb-code-design-reviewer` | Diff/design → evidence-based structure and maintainability findings |
| Review behavior | `yb-code-correctness-reviewer` | Diff/workload → correctness, algorithm, concurrency, failure findings |
| Review trust and data | `yb-security-privacy` | Relevant artifacts → security/privacy findings and remediation evidence |
| Release and operate | `yb-release-operator` | Candidate/evidence → rollout/recovery, authorized execution, observed operational results |
| Learn and maintain | Product + operations + relevant specialists | Outcomes/feedback/incidents/cost → revised brief, maintenance, scaling, deprecation or retirement |

## One shared handoff

For consequential work, carry the current artifact revision, scope, stable requirement IDs, decision status, actual evidence, open questions, and next role. Reuse project IDs or `FR-` for functionality, `NFR-` for quality, `UX-` for experience, `MET-` for metrics, and `RISK-` for risks. Architecture adds `ADR-`. Do not copy competing requirements registers.

An accepted requirement may be unimplemented. Implemented behavior may be unverified. Passing checks do not approve product assumptions or authorize production changes. Record these states separately.

## Product document

The idea skill produces one readable brief covering the problem, users, alternatives, value/business hypothesis, journeys and states, first-release boundaries, acceptance criteria, outcome measures, validation, and open decisions.

Its architect section states boundaries, invariants, data/trust needs, constraints, quality targets and their status, and decisions requiring technical analysis. Its engineer/QA section provides prioritized slices, behavior, acceptance examples, UX states, dependencies, and architecture decisions still needed. It does not invent an architecture to make a document appear ready.

## Verification and release

Reviewers form initial assessments independently, then merge duplicate root causes. Code is reviewed by an agent that didn't write it, or the review is labeled a self-review. Before merging, read every review comment and get any review bot's review of the latest commit. QA consolidates behavior evidence and gaps; operations checks the exact candidate/environment, migrations, rollback or forward repair, and observable release results. Product acceptance belongs to the relevant decision owner. Missing ownership stays explicit.

Security, privacy, accessibility, and operability begin during definition/design and are verified where appropriate. A late checklist cannot substitute for missing policy. Follow actual authorization for deployments, external communications, live-data changes, or retirement. Do not create monitoring schedules merely because operations appears in the workflow.

Feed measured results back into product choices. Preserve requirement IDs and record affected designs, code, tests, and release plans when intent changes.

## Frontend specialization

The frontend engineer owns visual direction, responsive layout, component behavior, and frontend integration for the requested surface. Product strategy owns product intent; architecture owns system boundaries and contracts. Use the general software engineer for broader implementation only when needed.

The frontend reviewer assesses the actual user experience independently, including meaningful states and input methods. Generic code reviewers cover structure or algorithm/correctness concerns; QA consolidates acceptance evidence. Reuse existing checks and deduplicate findings by root cause. Code-only or screenshot-only review leaves explicit interaction and rendering gaps. No role may claim measured usability, accessibility conformance, or production performance without sufficient evidence.
