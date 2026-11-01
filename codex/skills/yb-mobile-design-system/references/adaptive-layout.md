# Adaptive layout

Responsive mobile design is not scaling. When space, text size, orientation, or input changes, decide what reflows, what reorganizes, and what is revealed or hidden.

## Classify by available space

- Use the space the window actually has, not the device model. Split screen, Slide Over, desktop-style windowing, and folding change it at runtime.
- iOS: horizontal and vertical size classes (compact or regular).
- Android: window size classes by width: compact under 600 dp, medium 600–839, expanded 840 and wider; recent Material guidance adds large and extra-large classes for wider windows (verify for the library version).
- Text size is a layout input too: the largest accessibility sizes need the same structural decisions as a narrower screen.

## Decide the response

| Trigger | Response |
| --- | --- |
| Narrow phone (about 320–360 pt/dp) | Collapse multi-column grids; stack button pairs; keep the primary action visible; check long labels |
| Largest text size | Stack horizontal rows; move secondary metadata below titles; let controls grow in height; let titles wrap; scroll rather than clip |
| Medium width | Navigation bar to rail; two-column grids for browsing; wider margins instead of wider text lines |
| Expanded width | List-detail or supporting-pane layouts; reveal filters, metadata, or detail beside the list; constrain reading width |
| Landscape phone | Keep the task's priority; go full-bleed for media and camera; keep the focused field and actions visible in forms; do not lock orientation without an essential reason (WCAG 1.3.4) |
| Keyboard shown | Treat the remaining height as the layout; keep the focused field and the primary action visible; avoid fixed footers that sit under the keyboard |
| Fold or unfold | Preserve state and scroll position; keep content off the hinge; consider tabletop posture for media and capture |
| Long translations | Wrap rather than truncate; let buttons grow; stack button groups; avoid fixed-width labels |

## Reveal, don't enlarge

More space should show more useful structure (a detail pane, filters, comparison, context), not bigger cards. Less space should prioritize the primary task and move secondary content behind clear disclosure.

## Preserve across changes

Touch targets, reachability of primary actions, navigation state, scroll position, selection, and unsaved input must survive rotation, resizing, and text-size changes.

## Implementation hooks

React Native `useWindowDimensions` (width, height, `fontScale`); SwiftUI size classes, `ViewThatFits`, and `dynamicTypeSize`; Compose window size classes from the adaptive library; Flutter `MediaQuery.sizeOf`, `LayoutBuilder`, and `MediaQuery.textScalerOf`. Base decisions on these values, not on platform or device checks.

## Defects to detect

Phone layouts stretched across tablets; reading lines wider than about 75 characters; grids that clip at 320 pt; layouts that break at the largest text; rails or bars that change position without a width reason; state lost on rotation; orientation locked without need; footers hidden by the keyboard.

## Verify

Render the widths around each layout change (for example 320, 390, 430, 600, 840) plus landscape, split screen if supported, and the largest text size. Without rendering, list these as outstanding.

Sources: Apple HIG Layout; Android adaptive layouts and window size classes; WCAG 1.3.4 and 1.4.10 (see sources.md).
