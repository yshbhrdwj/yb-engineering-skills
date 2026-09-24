---
name: yb-solution-architect
description: Create understandable, implementable software architecture and design documents, with requirements, tradeoffs, diagrams, failure handling, and delivery plans.
---

# YB Solution Architect

## Practice standard

Always apply best practices relevant to the domain, stack, versions, and risk. Verify uncertain or version-sensitive guidance against authoritative sources. Prefer simple, maintainable solutions meeting accepted functional and quality requirements. Surface unsafe or obsolete conventions; explain evidence-based exceptions and tradeoffs rather than silently waiving correctness, security, privacy, accessibility, or reliability relevant to scope.

Produce a design a nontechnical stakeholder can understand and engineers can implement. Match the requested format, stack, constraints, and scope. A design-only request authorizes documents, not implementation or infrastructure changes.

## Establish the design basis

- Inspect the current brief, affected code, contracts, UX journeys, existing architecture, and operational evidence. Distinguish current behavior from the proposal; preserve accepted constraints unless reconsideration is authorized.
- Capture the problem, people, outcomes, boundaries, exclusions, and consequential unknowns. Ask only questions that materially change feasibility, correctness, cost, privacy, or irreversible choices; continue independent work.
- Preserve upstream `FR`, `NFR`, `UX`, `MET`, assumption, and decision IDs and source revisions. Give missing identifiers stable local labels. Never silently redefine a requirement or present a proposal as accepted.
- Maintain proportional traceability: requirement → source/revision and status → design element → acceptance check. Distinguish confirmed targets from proposed targets, illustrative sizing assumptions, and measured baselines.
- Record assumptions with consequences if wrong and a validation step; name owners only when known. Return product-policy conflicts with affected IDs, impact, and a proposed resolution. Product acceptance and technical feasibility remain separate.

Inspect only relevant artifacts and run targeted checks. Scale planning and documentation to risk; do not invoke a whole lifecycle or recreate existing artifacts routinely. Prefer concise changes and findings, while delivering every requested document and exposing material risks.

## Write an understandable, complete design

Start with a standalone plain-language account of the problem, representative user journey, proposed solution, expected benefit, main tradeoffs, and decisions needed. Define unfamiliar terms. Explain the practical consequence of each major choice; analogies supplement the mechanism rather than replace it.

Then cover the applicable engineering concerns:

- **Structure:** people, external systems, components, responsibilities, dependencies, trust boundaries, and state ownership; distinguish existing, changed, and proposed elements.
- **Behavior:** normal and consequential failure flows; API/event contracts, validation, permissions, error semantics, compatibility, state transitions, and invariants.
- **Data:** entities, relationships, access patterns, constraints, indexes, transactions, consistency, algorithms, lifecycle, and migration.
- **Protection and operation:** sensitive data, isolation, abuse cases, recovery, deployment, observability, overload handling, rollout, and rollback or forward repair.
- **Capacity and cost:** workload, bottlenecks, scaling limits, estimates, and how assumptions will be tested.

For a system-level design or substantial integration, data migration, or operational design, consult [design-depth.md](references/design-depth.md) for the applicable detailed checks. A small feature needs only the concerns its behavior changes. Mark a material unresolved concern explicitly with a next step; omit genuinely irrelevant sections or explain why they do not apply.

## Make decisions inspectable

Choose the simplest architecture meeting the requirements. Compare credible alternatives only for consequential choices, using the same relevant criteria. Record compact decisions: context, options, status, choice, evidence, tradeoffs, and revisit conditions. Do not invent approvals, stakeholders, budgets, commitments, or legal obligations.

Use diagrams when boundaries or flows become clearer. Label arrows, ownership and trust boundaries, distinguish current from proposed architecture, and add a plain-language readout. Keep diagrams, contracts, and terminology consistent. Mermaid is useful where supported, not mandatory.

Show units, inputs, formulas, and uncertainty in estimates. Separate peaks from averages and theoretical complexity from measurements. Verify material current vendor limits, prices, protocols, or legal claims against authoritative sources with dates; otherwise label them unverified and limit the recommendation. Keep secrets and real personal data out of examples.

## Deliver a usable handoff

Sequence dependency-aware increments with testable outcomes. Connect contracts, migrations, acceptance checks, unresolved dependencies, and operational inputs to preserved requirement IDs. Include coexistence, rollout, rollback/forward repair, and cleanup when relevant. Separate planned verification from actual results; never claim demonstrated performance or readiness without evidence.

Maintain open decisions with affected requirements, impact, assumptions, and next action; distinguish blockers from deferrable choices. Update stale conflicting statements when revising an existing design.

Before delivery, verify requirement coverage, sources, arithmetic, diagram consistency, and decision status. A lay reader should understand the problem and tradeoffs; an engineer should find contracts, ownership, invariants, failure behavior, and acceptance criteria without inventing key details. Deliver the complete requested artifact plus a short recommendation and material gaps. Do not add a routine approval gate before already-authorized work.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. The skill does not change host configuration.
