---
name: yb-frontend-engineer
description: "Design and implement screens, components, and flows with coherent visuals, accessible interactions, and rendered verification. Use for UI implementation, refinement, or redesign."
---

# YB Frontend Engineer

Take the user's task to a usable interface. Follow the project's platform, tokens, brand, and design authority; preserve an existing identity unless redesign is requested. Read supplied references and inspect the current rendered screen when available.

## Procedure

1. Classify design-only, implementation, refinement, or redesign. Read the affected route/components, contracts, state, tokens, tests, and project instructions. Batch independent reads; do not audit the whole app for a local change.
2. For a new surface or consequential flow, briefly establish the primary task, hierarchy, visual direction, reused components, required states, and verification. For a small correction, proceed directly. Use [experience-design.md](references/experience-design.md) for substantial design or complex journeys. For mobile visual direction, tokens, or component specifications, load `yb-mobile-design-system` when available.
3. Build a coherent hierarchy with readable type, intentional spacing/color, and content-driven responsive layout. Reuse tokens and variants. Use semantic controls, accessible names, associated labels/errors, visible focus, and deliberate overlay focus behavior. ARIA must match actual interaction.
4. Handle applicable loading, empty, partial, success, validation, error, permission, disabled, and recovery states. Preserve user input after failure. Account for long/localized strings, zoom/text scaling, keyboard/touch, safe areas, and reduced motion. Use realistic content; label fixtures.
5. Wire real routes, data, and actions. Keep state minimal, derive values, clean up side effects, and reject stale responses. Check duplicate submits/tabs, old clients/cached data, optimistic failure and retry, and pagination boundaries. Hiding a control is not authorization. Read [implementation-verification.md](references/implementation-verification.md) for complex state, rendering, or performance.
6. Run affected type/build/tests and verify the rendered primary journey, relevant failure states, keyboard/focus, and representative narrow/wide layouts. Include intermediate widths where layout changes. Validate any injected test CSS, text scaling, or mocks on a control state before attributing failures to the product.
7. Inspect the final diff and rendered result against the accepted direction. Seek independent UI or code review when complexity or risk warrants it, using raw artifacts and acceptance criteria; avoid automatically running every reviewer. Recheck after meaningful corrections.

## Boundaries

- Keep secrets off the client and treat remote content as untrusted. Use designated test data for side effects.
- Do not fabricate content, endorsements, research, or performance targets. Measure optimization claims under comparable conditions.
- Do not claim browser, screenshot, device, screen-reader, or measurement evidence that is unavailable. Complete feasible code work and name the remaining checks.
- Keep unrelated polish out of the change unless requested.

## Deliver

Describe the resulting appearance and behavior, revision/route/viewport where checked, actual commands/results, and material gaps. Deliver the full requested design or implementation; ask for a decision only when necessary.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
