# Accessibility design requirements

Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (W3C Recommendation; current version dated 12 December 2024) and the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Use the project's target version and level; default to WCAG 2.2 AA when none is stated and say so. WCAG 3 is a Working Draft and is not a conformance target.

Write specifications in two labelled groups: **Requirement** (a success criterion at the target level, cited by number) and **Recommendation** (better practice beyond it). Never present a recommendation as conformance, or conformance as proven by design review, heuristics, or automated scans. Scans detect a subset of failures; conformance needs manual evaluation of the built interface.

## Semantics before ARIA

Use native elements first: `button`, `a href`, `input` with `label`, `select`, `details`/`summary`, `dialog`, `table`. They bring keyboard behavior, names, and states for free. ARIA changes what assistive technology is told, not how the element behaves, so a role promises behavior the implementation must then provide; the APG's own rule is that no ARIA is better than bad ARIA. Specify landmarks (`header`, `nav`, `main`, `footer`, labelled when repeated), one `h1`, and heading levels that follow structure.

## Focus order and visibility

- Requirement: focus order preserves meaning (2.4.3); focus is visible (2.4.7); a focused element is not entirely hidden by author content such as sticky headers or cookie banners (2.4.11 Focus Not Obscured (Minimum), AA, new in 2.2).
- Recommendation: a focus indicator at least 2 CSS px thick with 3:1 contrast between focused and unfocused states (the 2.4.13 Focus Appearance AAA criterion), offset outside the control. Specify `scroll-padding` for sticky regions.
- Specify where focus goes after every consequential change: dialog open and close, route change (to the new `h1` or main region), item deletion (to the next item), and form error (to the summary or first invalid field).

## Contrast

- Requirement: text 4.5:1, large text (at least 18pt, or 14pt bold, roughly 24px and 18.66px) 3:1 (1.4.3); user-interface component boundaries, states, and meaningful graphics 3:1 against adjacent colors (1.4.11). Logos and incidental or disabled text are exempt from 1.4.3.
- Method: compute from actual color values (formula in color-surfaces) for every state and mode; report the pair and ratio, or state that it was not computed.

## Target size and pointer input

- Requirement: targets at least 24×24 CSS px, or spaced so a 24px circle centred on each does not overlap another (2.5.8 Target Size (Minimum), AA). Exceptions exist for inline links in text and equivalent alternatives.
- Requirement: any drag action has a single-pointer alternative (2.5.7 Dragging Movements, AA).
- Recommendation: 44×44 CSS px for touch-primary interfaces (the 2.5.5 AAA size).

## Reflow, zoom, and text spacing

- Requirement: content reflows at 320 CSS px width (equivalent to 1280px at 400% zoom) without two-dimensional scrolling, except content that needs it such as data tables and maps (1.4.10); text resizes to 200% without loss (1.4.4); no loss when users set line height 1.5, paragraph spacing 2× font size, letter spacing 0.12em, word spacing 0.16em (1.4.12). Design containers to grow, not to fixed heights.
- Never disable zoom in the viewport meta tag.

## Labels, instructions, and errors

- Requirement: visible labels or instructions for inputs (3.3.2); errors identified in text (3.3.1); suggestions given when known (3.3.3); legal, financial, and data-deleting submissions reversible, checked, or confirmed (3.3.4); names that contain the visible label text (2.5.3); input purpose identifiable via `autocomplete` for user data (1.3.5).
- New in 2.2: do not make users re-enter information already given in the same process (3.3.7 Redundant Entry, A); authentication without a cognitive function test unless an alternative or assistance such as password managers and paste is supported (3.3.8, AA); help mechanisms in the same relative place across pages (3.2.6 Consistent Help, A).
- Specify error association (`aria-describedby`, `aria-invalid`) and announcement (focus move or live region).

## Color independence

- Requirement: color is not the only means of conveying information, indicating an action, or distinguishing an element (1.4.1). Links in body text need a non-color cue (underline) unless they meet 3:1 against surrounding text and gain a cue on hover and focus.

## Tables and modals

- Tables: header cells with `scope`, caption, no layout tables; complex headers need `headers`/`id`. Sortable headers are buttons with `aria-sort` on the header cell.
- Modals: follow the APG dialog (modal) pattern: `role="dialog"` with `aria-modal="true"` (native `<dialog>` with `showModal()` provides this), labelled by its title, focus moved in, Tab contained, Escape closes, focus returned to the trigger.

## Motion and timing

- Requirement: pause, stop, or hide moving or auto-updating content that starts automatically and lasts over five seconds (2.2.2); no more than three flashes per second (2.3.1); adjustable time limits (2.2.1). Recommendation: honor `prefers-reduced-motion` for all non-essential motion (2.3.3 is AAA).

## Localization and RTL

Specify `lang` on the page and on passages in other languages (3.1.1, 3.1.2), `dir="rtl"` support with logical CSS properties, mirrored directional icons, and room for text expansion. Dates, numbers, and currencies follow locale.

## Cognitive load

Recommendations that matter as much as many criteria: plain language, one primary action per view, consistent navigation and naming (3.2.3 and 3.2.4 are requirements), visible progress in multi-step tasks, forgiving inputs (accept spaces in card numbers), undo instead of confirmation for reversible actions, and no time pressure without need.

## Handoff and verification

Each specification lists its requirements by criterion number and the manual checks that will verify them: keyboard-only pass, focus visibility and return, screen-reader name and state check with a named screen reader and browser, 320px reflow, 200% text, text-spacing override, contrast computation, reduced motion. Hand verification of the built interface to `yb-frontend-reviewer` and `yb-qa-engineer`; a design specification is not evidence of conformance.
