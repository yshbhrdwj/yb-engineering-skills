# Typography

Type carries most of a mobile interface's hierarchy. Judge it at real sizes, in real content, at the largest supported text setting.

## Derive the roles

Do not apply one universal scale. Derive roles in this order:

1. **Anchor** body text to the platform default (iOS Body 17 pt; Material body large 16 sp), then adjust only for audience (older adults, children), viewing distance (glanced in motion, held close, mounted), or content (long reading, dense data).
2. **Inventory the jobs** text actually does on representative screens: screen title, section heading, item title, body, metadata, label, numeric value. Each job gets one role; merge roles that differ by less than a visible step.
3. **Set the ratio** between levels from the direction: tight for dense professional tools, wider for expressive or editorial products.
4. **Assign weight and color** before adding sizes; check that each level is distinguishable in grayscale.
5. **Test the extremes**: longest real strings, the largest accessibility size, the target languages, and numeric updates.

## Decide

- **System or custom.** System fonts (SF Pro on iOS, Roboto or the device font on Android) give optical sizing, tuned tracking, Dynamic Type metrics, complete glyph coverage, and zero load cost. Choose a custom face when identity depends on it, usually for display and headings. Body text in a custom face must justify the cost: licensing, file size, scaling, and fallback for every supported script.
- **Roles, not sizes.** Define semantic roles (display, headline, title, body, label, caption, numeric) with size, line height, weight, tracking, and font family. Components consume roles; screens never set raw sizes.
- **Scale.** Build roles with a deliberate ratio, often 1.125–1.25 for dense products and up to 1.333 for expressive ones (Heuristic). Five to seven roles in use on one screen is usually the ceiling before hierarchy blurs.
- **Weight before size.** On small screens, weight and color separate levels more economically than size jumps. Use at most three weights in a product; two often suffice.
- **Line height.** Body 1.3–1.5× size; headings 1.1–1.3×; large display tighter (Heuristic). Scripts with tall marks (Thai, Devanagari, Vietnamese stacked diacritics) and CJK need more room; test them rather than reusing Latin values.
- **Tracking.** System fonts apply size-specific tracking automatically. Custom fonts do not: large display sizes usually need slight negative tracking, and all-caps or small labels need slight positive tracking (Heuristic). Never track body text loosely for "airiness".
- **Line length.** Phones rarely exceed comfortable lengths; tablets and landscape do. Constrain reading text to about 60–75 characters with readable-width guides or max widths.

## Platform

- **iOS.** Dynamic Type text styles (Large Title 34, Title 1 28, Title 2 22, Title 3 20, Headline 17 semibold, Body 17, Callout 16, Subheadline 15, Footnote 13, Caption 1 12, Caption 2 11 pt at the default size) scale through seven standard and five accessibility sizes. Custom fonts should map to these styles via font metrics scaling so they follow the user's setting. Avoid text below 11 pt (Guideline). SF switches optical sizes automatically; custom fonts with an optical-size axis need it set explicitly.
- **Android.** Material 3 roles: display, headline, title, body, label, each large/medium/small (display large 57/64, headline large 32/40, title large 22/28, body large 16/24, label large 14/20, label small 11/16 sp size/line height). Use sp for text. Android 14 and later scale fonts up to 200% nonlinearly, so large text grows less than small text; never assume a fixed multiplier.
- **Both.** Respect bold-text and font-scale settings; test long localized strings, right-to-left scripts, and fallback glyphs.

## Implement

- Ship tokens such as `type.title.medium` with size, line height, weight, letter spacing, and family. Line height belongs in the token, not in components.
- Custom font weights need real font files per weight on Android; requesting a weight that is not bundled produces synthetic or wrong rendering.
- Use tabular figures for anything compared or updated in place: prices, timers, scores, tables, and charts. Right-align or decimal-align numeric columns; keep consistent precision and unit placement; format with locale-aware APIs.
- Align mixed sizes on one line (currency symbol and amount, value and unit, icon label and count) by **baseline**, not by box center. Center alignment includes font ascent/descent padding and makes the smaller text float.
- Truncate deliberately: tail truncation for single-line labels; middle truncation for file names and identifiers; wrapping for anything a user must read to decide. Never truncate critical numbers; abbreviate with the full value exposed to assistive technology.
- Let text containers grow. Fixed heights, fixed line counts on primary content, and absolute positioning of text break at large sizes.

## Defects to detect

- Hierarchy too flat (adjacent roles within ~10% size and the same weight) or too noisy (many sizes doing one job).
- Section headings visually weaker than the content they introduce, or a screen with competing headlines.
- Baselines misaligned across a row or between columns of a list.
- Loose tracking on body, missing negative tracking on custom display type, or tight all-caps.
- Proportional digits jittering in timers, counters, prices, or columns.
- Placeholder text styled like entered text; helper text indistinguishable from errors.
- Orphaned single words on headings and buttons; widows on short cards where a balanced wrap is available.
- Clipped ascenders or descenders from fixed line heights or containers; text clipped or overlapping at the largest size.
- Fallback glyphs with different metrics in a custom face (common in names, currency symbols, and non-Latin content).
- Captions below 11 pt/sp, or secondary text both small and low-contrast.
- Titles so large they push the primary task below the fold, or headers whose weight unbalances a sparse screen.
- Text competing with the primary action: a heavier or larger label near the button than the button itself.
- Long body text set wide, tight, or in light weights, which becomes tiring to read.
- Wrapped labels that break fixed layouts (tabs, chips, segmented controls, buttons).
- Inconsistent weights for the same role across screens.

## Mixed scripts and density

- Pair a custom Latin face with system fonts for scripts it lacks, and check that sizes and line heights look matched; the same point size can look very different across scripts.
- Screen density changes rendering, not size: hairline weights and light fonts degrade on lower-density Android screens and in small sizes. Prefer regular or heavier weights below about 15 pt/sp.

## Tradeoffs

- Density versus legibility: dense professional tools may use 13–15 pt/sp body text in tables, but only with strong contrast, tabular figures, and scalable layouts.
- Capping text scaling (for example on tab labels or a fixed numeric keypad) can be justified; capping body or primary content is not. Prefer layout changes such as stacking, wrapping, or a larger-text alternative layout.

## Verify

Check the default and largest text sizes, both themes, a long localized string, and numeric updates in motion. Measure baseline offsets or line boxes only from a rendered capture or layout inspector; otherwise report the concern as source-based.

Sources: Apple HIG Typography; Material 3 Typography; Android font scaling; WCAG 1.4.4 and 1.4.12 (see sources.md).
