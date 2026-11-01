# Interaction and motion

Interaction quality is felt before it is seen: immediate response, predictable gestures, and feedback that matches the weight of the action.

## Feedback timing

- Acknowledge every touch immediately with a pressed state; delays above about 100 ms feel unresponsive (Heuristic).
- Under about 1 second: keep the user in place and show progress inline. Longer: show progress with context and let people continue or cancel. For known layouts, skeletons beat spinners; delay showing any loader by roughly 150–300 ms to avoid flashes on fast responses.
- Optimistic updates suit reversible, high-success actions (likes, toggles, reordering) when failure is reconciled visibly. Do not use them for payments, orders, medical records, or anything irreversible.
- Success: confirm in place (state change, inline message, checkmark, haptic) rather than a blocking dialog. Reserve full success screens for meaningful completions such as an order or a transfer receipt.
- Errors: show near the cause, say what happened and how to recover, preserve input, and offer retry. Network loss should degrade gracefully with cached content and a clear offline state.

## Touch and pressed states

- Pressed feedback matches the platform: iOS dims or highlights; Android uses ripples or state layers. A shared component can use one brand treatment if it is immediate and visible in both themes.
- Disable controls during submission and show progress inside the control; prevent duplicate submissions without freezing the whole screen.
- Keep at least 8 pt/dp between adjacent targets to reduce mis-taps (Heuristic).

## Gestures

- Every gesture-only action (swipe to delete, long press, pinch, drag to reorder) needs a visible alternative (button, menu, edit mode). Path-based and dragging gestures require single-pointer alternatives under WCAG 2.5.1 and 2.5.7 (Required where WCAG applies).
- Avoid conflicts: horizontal carousels near the left edge compete with iOS back swipe and Android back gestures; maps and charts inside scroll views need clear gesture ownership; scrollable content inside sheets must hand off to sheet dragging only at the top.
- Gesture-driven motion tracks the finger, can be interrupted, and settles based on velocity.

## Motion

- Motion should explain: where something came from, where it went, what changed. Decoration-only motion competes with content.
- Delightful or distracting: delight is rare, short, tied to a meaningful moment (completion, first success), and never delays the next action. Distraction repeats on every visit, plays during a task, or makes people wait.
- Shared-element and container transitions suit list-to-detail relationships; use them where the platform navigation supports them and keep the back transition symmetrical.
- Hierarchy: micro-interactions about 100–200 ms; component transitions 200–300 ms; screen transitions about 300–500 ms or spring-driven equivalents (Heuristic). Use one motion vocabulary across the app, ideally the platform's own springs and curves.
- Animate transform and opacity; animating layout properties is costly and janky on lower-end devices.
- Every animation must be interruptible; a second tap during a transition should act, not queue.
- Reduced motion: replace movement, parallax, zooms, and auto-playing loops with fades or instant state changes. Keep meaningful feedback; remove only the vestibular trigger.

## Haptics

Use haptics to confirm meaningful events: selection changes on pickers, completion of an important action, warnings and errors, snapping into place. Avoid haptics on every tap, on scroll, or during continuous animations. Match the system's meaning (success, warning, error) and respect user settings.

## Keyboard and input

- Correct keyboard type, autofill hints, auto-capitalization, and autocorrect per field (emails, codes, names, amounts).
- Return key moves to the next field or submits; the last field submits.
- Keep the focused field and primary action visible above the keyboard; allow dismissal by scrolling or tapping outside on forms.
- Do not auto-focus fields on screens whose primary task is reading.

## Scroll behavior

- Preserve scroll position when returning from detail screens and switching tabs.
- Large or collapsing headers should collapse smoothly with scroll and not jump when content is short.
- Respect platform overscroll (bounce on iOS, stretch on recent Android). Scroll-to-top on status bar tap (iOS) and active tab re-tap.
- Sticky elements must not obscure focused content, especially at large text sizes.

## Defects to detect

No pressed state; spinners flashing for fast loads; full-screen success modals for routine actions; swipe-only actions; gesture conflicts with system back; animation queues; long, uninterruptible transitions; motion that ignores reduced-motion settings; haptics firing repeatedly; keyboard covering the active field or submit button; lost scroll position.

## Verify

Exercise the interaction on a device or simulator, including a slow network, a failure, a double tap, an interrupted gesture, reduced motion, and the keyboard open. Without a device, list these as outstanding checks.

Sources: Apple HIG Motion, Gestures, Haptics; Material 3 Motion and Interaction states; WCAG 2.2 (see sources.md).
