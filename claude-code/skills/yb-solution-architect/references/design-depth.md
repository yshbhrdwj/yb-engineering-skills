# Detailed architecture checks

Use the relevant portions for system-level or consequential integration, migration, and operational designs. These are design prompts, not mandatory sections or guaranteed requirements.

## Contracts and distributed behavior

Specify operation/payload schemas, identifiers, validation, authorization, ownership, error contracts, versioning, and compatibility at critical interfaces. Trace permission failure and dependency failure alongside the normal path. Explain timeouts, cancellation, retry budgets, deduplication, ordering, idempotency, and partial-work recovery; a local transaction does not make remote side effects atomic.

Define state invariants and their enforcing boundary. Explain concurrent writes, conflict resolution, stale reads, durability, and cache invalidation where they affect the contract. Choose dependency direction and extension points for demonstrated variation rather than speculative reuse.

## Data and protection

Tie schemas, indexes, transactions, and sources of truth to access patterns. Justify data structures using workload size, operations, time/space complexity, and I/O costs. Cover migration, derived copies, retention, deletion, backups, and restore-time handling.

Identify actors, sensitive data, high-impact misuse, tenant/privilege boundaries, and control enforcement. Address authentication, authorization, secrets, encryption, input validation, and audit needs where relevant. Explain collection purpose and minimization; distinguish supplied privacy obligations from unverified legal interpretations.

## Reliability, capacity, and delivery

Describe topology, configuration, dependency health, metrics/logs/traces, actionable alerts, degraded operation, overload limits, backpressure, and failure blast radius. Connect recovery procedures to specified recovery-time/data-loss targets and a verification method: a backup alone does not establish recoverability.

Address feature flags, mixed-version compatibility, migration order, and rollback. For irreversible changes specify the decision point, recovery or forward repair, and residual risk.

Size from measurements or labeled assumptions: peak demand, payloads, fan-out, retention/storage growth, bandwidth, and dependency limits. Identify scaling triggers and a test that could disprove the estimate. Date pricing sources, show ranges when uncertain, and state excluded costs.

Choose acceptance checks from the actual risks: functional, contract/integration, security/privacy, performance, resilience, migration, and recovery. Keep evidence, proposals, and unknowns visibly distinct.
