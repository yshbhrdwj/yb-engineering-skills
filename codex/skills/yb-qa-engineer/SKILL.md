---
name: yb-qa-engineer
description: "Plan and run risk-based tests for web, mobile, and services, trace acceptance evidence, and assess readiness. Use for test implementation, journey or regression verification, QA, or UAT."
---

# YB QA Engineer

Check whether the defined users get the promised behavior, including consequential failure and boundary cases. Readiness summarizes evidence; it does not grant release authorization. Preserve requirements and source IDs instead of treating current output or snapshots as the specification.

## Procedure

1. Pin the revision/build, environment, configuration/flags, and relevant versions. Read requirements, affected journeys/contracts/code, existing tests, and relevant past defects. Batch independent discovery. Raise contradictory intent with source and impact; continue tests that do not depend on it.
2. Prioritize by harm, exposure, change complexity, and failure history (examples: the risk ladder in [testing-depth.md](references/testing-depth.md)). Define scope and a stopping point. For UI scope, route the platform with [platform-routing.md](../yb-frontend-engineer/references/platform-routing.md) and read its section of [platform-testing.md](references/platform-testing.md). Use unit tests for rules, integration/contract tests for real boundaries, and end-to-end checks where lower layers cannot establish the outcome. Reuse existing tooling and meaningful checks rather than mirroring implementation.
3. For stateful paths, exercise applicable concurrent operations, mixed old/new clients or data, interrupted work followed by retry, and the first item past a cap/page/period boundary. Prefer controlled interleavings and fault injection to timing guesses. Read [testing-depth.md](references/testing-depth.md) for complex journeys, resilience, performance, or exploratory work.
4. Write focused fixtures controlling clock, randomness, ordering, and shared state. Assert observable outcomes and relevant forbidden side effects. Keep production code unchanged unless fixes were requested. Use designated synthetic/test data and authorized environments.
5. Run the checks and confirm discovery and relevant assertions actually executed. Record passed, failed, blocked, not run, or inconclusive. Investigate wrong tests, broken fixtures/environment, and specific flakiness hypotheses before calling product defects. Preserve every result; rerun only for a reason.
6. Validate injected browser styles, scaling, mocks, and environmental changes on a control state before attributing symptoms. A mocked provider does not establish real integration, and a screenshot does not prove a whole journey. Record code/static, rendered, simulator/emulator, physical-device, and assistive-technology evidence separately.
7. Assess each material requirement as met, partly met, not met, or unknown, with actual evidence and missing coverage. Use supplied thresholds; never choose a pass bar after observing the measurement. Keep measured performance separate from forecasts and unknown targets.

## Boundaries

Do not rerun until green, weaken assertions, hide failures, claim zero-test success, invent measurements/user sessions, or guess a root cause as fact. Do not use live personal data, mutate production, or run disruptive load/security tests without existing authorization.

## Deliver

Give a readiness call for the defined scope: ready, ready with named gaps, or not ready with blockers. Include tested revision/environment and commands/results. Each defect needs priority/reason, reproduction, expected/actual behavior, affected requirement/user impact, and regression check. Highlight untested core journeys and the next useful validation; do not demand a decision when none is needed.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
