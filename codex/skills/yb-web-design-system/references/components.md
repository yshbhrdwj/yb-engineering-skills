# Component design contracts

Read only the family you are designing. Each contract lists what a specification must decide; fill it with the project's tokens. A finished contract covers: purpose, anatomy, variants, type, geometry, semantic color, states, keyboard and focus, accessibility semantics, responsive behavior, loading/error/empty states, common defects, and verification. Prefer a native element that already provides the behavior.

## Contract template

```text
Component: <name>         Purpose: <the one job it does>
Anatomy: <parts, required vs optional>
Variants: <only those with distinct meaning; size and emphasis are separate axes>
Type / geometry: <type role, height, padding, radius, icon size, gap tokens>
Color: <roles per state>
States: rest, hover, active, focus-visible, selected, disabled, loading, invalid (as applicable)
Keyboard / focus: <keys, focus entry and exit>
Semantics: <element or role, name source, state attributes>
Responsive: <what changes, at which container or content condition>
Loading / error / empty: <appearance and next action>
Defects to avoid: <known failure modes>
Verify: <observable checks>
```

## Actions: buttons and links

- Purpose: a button does something; a link goes somewhere. Choosing by appearance instead breaks keyboard, middle-click, and screen-reader expectations.
- Variants: emphasis (primary, secondary, tertiary/ghost, destructive) and size (sm, md, lg) are independent axes. One primary per view or region.
- Geometry: height from label line-height plus padding; horizontal padding about 1.5–2× vertical; icon gap from the spacing scale; inline icons sized to the label's cap height. Buttons beside inputs share their height token. Minimum target 24×24 CSS px (WCAG 2.2 AA), with 44px a common recommendation for touch-primary contexts.
- States: hover and pressed by consistent lightness shift; focus ring offset and 3:1; loading keeps width (spinner replaces or precedes label, label stays for the accessible name) and blocks duplicate activation; disabled explains why nearby when the reason is not obvious.
- Semantics: `<button type="button|submit">`, `<a href>`. Icon-only buttons need an accessible name (`aria-label` or visually hidden text) and usually a tooltip. Toggle buttons use `aria-pressed`.
- Defects: `div` with click handlers; links styled as buttons that submit; full-width buttons on desktop forms; mismatched heights next to inputs; text that looks high because padding ignores the label's descender-free glyphs; destructive actions styled as primary.
- Verify: Tab reaches it, Enter/Space activate buttons and Enter activates links, focus ring visible on every fill, label not clipped at 200% text.

## Inputs: fields, selection, and forms

- Anatomy: visible label (never placeholder-only), optional hint, control, error message, optional character count. Required/optional marked consistently in text, not only by color or a lone asterisk.
- Variants: text, textarea, select, combobox, checkbox, radio group, switch, date, file, search. Use a switch only for immediate on/off settings; a checkbox for choices submitted later.
- Geometry: control height matches buttons; label-to-control gap smaller than field-to-field gap; one alignment edge for all labels; field width hints at expected input length (postal code narrower than street).
- States: rest, hover, focus (ring plus border change), filled, invalid (border plus icon plus message), disabled, read-only (readable, not grayed out).
- Semantics: `<label for>` or wrapping label; hints and errors linked by `aria-describedby`; `aria-invalid="true"` on error; groups in `<fieldset><legend>`; correct `type`, `inputmode`, and `autocomplete` tokens so browsers and password managers help.
- Validation: validate on submit and on blur after first interaction, not on every keystroke while typing. On submit failure, move focus to an error summary that links to each field, or to the first invalid field. Never clear entered values on error.
- Defects: placeholder as label; errors only at the top or only in red; disabling submit with no explanation; splitting one value (phone, card number) into several fields; custom selects that lose type-ahead and native mobile pickers.
- Verify: every control has a programmatic name; errors are announced and associated; values survive a failed submit; autofill works.

## Navigation

- Site navigation: a list of links in `<nav aria-label>`; current page marked with `aria-current="page"` and a visible non-color indicator. Dropdowns use the disclosure pattern (a button with `aria-expanded` controlling a list of links), opened by click or Enter/Space, closed by Escape with focus returned to the button. Do not use `role="menu"` for site navigation: menu roles promise application-style arrow-key behavior that link lists do not provide.
- Hover-to-open alone excludes keyboard and touch users and fires accidentally; if hover opens, click and keyboard must too, with a short close delay.
- Application navigation: sidebar for many destinations or deep hierarchy; top bar for few; tabs only for switching views of the same object (`role="tablist"` with arrow keys, one tab stop). Breadcrumbs for deep hierarchy, in a `nav` with `aria-label`.
- Responsive: collapse to a menu button when items no longer fit at readable size, decided by content (container or measured breakpoint), not a fixed device width. The collapsed panel is a disclosure or a modal dialog; if it covers the page, it needs dialog focus behavior. Keep search and the primary CTA visible outside the collapsed menu when they are the main tasks.
- Defects: icon-only hamburger without name; menu that traps or loses focus; current page shown only by color; mega menus with no keyboard path; navigation that reorders between widths.
- Verify: Tab order follows visual order; Escape closes and returns focus; current page announced; usable at 320px and 200% text.

