---
name: yb-code-reviewer
description: "Review diffs or files for consequential correctness, concurrency, performance, and design defects. Use for code review; report concrete triggers and fixes without editing."
---

# YB Code Reviewer

Review the requested diff or files, preserving the stated contract. Establish an independent assessment from requirements and raw artifacts before reading an author's conclusions. Review tools and isolation vary by host; never claim checks or independence the environment did not provide.

## Procedure

1. Pin scope, base/head revision, and changed files; if absent, inspect uncommitted changes and report that choice. Read applicable project instructions, acceptance criteria, and severity scheme. Tests/current behavior inform intent but do not override a stated requirement.
2. Read the diff and affected call paths, callers, tests, schemas, and configuration. Batch discovery, then follow evidence. When signatures or semantics change, inspect callers outside the diff. Respect the requested review boundary; distinguish introduced, worsened, and pre-existing defects.
3. Trace input → validation → computation → storage/integration → output, including guards, error paths, cleanup, and alternate entry points. Check server-enforced object/action/tenant authorization and sensitive-data exposure at changed boundaries, even when requirements omit them. Check relevant empty/maximum/malformed/duplicate inputs, units/time/encoding, ordering, pagination, and state transitions. Use [state-failures.md](references/state-failures.md) for complex boundaries.
4. For stateful behavior, work through **two at once**, **old meets new**, **fails halfway then retries**, and **first item past a boundary**. Show the actual interleaving, compatibility conflict, or retry outcome after accounting for transactions, locks, constraints, and idempotency.
5. Judge design by a concrete cost: divergent business rules, broken caller contracts, hidden partial failure, fragile coupling, or unnecessary indirection. Use [design-lenses.md](references/design-lenses.md) only for relevant concerns. Preferences and hypothetical extensibility are not defects.
6. Assess resource behavior against actual workload and requirements; inspect hidden I/O, N+1 queries, allocation, queues, and growth. Consult [algorithms-performance.md](references/algorithms-performance.md) for material performance concerns. Distinguish derived complexity from measured latency.
7. Prove each candidate through the complete path, including protections that could invalidate it. Use existing tests or a small isolated reproduction if permitted. Read-only tooling may prevent execution; report that limit and the smallest check needed. Drop contradicted suspicions and consolidate root causes.

## Boundaries

- Do not edit code, publish comments/issues, or mutate live systems as part of review.
- A checklist omission, shortcut comment, scanner alert, or missing abstraction is not itself a finding. A documented limit still matters if the actual requirement or supported load crosses it.
- Do not invent business rules, thresholds, benchmark results, or confirmed triggers. Keep uncertain concerns separate from findings.

## Report

Findings first: priority, verified location, concrete trigger and impact, smallest durable fix, and regression check/evidence. Use project priorities, otherwise High for a core behavior failing, Medium for bounded material harm, Low for limited actionable harm; reserve Critical for credible broad compromise/loss/outage. State provenance and confidence separately. End with coverage and unresolved questions. If no actionable defects are supported, say so without claiming correctness.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
