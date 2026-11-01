# Frontend implementation and verification

Read relevant sections for complex state/data flows, rendering architecture, or performance work. Inspect actual framework/version guidance and existing project utilities before choosing APIs.

## State, boundaries, and data

- Decide which state belongs in a component, URL, server cache, shared store, or durable storage. Preserve expected back/forward, deep links, refresh, and unsaved-change behavior. Avoid multiple writable copies of the same source of truth.
- Separate fetching, mutation, presentation, and validation enough to reason about failures. Cancel or disregard stale work; define optimistic-update reconciliation/rollback and retry behavior. A disabled button alone is not a server idempotency guarantee.
- Keep side effects out of rendering; respect lifecycle cleanup and scheduling. Use stable identity where item state must survive reordering. Evaluate memoization only when it addresses actual work and dependency correctness.
- For server-rendered/hydrated applications, keep secrets on the server, avoid server/browser divergence, and handle browser-only APIs deliberately. Check serialized props and cache scope for unintended data exposure.
- Validate client input for usability and server input for trust. Respect endpoint contracts, authorization, CSRF/session boundaries, and safe URL/content handling. Never persist sensitive values merely for convenience.

## Performance and resilience

Start with the slow user journey, representative data/device/network, and accepted target. Separate bundle, network, server response, image/font, layout, rendering, and interaction costs. Measure before optimizing when tools permit; label derived complexity and unmeasured hypotheses.

Prioritize critical content and keep geometry stable as assets arrive. Avoid eager offscreen resources, unnecessary blocking scripts, repeated network waterfalls, and excessive work on frequent events. Lazy loading critical content can make loading worse; virtualization adds navigation, focus, search, and measurement tradeoffs. Add dependencies only for a demonstrated benefit.

Use laboratory measurements for reproducible diagnosis and field data for real-user experience; record tool/version, route, build, device/network assumptions, and variability. A single local result does not establish a population percentile or satisfy an unknown budget. Consult current [Web Vitals guidance](https://web.dev/articles/vitals) when using those metrics; do not freeze changing thresholds into this skill.

## Evidence by layer

| Layer | Useful evidence |
| --- | --- |
| Static/code | Relevant type/lint/build checks, contracts, state/cleanup and safe rendering inspection |
| Logic/component | User-observable validation, success/error, pending, cancellation, stale-response and retry behavior |
| Browser | Primary journey, keyboard/focus, navigation, narrow/wide and intermediate layout, zoom, overflow, asset loading |
| Accessibility | Automated checks plus applicable manual semantics, keyboard, focus, and assistive-technology evaluation |
| Visual | Fresh screenshots tied to route/build/viewport/state, compared to accepted direction and incumbent design |
| Performance | Reproducible measurements tied to representative workload and accepted/proposed budget |

Choose the smallest set that can verify the change. Exercise actual user actions instead of implementation details; add regressions for meaningful defects. Do not change snapshot baselines solely to hide unexplained differences. Use mocks deliberately and disclose what integration remains untested.

If browser or device access is absent, say so and separate code-supported conclusions from visual/interaction questions. Report genuine failures and blocked checks with the next useful verification step; do not mark them passed or abandon authorized work that remains possible.
