# Targeted frontend probes

Use only sections relevant to the interface and suspected risk. Record what was actually exercised and what remains unknown.

## Forms and overlays

Follow the task with keyboard and supported pointing/touch input. Check native control semantics before proposing custom ARIA; inspect accessible names, grouping, instructions, input purpose, validation timing, and associations between fields and errors. Confirm useful values survive a failed submission and that pending/disabled states explain the next step without permitting unintended repeated actions.

For dialogs, menus, popovers, and drawers, check the appropriate interaction pattern: trigger semantics, initial focus, navigation, dismissal, focus return, background access, and scrolling. Focus trapping applies to modal contexts, not every overlay. Test opening, nested interactions, asynchronous updates, validation errors, and dismissal where supported. Distinguish accessibility-tree inspection from actual assistive-technology testing.

## Responsive layouts and localization

Exercise widths around actual layout transitions, zoom/text enlargement, long content, empty data, and meaningful extremes. Check reading order, clipping, two-dimensional scrolling, touch/keyboard reachability, and whether fixed headers, banners, dialogs, or virtual keyboards hide active controls.

Inspect supported locales for text expansion, date/number/unit formatting, bidirectional content, and directionality. Flag implementation constraints supported by evidence; do not claim a translation is wrong without language or domain knowledge. Test a screen reader or locale only when tooling and expertise permit, and state the limitation otherwise.

## Motion and visual stability

Check whether motion clarifies state changes, respects reduced-motion settings, avoids obstructing input, and remains understandable when interrupted. Verify essential content and controls without relying on animation completion. Consider hover/focus/touch parity and flashing or distracting content where present.

Separate layout shifts, loading delays, and animation smoothness. Reserve space where content changes cause harmful movement; do not prescribe one animation library, duration, or effect for every interface.

## Frontend performance evidence

Tie measurements to build, device/browser, network/CPU conditions, cache state, route, user action, and observation window. Distinguish lab from field data and initial load from interaction performance. Use relevant accepted budgets or current authoritative guidance; a development build or single local sample does not prove production performance.

Trace concrete causes such as blocking resources, excessive asset transfer, expensive rendering/layout, unnecessary updates, request waterfalls, or long-running main-thread work before recommending changes. State tradeoffs: virtualization can affect navigation/accessibility, lazy loading can delay essential content, and caching introduces invalidation concerns. Rerun the affected measurement after a change and preserve functional behavior.
