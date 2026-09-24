# Conditional test guidance

Read only the sections relevant to the requested validation and identified risks.

## Journeys, accessibility, usability, and metrics

Trace entry to completion: role, navigation, forms, persistence, feedback, cancellation, recovery, empty/loading/error states, and cross-interface transitions. Check API/CLI/UI inputs, outputs, error/status contracts, pagination, retries, idempotency, and compatibility as applicable.

For UI requirements inspect content clarity, responsiveness, localization, keyboard/focus behavior, labels, and relevant assistive technology. Distinguish automated accessibility results, manual checks, and unverified criteria; one passing scanner does not establish conformance.

Distinguish usability inspection from research with representative users. Script completion or model judgment does not demonstrate user comprehension. For `MET` requirements check event meaning, timing, attributes, duplication, collection boundaries, and specified consent behavior; working instrumentation does not prove improved business outcomes.

## Performance, consistency, and resilience

Record workload, data size/distribution, concurrency, duration, warmup/cache state, limits, and measurement method. Separate local observations, theoretical complexity, and representative load evidence. Use consistent conditions for comparisons; report unknown thresholds rather than inventing targets.

Where relevant, exercise permissions/isolation, concurrent writes, duplicate delivery, partial work, resource bounds, timeout/cancellation, retry budgets, backpressure, and recovery under controlled dependency failure. Use deterministic interleavings or reproducible scenarios; a happy path does not demonstrate resilience and inspection does not demonstrate failover.

## Exploratory testing

Define a risk-focused charter, environment, synthetic data, time/scope boundary, and observations. Convert concrete failures into reproducible defects or follow-up checks. Unexplored behavior is a coverage gap, not a manufactured defect. Route specialist security/privacy questions with observed evidence when deeper assessment is necessary.
