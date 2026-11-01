# Interaction and motion

Motion explains change: where something came from, where it went, what caused it. When it does not explain, it decorates, and decoration that delays the task is a defect. Choose libraries only with the stack in view (see frameworks-feasibility); most interface motion needs only CSS transitions.

## Input parity

Every hover affordance has a focus equivalent and a touch path. Hover can preview, never be the only way to reveal an essential action. Style `:focus-visible` for keyboard focus and leave pointer clicks without a ring if the design prefers, but never remove focus indication. Pointer and keyboard activate the same outcome; touch targets meet size and spacing requirements.

## Micro-interactions

A state change should be visible within about 100ms of input to feel direct. Pressed states respond on pointer-down. Toggles move immediately and reconcile on failure with a visible revert and message. Copy-to-clipboard, save, and similar actions confirm in place (label change, check icon) rather than with a distant toast.

## Loading and transitions

Under about one second, show nothing or a subtle pending state on the trigger; beyond that, show skeletons or progress near the content. Keep layout stable as content arrives. Page transitions should be fast and purposeful; the View Transitions API can animate between states and pages, but every transition must be skippable by simply completing quickly, and navigation must not wait for animation.

## Scroll effects

Scroll-linked animation, parallax, and scroll-jacking compete with the user's control of the page. Use reveal-on-scroll sparingly and only for content that is already in the DOM and readable without it; never hide content until an animation runs (it disappears for users with reduced motion, printing, or failed scripts). Never alter scroll speed or direction.

## Disclosure and modals

Expanding content should animate height or opacity briefly (150–250ms) and move focus only when the user asked for the new content. Modals fade and scale subtly from their trigger region; their exit is faster than their entrance. Animate `transform` and `opacity`; animating `width`, `height`, `top`, or `left` triggers layout work on every frame.

## Motion hierarchy and timing

Assign duration by distance and importance: small state changes 100–150ms, component transitions 150–250ms, large surface or page movement 250–400ms. Longer durations read as sluggish in tools used repeatedly. Ease out (fast start, gentle stop) for entering elements, ease in for exits, ease in-out for movement between two on-screen positions. Animate one primary element per change; stagger lists only briefly and cap the total. Define durations and easings as tokens.

## Reduced motion

Under `prefers-reduced-motion: reduce`, replace movement with instant change or a short opacity fade; stop autoplaying, parallax, looping, and flashing effects; keep essential feedback (a progress indicator can still progress). Any animation that starts automatically and lasts more than five seconds needs a pause control regardless of preference (WCAG 2.2.2). Nothing may flash more than three times per second (WCAG 2.3.1).

## Interruption

Animations must be interruptible: a second click on a toggle reverses from its current position, a closing panel can be reopened mid-close, and input is never blocked while motion completes. Streaming data updates must not move targets under the pointer.

## When motion helps and when it hurts

Helps: showing spatial relationships (a panel slides from its trigger), confirming cause and effect, drawing attention to one change among many, smoothing a necessary layout change. Hurts: delaying content, looping in peripheral vision, animating every card on scroll, adding ceremony to frequent actions, and motion that differs from the product's character (a playful bounce in a clinical tool).
