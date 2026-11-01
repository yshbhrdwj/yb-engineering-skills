# Focused design lenses

Use the sections relevant to a suspected consequence. Principles are diagnostic aids, not quotas for findings.

## Clarity and cost of change

Flag misleading names when units, ownership, domain distinctions, or side effects can cause a concrete mistake. Judge function size by entangled policies and fragile reasoning, not line count. Inspect hidden dependencies, temporal coupling, initialization order, mutation ownership, and impossible/invalid states.

Distinguish duplicated syntax from duplicated knowledge: repeated business policy can drift, while superficially similar behavior may have different owners. Check error handling for hidden partial failure or lost causes. Flag inaccurate public contracts or missing rationale for consequential decisions; leave formatting to established tools.

## SOLID in any paradigm

- **Single responsibility:** Name independently changing policies or owners coupled by one unit, and the likely change exposing that coupling.
- **Open/closed:** Identify established variation repeatedly requiring risky edits. A switch is not inherently defective; prefer a small extension mechanism over speculative generality.
- **Substitution:** Give a caller scenario where an implementation changes preconditions, results, exceptions, side effects, or invariants promised by its contract.
- **Interface segregation:** Identify consumers forced to depend on unused capabilities or implement meaningless operations. Split only where consumer needs justify it.
- **Dependency inversion:** Show how volatile infrastructure blocks testing or independent policy changes. Isolate meaningful volatility; an interface for every class adds little by itself.

Challenge deep inheritance, excessive indirection, and abstractions whose maintenance cost exceeds the variation they handle. Prefer domain-native functional/procedural structures where appropriate.

## Architectural contracts

Check cycles, layer violations, misplaced business rules, and cross-module knowledge against stated constraints. Determine ownership of authorization, validation, transactions, caching, and error translation. Multiple defenses may be legitimate; independently duplicated business rules can diverge.

Where affected, trace nullability, API/schema versions, serialization, migration defaults, rollback assumptions, and mixed-version behavior. Check invariants across alternate entry points and whether tests expose observable contracts. Do not prescribe mocks or dependency injection without a concrete testing problem.

## Nonfunctional mechanisms

Identify actual cardinality, operation frequency, growth, and hot paths. Look for repeated scans/sorts, N+1 calls, copying, unbounded materialization, unsuitable indexes, and hidden I/O. Evaluate alternatives against required lookup, ordering, duplicates, memory, concurrency, and maintenance semantics. An asymptotic improvement does not establish a measured speedup.

For applicable latency, reliability, accessibility, security/privacy, compatibility, and operational requirements, identify the mechanism and evidence. Caching brings invalidation/staleness costs; parallelism adds coordination/failure costs; services add deployment and consistency boundaries. Mark unverified properties unknown instead of inventing guarantees.

## Severity fallback

Critical: demonstrated immediate broad compromise, unrecoverable loss, or widespread outage. High: realistic failure of a core requirement or important production path. Medium: bounded defect or substantial design weakness with a likely concrete consequence. Low: limited actionable harm; preferences remain optional. Explain confidence separately from severity.
