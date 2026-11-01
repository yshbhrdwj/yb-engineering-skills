# Color, surfaces, and imagery

A palette is only good if every screen, state, and theme can be built from it without improvisation.

## Build the palette

- Generate tonal ramps in a perceptual space (OKLCH/OKLab, or Material's HCT) so equal steps look equal. HSL lightness is not perceptual: yellow and blue at the same HSL lightness differ sharply in contrast.
- Layer tokens: primitives (`blue.600`) → semantic roles (`color.action.primary`, `color.text.secondary`, `color.surface.raised`, `color.border.subtle`, `color.status.danger`) → optional component tokens. Components reference roles, never primitives or hex values.
- Every role needs an "on" partner (text and icon color for that surface) with verified contrast in both themes.
- Neutral ramps carry most of the interface. A slight hue in neutrals (toward the brand or warmth) makes the system feel intentional; pure gray with a saturated brand often looks disconnected (Taste, commonly effective).
- Use brand color for meaning: primary actions, selection, and key moments. Brand color on everything removes its signal.
- Proportion matters more than palette size: neutrals carry most of the surface area, a secondary color supports structure, and the accent stays scarce enough to guide the eye.
- Temperature sets tone: warm neutrals feel personal and calm; cool neutrals feel precise and technical. Keep one temperature across surfaces unless a shift is deliberate.

## Diagnose a weak palette

1. Render or list every role pair in use; flag hex values outside the roles.
2. Check contrast for each text and boundary pair in both themes.
3. View key screens in grayscale: hierarchy should survive without hue.
4. Count accent usage per screen: if the accent marks more than a few things, it marks nothing.
5. Compare roles across states (pressed, selected, disabled, error) for collisions, such as selected and error both reading as "highlighted".
6. Correct at the ramp or role level (adjust a step, add a missing role, remap a component), never per screen.

## Surfaces and elevation

- Define a surface ladder (base, raised, overlay, plus grouped and inset where the platform uses them). Each step should be distinguishable without borders in both themes.
- Material 3 expresses elevation mostly through tonal surface containers (lowest → highest) with shadow reserved for floating elements. iOS uses grouped backgrounds, separators, and system materials; in dark mode, elevated content uses lighter backgrounds.
- Recent iOS releases put navigation and controls on a translucent glass layer over content. Treat glass as a control layer, not a content style; text on glass must still meet contrast, including with Reduce Transparency and Increase Contrast enabled. Verify current Apple guidance before adopting it in a custom component.
- Dark theme is a separate design, not an inversion: desaturate and lighten saturated brand colors, raise surface tone with elevation, reduce large pure-white areas, and recheck every state color. Pure black backgrounds suit media and OLED-focused products; elsewhere they increase halation next to light text (Heuristic).

## State and status color

- Pressed, focused, selected, dragged, and disabled states are part of the palette. Material uses state layers of content color at fixed opacities (hover 8%, focus and pressed 10%, dragged 16%) and disabled content at 38% with containers at 12%; iOS typically dims or highlights system controls (Guideline).
- Disabled controls are exempt from WCAG contrast, but users still need to recognize them and understand why they are unavailable.
- Status colors (danger, warning, success, info) always pair with text or an icon. About 1 in 12 men has a color-vision deficiency; red and green alone are not reliable.
- Financial up/down colors follow locale: red means increase in some markets (for example mainland China). Make the convention a setting or follow locale, and always add signs or arrows.

## Contrast requirements

- Text: 4.5:1, or 3:1 for large text (WCAG 1.4.3, Required where WCAG applies). Non-text UI boundaries, focus indicators, and state indicators: 3:1 against adjacent colors (1.4.11).
- Check text over images, gradients, and glass at the worst point, not the average. Add scrims or solid backing where content varies.
- Measure contrast from token values, then confirm on a render for translucent and layered surfaces; computed values for blended colors are estimates.

## Data visualization

- Categorical palettes: distinct lightness as well as hue, at most about six to eight series, direct labels instead of legends where space allows.
- Sequential: one hue varying in lightness. Diverging: two hues around a meaningful neutral midpoint.
- Never encode a critical difference with hue alone; use position, shape, pattern, or labels.

## Imagery

- Choose one photographic treatment (crop ratio, color grade, subject framing) and one illustration style per product. Mixed stock styles break identity faster than any color issue.
- Fix aspect ratios per slot; define focal-point cropping for faces and products; reserve space with placeholders to avoid layout shift.
- Images with text overlays need a scrim or gradient tuned for the worst image.
- Mark meaningful images with descriptions; mark decorative imagery hidden from assistive technology.

## Defects to detect

Raw hex in components; two near-identical grays serving one role; brand color used for non-interactive decoration; surfaces separated only by low-contrast borders; dark theme built by inversion (shadows on dark, saturated primaries vibrating); disabled and secondary text indistinguishable; status conveyed by color alone; text over photos without protection; glass or blur reducing legibility.

## Tradeoffs

Dynamic color (Android 12 and later) increases personal fit and platform cohesion but weakens brand recognition; use it for surfaces and secondary roles while keeping brand moments fixed, or offer it as a user choice. A brand palette that fails contrast needs an accessible variant for text and controls, keeping the original for large decorative areas.

## Verify

Compute contrast for every role pair in both themes; render key screens in light, dark, increased contrast, and with a grayscale filter to test color-independent meaning.

Perceptual spaces such as OKLCH guide ramp construction; contrast requirements are still computed with the WCAG formula. Express final tokens in formats the stack supports (hex or RGB in React Native and most native code).

Sources: WCAG 1.4.1, 1.4.3, 1.4.11; Material 3 Color and Elevation; Apple HIG Color, Dark Mode, Materials (see sources.md).
