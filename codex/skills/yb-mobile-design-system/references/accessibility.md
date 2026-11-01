# Accessibility

Accessibility is a design input in every mode. Label requirement strength accurately: WCAG 2.2 AA is the common technical benchmark; legal duties depend on jurisdiction and sector (for example the European Accessibility Act for covered services since June 2025); platform guidance adds recommendations.

## Requirement map

| Topic | Benchmark | Strength |
| --- | --- | --- |
| Text contrast 4.5:1, large text 3:1 | WCAG 1.4.3 | Required where WCAG applies |
| UI boundaries, focus, state indicators 3:1 | WCAG 1.4.11 | Required where WCAG applies |
| Color not the only signal | WCAG 1.4.1 | Required where WCAG applies |
| Text scales without loss | WCAG 1.4.4; Dynamic Type; Android font scale | Required (WCAG) and Guideline (platforms) |
| Names, roles, states, values exposed | WCAG 4.1.2 | Required where WCAG applies |
| Single-pointer and non-drag alternatives | WCAG 2.5.1, 2.5.7 | Required where WCAG applies |
| Target size 24 × 24 CSS px minimum | WCAG 2.5.8 | Required where WCAG applies |
| Targets 44 pt (iOS), 48 dp (Android) | Platform guidance | Guideline |
| Status messages announced | WCAG 4.1.3 | Required where WCAG applies |
| Orientation not locked without need | WCAG 1.3.4 | Required where WCAG applies |
| Reduced motion honored | WCAG 2.3.3 (AAA); platform settings | Guideline |

WCAG was written for web content; WCAG2ICT guidance maps it to native apps. State that mapping instead of overstating conformance.

## Text scaling

- Test the largest standard size and the largest accessibility size (iOS AX5; Android 200%). Primary content must remain readable without truncation or overlap.
- Switch layouts at large sizes: stack horizontal rows, move secondary metadata below titles, let buttons grow in height, allow multi-line navigation titles, and make cards scroll rather than clip.
- Cap scaling only for elements that cannot reflow and remain readable at the cap; never cap body text.

## Screen readers

- Every interactive element has a concise name (verb or noun, not "button"), the right role, and its state (selected, checked, disabled, expanded) and value (slider position, progress).
- Group related content into one element where it reads as one item (a list row with title, subtitle, and price); expose secondary actions as custom actions instead of extra focus stops.
- Reading order follows visual order; when a screen, sheet, or dialog opens, focus moves to it, and it returns to the trigger on close.
- Announce asynchronous results (saved, failed, new messages) without moving focus unnecessarily.
- Decorative images and icons are hidden; meaningful images have descriptions; charts provide a text summary or data table.

## Motor and touch

- Minimum targets with spacing; primary actions reachable without precision gestures.
- Every gesture has a visible alternative; time limits can be extended or disabled.
- One-handed use: place frequent and primary actions in the lower part of the screen on phones; avoid critical actions only in top corners (Heuristic).
- Support external keyboards and switch access focus order on tablets.

## Vision settings

Honor bold text, increased contrast, reduced transparency, color filters, Smart Invert (exclude media), and dark mode. Never rely on hue alone for state or status.

## Cognition and recovery

Plain language, one primary action per step, visible progress in multistep flows, undo for destructive actions where possible, confirmations that name the consequence, forgiving input formats, preserved input after errors, no surprise timeouts.

## Localization

- Allow 30–40% text expansion for languages such as German and Finnish; avoid fixed-width labels.
- Support right-to-left layouts with logical leading/trailing properties; mirror directional icons only.
- Format dates, numbers, currency, and units with locale APIs; avoid concatenated sentences.

## Defects to detect

Icon-only buttons without names; rows read as five separate fragments; focus left behind a sheet; errors only in color or only visual; text clipped at large sizes; global font-scale caps; swipe-only actions; fixed-height buttons; placeholder-only labels; status changes that are silent to screen readers.

## Verify

Rendered checks: largest text sizes, dark and increased-contrast modes, VoiceOver and TalkBack passes on the primary journey, Accessibility Inspector or Accessibility Scanner where available. Source checks: roles, labels, states, grouping, and announcements. An accessibility tree is not a screen-reader test, and automated scans cover a subset; report what was actually run.

Sources: WCAG 2.2; WCAG2ICT; Apple HIG Accessibility; Android accessibility guidance; European Accessibility Act (see sources.md).
