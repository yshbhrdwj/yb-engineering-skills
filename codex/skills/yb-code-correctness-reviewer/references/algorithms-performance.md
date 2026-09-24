# Algorithms, data structures, and performance

Use when workload or resource behavior can affect a review conclusion.

## Total cost and semantics

Name variables such as records n, edges e, requests r, or returned results k. Inspect the complete call chain: repeated scans, sorting/parsing, library operations, database execution, serialization, allocations/copying, recursion, and network round trips. Include auxiliary storage and stack growth. Distinguish worst-case, expected, amortized, and output-sensitive bounds.

Choose structures by lookup/insertion/deletion, ordering/range queries, duplicate semantics, locality, mutation frequency, and concurrency. Evaluate indexes, hash lookups, heaps, streaming, batching, or bounded buffers against the actual bottleneck. Include constants, small-input behavior, adversarial inputs where relevant, and the cost of maintaining extra state. Do not present alternatives unless the tradeoff matters to the finding.

## Database and runtime behavior

Inspect N+1 calls, join fan-out, query plans, index use, lock contention, pagination, unbounded results, connection pools, and redundant remote operations. A loop's apparent complexity may hide expensive queries.

Look for memory retention, growing queues, missing backpressure, resource leaks, excessive copying, and CPU/I/O saturation. Account for cleanup on error/cancellation and resource ceilings; faster execution that exceeds memory limits may be unacceptable.

## Credible measurement

Use existing traces, profiles, plans, and benchmarks where useful. Compare the same workload/environment and verify correctness in both cases. Record input distribution/size, cache state, warmup, repetitions, background load, runtime/build version, and resource limits where they affect interpretation.

Use distributions or percentiles when relevant; a single run does not establish statistical confidence. Separate measured results from theoretical bounds and expected benefits. If no benchmark ran, state that limitation and the smallest representative measurement needed. Run only proportionate experiments within the authorized scope.
