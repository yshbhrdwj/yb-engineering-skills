# Typography

Decide type from content and display context: what is read, how long, at what distance and density, in which languages. A scale chosen before the content is known is arbitrary.

## Families and identity

Choose a family for its job, then its voice. Text faces need open apertures, a generous x-height, distinct `Il1` and `0O`, and multiple weights; display faces may be idiosyncratic because they are read in short bursts. One family with a good weight range is often stronger than a pairing. Pair only when roles differ clearly (a serif display with a sans text, or a sans with a monospace for code and data), and match x-height and mood so the switch reads as intentional.

Brand distinctiveness rarely comes from an exotic font alone; it comes from how size, weight, case, and spacing are used. Avoid the reflex of the same few geometric sans faces for every product unless they genuinely fit.

## System versus web fonts, and loading

A system stack (`system-ui`, `-apple-system`, `Segoe UI`, `Roboto`, sans-serif) costs nothing to load and feels native; it suits dense applications and tools. Web fonts buy identity at a cost: each family and weight is a download that can delay text or shift layout. Budget files: usually one variable file per family, subset to the needed scripts, self-hosted where the stack supports it, with `font-display` chosen deliberately (`swap` shows fallback text immediately; `optional` avoids late swaps on slow connections). Reduce swap shift by matching the fallback's metrics with `size-adjust`, `ascent-override`, and `descent-override` in the fallback `@font-face`. Framework font tools can do this automatically (see frameworks-feasibility).

## Variable fonts and optical sizing

A variable font replaces several static weights with one file and permits intermediate weights (for example 450 for body on dark backgrounds, where text looks bolder than on light). Families with an `opsz` axis adjust stroke contrast and spacing to size; keep `font-optical-sizing: auto` unless a deliberate effect needs otherwise.

## Scales

Use a modular ratio as a starting point, then adjust steps to roles. Tighter ratios (1.125–1.2) suit dense applications where many levels must coexist; wider ratios (1.25–1.333 and up) suit editorial and marketing pages with few levels and dramatic display type. Name steps by role (`display`, `heading-1`, `body`, `caption`, `label`), not by pixel.

Fluid type interpolates between a minimum and maximum: `font-size: clamp(2rem, 1.2rem + 2.5vw, 3.5rem)`. Always include a `rem` term so user font-size preferences still scale the result; a pure `vw` value ignores zoom and fails text-resize expectations. Keep body text fixed or nearly fixed (about 1rem to 1.125rem); fluidity belongs to display sizes. Application UI rarely needs fluid type at all.

## Roles

- Body: about 16–18px equivalent on the web for reading; dense application UI may use 14px for secondary data, rarely smaller for anything users must read.
- Headings: separate levels by at least one clear signal (size step or weight), not color alone. Heading levels follow document structure, not visual size.
- Labels and captions: smaller, often medium weight; uppercase only for short labels, with positive tracking (about 0.04–0.08em).
- Numerals: use `font-variant-numeric: tabular-nums` wherever numbers are compared in columns, update live, or align (tables, prices, timers, tickers). Proportional numerals jitter when values change. Lining figures suit UI; oldstyle figures can suit editorial prose.

## Measure, leading, tracking

Measure 45–75 characters for body (`max-width: 65ch` is a good default for prose). Leading about 1.4–1.6 for body; tighter (1.05–1.25) for large display, because large leading makes multi-line headings fall apart. Large display type usually wants slightly negative tracking (about −0.01 to −0.03em); body type wants none; small text and uppercase want positive. Never letter-space lowercase body text for decoration.

## Truncation and balancing

Truncate only text whose full value is available elsewhere (tooltip, detail view, accessible name). Prefer wrapping for anything users must read or compare. `text-wrap: balance` evens headline lines (browsers limit it to short blocks); `text-wrap: pretty` reduces orphans in body copy at a small cost. Use multi-line clamping for previews, never for content users must act on.

## Vertical rhythm

Derive spacing between text blocks from the body line-height so paragraphs, lists, and headings fall into a consistent cadence. Heading margins should be asymmetric: more space above than below, so the heading binds to the content it introduces. Strict baseline grids are rarely worth enforcing on the web; consistent multiples of a base unit achieve the perceptible benefit.

## International text and RTL

Plan for 30–40% text expansion in translation (more for short labels). CJK text needs larger sizes or more leading and must not be letter-spaced; Arabic and Devanagari need taller line boxes for marks. Use logical properties (`margin-inline-start`, `padding-block`) so layouts mirror in RTL, mirror directional icons, and never mirror logos, media controls, or numbers. Fallback stacks must cover every supported script.

## User scaling

Size type in `rem`; never disable zoom; never set a root font size in `px` that overrides the user's default. Layouts must survive 200% text resize and the WCAG text-spacing overrides (see accessibility-design) without clipping or overlap.

## Judging rendered type

Look at real content at real sizes, in a browser when one is available. Check: does the first line of a block sit visibly on the same baseline as its neighbors in a row; do icons align to text optically; do headings orphan single words; does bold body text look heavy on dark mode; is the cap height of a button label centered (descender-free labels often look high); do mixed fonts in one line share an x-height; do numbers jitter when they update. Without rendering, list these as hypotheses to verify.