## Content and data display

- Cards: a card is a grouping device, not a default. Use when items are heterogeneous or browsable; use a list or table when items are compared. A whole-card link needs one real link (stretched with a pseudo-element) rather than nested interactive elements.
- Tables: real `<table>` with `<th scope>` and a `<caption>`; numbers right-aligned in tabular numerals; text left-aligned; headers align with their data. Sort state on header buttons with `aria-sort`. Sticky header for long tables. On narrow screens, keep the table and scroll it horizontally inside a labelled, focusable region, or switch to a stacked layout only when row-to-row comparison is unimportant.
- Lists, badges, avatars, stats: badges carry short status text, not color alone; counts in badges need an accessible name ("3 unread"). Stat tiles show value, label, comparison, and timeframe; a big number without context is decoration.
- Charts: title that states the takeaway, direct labels, accessible summary or data table alternative, no color-only encoding.
- Empty states: explain what will appear here and offer the action that creates it; distinguish "no data yet", "no results for this filter", "no permission", and "failed to load".
- Loading: skeletons that match final geometry for content; spinners only for short, indeterminate actions; progress bars when duration is knowable.

## Overlays

- Modal dialog: prefer native `<dialog>` opened with `showModal()`, which makes the rest of the page inert and closes on Escape. Contract: labelled by its visible title; initial focus on the first meaningful control (or the dialog itself for long content); Tab and Shift+Tab cycle within; Escape closes; focus returns to the invoking element; background does not scroll. Use for decisions that block the task; never for content users need to compare with the page.
- Non-modal popovers, menus, tooltips: the `popover` attribute provides light-dismiss and top-layer stacking. Tooltips supplement, never hold, essential information; they appear on hover and focus, are dismissible with Escape, and stay while the pointer moves onto them (WCAG 1.4.13).
- Drawers and sheets: modal or non-modal by whether the page remains usable; follow the matching focus rules.
- Toasts: for non-blocking confirmation only; announced through a polite live region; never the only place an error or required action appears; persist until dismissed when they contain an action.
- Defects: focus left behind the overlay; close button without name; stacked overlays; scroll bleeding through; dialogs that are too tall for small viewports with no internal scroll.
- Verify: keyboard-only open, operate, and close; focus return; screen-reader name; 320px width and short viewport heights.

## Complex experiences

- **Authentication:** one column, visible labels, `autocomplete="username"`, `"current-password"` or `"new-password"`, show-password toggle, paste allowed. No cognitive tests without an alternative (WCAG 2.2 3.3.8): support password managers, passkeys, or email links. Errors do not reveal which field was wrong when that would leak account existence.
- **Onboarding:** reach first value fast; ask only what personalizes the next screen; show progress for multi-step; allow skipping and resuming; never block the product behind a tour.
- **Checkout:** linear steps with visible progress, editable summary always visible on wide screens and collapsible on narrow, total including fees before the final action, guest checkout where the business allows, address autocomplete, no re-entering known data (WCAG 3.3.7 redundant entry: offer "same as shipping"). Final action labelled with its consequence ("Pay $48.00").
- **Settings:** grouped by user mental model, searchable when long; immediate-apply controls (switches) versus explicit save forms must not be mixed within one group; destructive settings isolated with consequence text.
- **Filtering:** filters near results; applied filters visible as removable chips; result count updates and is announced; "no results" offers to clear the most restrictive filter. On narrow screens filters move into a sheet with an explicit apply action.
- **Data grids:** use a plain table unless cell-level editing or navigation is required; the ARIA grid pattern brings arrow-key navigation and one tab stop, and costs significant implementation. Define column resize, pinning, sorting, selection with checkboxes and range selection, row actions, inline edit and its commit and cancel, and virtualization's effect on find-in-page and screen readers.
- **Drag and drop:** always provide a non-drag alternative (WCAG 2.5.7): move buttons, a menu, or keyboard pick-up and drop. Show a drop target and a placeholder; announce moves through a live region.
- **Command palette:** opened by a documented shortcut and a visible button; combobox pattern with a listbox of results; recent and suggested commands before typing; shortcut hints shown beside commands.
- **Trading and analytics surfaces:** stable layout under streaming updates (tabular numerals, fixed column widths); change shown by sign, arrow, and color, never color alone; update flashes brief and suppressed under reduced motion; order entry separates buy and sell by position, label, and color, confirms consequential orders with a summary, and never moves controls while the user aims at them.
