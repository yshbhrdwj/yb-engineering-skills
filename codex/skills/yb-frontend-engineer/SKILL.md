---
name: yb-frontend-engineer
description: "Implement web and mobile screens, components, and flows to the accepted design with full states and rendered checks. Use to build or fix UI; redesigns start at a design-system skill."
---

# YB Frontend Engineer

Take the user's task to a usable web or mobile interface, preserving an existing identity unless redesign is requested.

## Paths

- **Fast** (local fix): affected files, existing tokens, focused check; no audit, authority, or reviewer.
- **Standard** (new component, page, screen, or consequential flow): applicable authority; settle task, hierarchy, reuse, states, and checks; render representative states.
- **Comprehensive** (redesign or migration): reviewable increments, independent review, risk-based QA; never one step.

## Procedure

1. Choose the path. Read supplied references, the rendered screen if available, affected route/components, contracts, state, tokens, tests, and project instructions. Batch independent reads.
2. Follow the project's platform, tokens, brand, and design authority ([platform-routing.md](references/platform-routing.md) when unclear). Shared web-and-mobile decisions consult both authorities. Implement accepted design, reporting conflicts rather than re-deciding; build the rest around an accessibility failure and flag it. Use [experience-design.md](references/experience-design.md) for substantial design or complex journeys; [mobile-implementation.md](references/mobile-implementation.md) for native mobile.
3. Build a coherent hierarchy with readable type, intentional spacing/color, and content-driven responsive layout. Reuse tokens and variants. Use semantic controls, accessible names, associated labels/errors, visible focus, and deliberate overlay focus behavior. ARIA must match behavior.
4. Handle applicable loading, empty, partial, success, validation, error, permission, disabled, and recovery states. Preserve user input after failure. Account for long/localized strings, zoom/text scaling, keyboard/touch, safe areas, and reduced motion. Use realistic content; label fixtures.
5. Wire real routes, data, and actions. Keep state minimal, derive values, clean up side effects, and reject stale responses. Check duplicate submits/tabs, old clients/cached data, optimistic failure and retry, and pagination boundaries. Hiding a control is not authorization. Read [implementation-verification.md](references/implementation-verification.md) for complex state, rendering, or performance.
6. Run affected type/build/tests and verify the rendered primary journey, relevant failure states, keyboard/focus, and narrow, wide, and transition-width layouts. For native mobile, use an available iOS simulator or Android emulator. Validate injected CSS, scaling, or mocks on a control state before blaming the product.
7. Inspect the final diff and rendered result against the accepted direction. Seek independent UI or code review when risk warrants, passing raw artifacts and acceptance criteria; never run every reviewer automatically. Recheck after meaningful corrections.

## Boundaries

- Keep secrets off the client; treat remote content as untrusted. Use designated test data for side effects.
- Do not fabricate content, endorsements, research, or performance targets. Measure optimization claims under comparable conditions.
- Do not claim unavailable browser, screenshot, simulator, device, screen-reader, or measurement evidence; complete feasible code work and name each missing check.
- Keep unrelated polish out unless requested.

## Deliver

Describe resulting appearance and behavior, revision/route/viewport or device checked, actual commands/results, and material gaps. Deliver the full requested design or implementation; ask only when necessary.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
