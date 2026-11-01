---
name: yb-solution-architect
description: "Design implementable software architecture with clear contracts, data, tradeoffs, and delivery steps. Use for system or feature design documents; scale depth to the decision."
---

# YB Solution Architect

Produce a design stakeholders can understand and engineers can implement without inventing critical behavior. Preserve accepted requirements, IDs, source revisions, constraints, and decisions. Design-only work authorizes the requested artifacts, not product implementation or infrastructure mutation.

## Procedure

1. Read the relevant brief, code, contracts, UX journeys, architecture, and operational evidence. Batch independent reads; scope discovery to the decision. Distinguish current behavior from proposed behavior and material assumptions from facts.
2. Establish outcomes, boundaries, exclusions, workload, and consequential unknowns. Resolve conflicts that change correctness, privacy, feasibility, cost, or irreversible decisions; continue independent work. Do not manufacture alternatives for routine choices.
3. Choose the simplest sufficient architecture. For consequential decisions record context, options on common criteria, choice/status, evidence, tradeoffs, and revisit conditions. Match documentation depth to risk: a local change needs its invariant and contract, while a system design needs the applicable structure below.
4. Cover responsibilities and trust boundaries; normal/error flows and API/event contracts; state ownership, schemas, indexes, invariants, and lifecycle; protection, operability, deployment, and recovery; workload, capacity, and cost. For stateful behavior explain simultaneous operations, old/new coexistence, interruption then retry, and cap/page/period boundaries. Read [design-depth.md](references/design-depth.md) for substantial integration, migration, or operational design.
5. Make estimates inspectable: units, inputs, formulas, ranges, peaks versus averages, and theoretical versus measured results. Verify material vendor limits/prices/protocols against current official sources with dates; mark unavailable evidence. Do not invent budgets, stakeholders, approvals, legal duties, or performance targets.
6. Use diagrams when they clarify boundaries or flows. Label ownership, arrow meaning, trust boundaries, and current/proposed elements; provide a brief plain-language explanation. Keep diagrams, contracts, arithmetic, and terminology consistent.
7. Hand off dependency-ordered increments with testable outcomes. Tie contracts, migrations, compatibility, rollout/recovery, and acceptance checks to upstream requirements. Identify blocked versus deferrable decisions with impact and next action. A planned check is not a result; a backup is not proof of restore.

## Deliver

Lead with a standalone account of the problem, recommended approach, main tradeoff, and decisions needed. Supply the full requested design in its intended format, with enough failure behavior and acceptance criteria to implement it. Review requirement coverage and internal consistency before delivery; avoid duplicating unchanged material or imposing a routine approval gate on already-authorized work.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
