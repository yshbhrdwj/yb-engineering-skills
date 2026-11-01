# Web and mobile test coverage

Read the section for the platform chosen by `yb-frontend-engineer`'s [platform routing](../../yb-frontend-engineer/references/platform-routing.md). Inspect existing test tooling, configuration, and CI first and extend them; add a framework only for a stated gap the existing tools cannot cover, and only with approval when it adds a dependency.

## Web

- Routing: direct load, refresh, back/forward, deep links with query state, authentication redirects, not-found and permission pages.
- Keyboard: complete the journey without a pointer; focus order, visible focus, and focus return after dialogs.
- Cross-browser: the project's supported browsers, with engine-specific runs (Chromium, WebKit, Firefox) where the tool supports them; name engines not run.
- Responsive: widths around layout transitions, 200% zoom, and long content.
- Visual regression: use the existing tool and baselines, review every diff, and mask dynamic content deliberately. Never update baselines to make failures pass.

## Mobile

- Component tests: React Native Testing Library or the stack's equivalent, queried by role and label, covering states, validation, and pending or disabled behavior.
- iOS and Android interaction, separately where behavior differs: back, sheets, pickers, keyboard, and permission prompts.
- Navigation and deep links: cold and warm start into each linked screen, back stack, invalid parameters, and signed-out entry.
- Gestures: swipe, long press, and drag; conflicts with scrolling and back; accessible alternatives.
- Permissions: first request, denial, "don't ask again", and revocation in settings.
- Lifecycle: background and foreground, process restoration, rotation, and interrupted network.
- Offline: cached reads, queued writes, reconnect conflicts, and user feedback.
- Device layouts and large text: small and large phones, tablets when supported, largest font scale, both themes.
- End-to-end journeys: the project's device-automation tool (Maestro, Detox, Appium, XCUITest, Espresso) on a simulator or emulator; physical devices for hardware-dependent behavior such as camera, biometrics, push, and performance.
- Visual regression: per-platform baselines under the same baseline rule.

## Evidence

Record platform, OS version, device profile or browser, and settings for each result. Simulator and emulator results are not physical-device coverage, a browser preview is not native testing, and component tests do not establish rendered layout. Missing tools or devices are named gaps in the readiness call.
