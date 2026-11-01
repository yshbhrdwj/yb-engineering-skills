# Domain boundaries, state, and failure

Read the sections matching the affected behavior; do not manufacture findings from absent features.

## Input and contract edges

Consider empty/single/maximum inputs, duplicates, missing/null/malformed values, off-by-one boundaries, sorting stability, filtering, deduplication, pagination, and ordering. Check overflow, precision, rounding, units, normalization/encoding, locale, time zones, clock assumptions, and date boundaries where relevant.

Trace allowed and invalid state transitions, repeated actions, cancellation, returned errors/exceptions, useful causes, cleanup, and user-visible failure. Inspect API/schema/serialization/configuration compatibility, migrations, and mixed-version behavior when affected.

## Concurrent and distributed state

Identify shared state, ownership, synchronization, isolation, and execution ordering. Demonstrate an actual interleaving for lost updates, check-then-act races, deadlocks, stale reads, duplicate processing, or unsafe publication. Check transaction boundaries, atomicity, constraints, compare-and-swap/version checks, and multi-record/system invariants.

Derive the required consistency model from the contract. Trace retries, idempotency keys and lifetimes, deduplication windows, delivery guarantees, and external side effects. Transactional local writes do not guarantee exactly-once remote effects.

For caches, examine key scope, tenant/user separation, invalidation, expiry, stampedes, and allowed staleness. Check timeout/cancellation propagation, bounded retries/backoff, rate limits, backpressure, resource release, and partial-failure recovery.

## Recovery and validation

When owned by the reviewed component, trace crash/restart, graceful shutdown, deploy/rollback compatibility, and dependency outages. Confirm that telemetry exposes failures without sensitive data or unbounded label cardinality.

Select checks by failure mode: boundary examples for domain edges, property/invariant tests for broad input behavior, controlled multi-connection/thread interleavings for races, and fault injection in an authorized isolated environment for partial failures. Assert meaningful outcomes; mocks or a happy-path suite may conceal the suspected defect.
