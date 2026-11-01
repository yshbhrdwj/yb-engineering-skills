# Color and surfaces

Build a system of roles, not a list of hex values. Components reference roles; roles reference ramps; only ramps hold raw values.

## Structure

1. **Ramps.** For each hue in use (one neutral, one brand, and status hues), define 10–12 steps of evenly perceived lightness. Build them in OKLCH: hold hue nearly constant, step lightness evenly, and reduce chroma at the very light and very dark ends where sRGB cannot display it (otherwise colors clip and shift hue). Tint neutrals slightly toward the brand hue (chroma about 0.005–0.02) so grays feel related rather than dead.
2. **Roles.** Map ramps to semantic tokens: `bg`, `surface`, `surface-raised`, `surface-sunken`, `border`, `border-strong`, `text`, `text-muted`, `text-on-accent`, `accent`, `accent-hover`, `focus-ring`, and per status (`success`, `warning`, `danger`, `info`) a foreground, a subtle background, and a border. Charts get their own categorical and sequential roles.
3. **Components** use roles only. A raw hex in a component is a defect: it cannot follow theme changes.

## Neutrals carry the interface

Most of any interface is neutral. Text uses two or three neutral steps (primary, secondary, disabled-or-placeholder), and surfaces use a few closely spaced steps. Pure black text on pure white is harsh at large sizes; a very dark neutral is usually better. Muted text must still meet its contrast requirement; "muted" is a hierarchy signal, not permission to fail.

## Accent and status

One accent is usually enough; it marks the primary action, selection, and focus. Using the accent for decoration dilutes its signal. Status colors must be distinguishable from each other and from the accent, and never be the only signal (pair with icon, text, or position). Reserve red for destruction and errors; using it as a brand accent makes every primary button look dangerous. Domain conventions vary: in many Western markets green means up and red means down, but East Asian markets often reverse this, so financial products must let the convention follow the market or the user.

## Light and dark modes

Dark mode is a separate palette, not an inversion. Use dark neutral surfaces (not pure black, which causes halation around light text and makes elevation impossible), lighten surfaces as they rise instead of adding shadows, desaturate and lighten accents so they do not vibrate, and reduce body text weight slightly or use a lighter step because light-on-dark looks heavier. Re-check every contrast pair in both modes. Implement modes by swapping role values (CSS variables under `prefers-color-scheme` or a class or attribute), so components never change.

## Surface and elevation hierarchy

Define three to five elevation levels and use each for one job: page, card or panel, raised (popover, dropdown), overlay (dialog), and toast. Separate surfaces with one primary method per level: a lightness step, a border, or a shadow. Combining a border, a shadow, and a different background on every card is visual noise. Shadows should be soft, low-opacity, and offset downward consistently, as from one light source; heavy, dark, or colored shadows everywhere are a signal to scrutinize.

## Borders and separation

Prefer spacing and alignment to lines. Where lines are needed (tables, dense panels), use the lightest border that remains perceptible. Borders that identify an interactive control's boundary (an input's edge) are non-text content and need 3:1 against adjacent colors; decorative dividers do not.

## Interactive states

Each interactive role defines rest, hover, pressed, focus, selected, disabled, and (for inputs) invalid. Derive hover and pressed by consistent lightness shifts of the same role (or `color-mix()` with the text color), so every control behaves alike. Focus uses a dedicated ring color with 3:1 contrast against the surrounding background, offset from the control so it is visible on any fill. Disabled lowers contrast and removes affordance but should remain legible enough to read why it is unavailable; prefer explaining the reason to disabling silently.

## CSS variables

Declare ramps and roles as custom properties at `:root`; override roles under the mode selector. Name by role, never by value (`--color-danger`, not `--red-600`, in components). `light-dark()` can express both modes in one declaration where supported, but variables under a mode selector work everywhere and are easier to audit.

## Charts and data color

Categorical palettes need hues that remain distinguishable for common color-vision deficiencies and in grayscale; limit categories to about six to eight, then group or label directly. Sequential scales vary lightness monotonically in one hue; diverging scales meet at a neutral midpoint that means something (zero, target). Label lines directly rather than relying on a legend's color match. Gridlines and axes sit just above the background in contrast.

## Gradients and transparency

Gradients belong to brand expression, not to every surface. Interpolate them in OKLCH (or `in oklch` in `linear-gradient`) to avoid muddy gray midpoints between complementary hues. Text on gradients, images, or translucent glass must meet contrast at its worst point; add a scrim or solid backing when it cannot. Translucent surfaces make contrast depend on whatever scrolls beneath them, so they are hard to keep accessible.

## Contrast methods

Compute WCAG contrast from relative luminance: ratio = (L1 + 0.05) / (L2 + 0.05), where each channel is linearized from sRGB (c/12.92 if c ≤ 0.04045, else ((c + 0.055)/1.055)^2.4) and L = 0.2126R + 0.7152G + 0.0722B. Requirements are in accessibility-design. Compute against the actual adjacent color, including hover, selected, disabled-with-meaning, and dark variants. Report the computed ratio with the two colors; if you did not compute it, say so. APCA is a perceptual alternative under research; it is useful for tuning but is not the WCAG 2.2 conformance measure.

## Spotting muddy or inconsistent color

Signals: more than one near-identical gray or blue in use (count unique values in the CSS); accent used for decoration and actions alike; status colors that differ by hue but not lightness, so they merge in grayscale; low-chroma mid-tones that read as dirty; dark mode that is the light palette inverted; text placed on saturated fills without checking; borders, shadows, and fills all used for separation at once. Fix by collapsing values into ramps and roles, then mapping each component to roles.
