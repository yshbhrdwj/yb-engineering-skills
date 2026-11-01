# Layout, spacing, and responsive behavior

Layout expresses priority. Responsive design re-expresses the same priority under different space and input: adapt, do not scale.

## Grid and flex

Use CSS grid for two-dimensional page structure and aligned collections; flexbox for one-dimensional rows of controls and content that should size to itself. A 12-column grid suits marketing pages that need many asymmetric splits; applications are usually better served by named regions (`header`, `nav`, `main`, `aside`) with explicit track sizes. `grid-template-columns: repeat(auto-fill, minmax(min(100%, 18rem), 1fr))` gives a collection that reflows without breakpoints; the inner `min()` prevents overflow on narrow screens. Give flex and grid children `min-width: 0` where text must truncate or wrap, because their default minimum is their content width and they will otherwise push the layout wider.

## Containers and gutters

Set content widths by content, not viewport: prose about `65ch`; forms about 32–40rem; application content can be fluid with a sensible maximum for line length in text-heavy areas. Define a small set of container widths as tokens. Gutters scale gently with viewport (`clamp(1rem, 4vw, 2rem)`) so narrow screens keep content area and wide screens keep air.

## Section and component spacing

Separate three tiers: inside components (tight, from the spacing scale's small steps), between related components (medium), between page sections (large, often fluid). Marketing pages use generous section spacing to pace a story; applications compress section spacing because users scan repeatedly. Empty space must group or emphasize something; space that only fills a viewport is padding, not design.

## Density

Density is a product decision: frequency of use and data volume justify compactness. Offer density as tokens (row height, control height, cell padding) rather than per-screen overrides. Compact data rows around 32px and comfortable rows around 44–48px are typical; touch-primary contexts need larger targets regardless of density.

## Alignment

Align to edges that the eye follows: text baselines, the left edge of text (not of icons or borders), and the optical center of shapes. Inputs in a form share one left edge for labels and one for fields. Numbers align right (with tabular numerals) so magnitudes compare; text aligns to its reading start. Fix misalignment by correcting the shared component or token, not with one-off pixel offsets; where a one-off optical correction is truly needed, encode it in the component.

## Breakpoints

Set breakpoints where the content breaks, not at device widths. Find them by widening the layout until something looks wrong: a measure becomes too long, a navigation no longer fits, a second column becomes useful. Express them in `rem` or `em` so they move with text zoom. Check intermediate widths (for example between a tablet and laptop arrangement), not just the endpoints; most layout defects live there.

Container queries (`container-type: inline-size`, then `@container (min-width: 30rem)`) let a component respond to the space it is given rather than the viewport. Prefer them for reusable components that appear in sidebars, cards, and full-width regions; keep viewport media queries for page-level structure.

## What changes, and when

- Reflow before you hide: stack columns, wrap toolbars, move secondary panels below primary content.
- Change navigation when its items no longer fit at a readable size; collapsing below a fixed device width that still has room is a defect.
- Collapse support content (filters, metadata, secondary actions) into disclosures; never collapse the primary task.
- Add columns when content benefits from comparison, not because space exists. Ultra-wide screens need a maximum content width or a genuinely useful extra region, not stretched lines.
- Keep the primary action reachable at every width: sticky only when the page is long and the action is the goal (checkout, compose).
- Change density with input: coarse pointers need larger targets and spacing (`@media (pointer: coarse)`), fine pointers can be denser. Do not infer touch from width.

## Zoom, text scaling, and reflow

At 400% zoom a 1280px viewport behaves like 320 CSS px; content must reflow into one column without horizontal scrolling, except content that inherently needs two dimensions (data tables, maps, diagrams), which may scroll within its own container. Sticky headers and footers consume more of the viewport as zoom increases: cap them or let them scroll away at small heights (`@media (max-height: …)`).

## Sticky, fixed, and nested scrolling

Every sticky or fixed element costs reading space and can obscure focused elements (a WCAG 2.2 concern). Use `scroll-padding-top` equal to the sticky header height so anchored and focused content is not hidden. Avoid nested scroll containers in the same axis; if unavoidable (a scrolling table in a scrolling page), make the inner region visibly bounded, keyboard focusable, and labelled. Use `overscroll-behavior: contain` on overlays and panels to stop scroll chaining.

## Viewport units and browser chrome

`100vh` on mobile includes the area behind collapsing browser toolbars, so full-height heroes overflow. Use `svh` for content that must fit the smallest viewport, `dvh` when it should track the toolbar (with care, because it resizes during scroll), or `min-height` rather than `height`. Respect safe areas in embedded webviews and installed apps with `env(safe-area-inset-*)`. Embedded webviews may lack hover, have no address bar, and limit `position: fixed`; design primary flows to work without those assumptions.

## Orientation

Landscape on phones has little height: avoid tall fixed headers and full-height sections; let content scroll. Do not lock orientation for web content unless essential.

## Layout stability

Reserve space for everything that loads later: images and embeds via `width`/`height` or `aspect-ratio`, ads and banners via fixed slots, web-font swaps via metric-matched fallbacks, async content via skeletons of the same size. Never insert content above what the user is reading unless they asked for it.
