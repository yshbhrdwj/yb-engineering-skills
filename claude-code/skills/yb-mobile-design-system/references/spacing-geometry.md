# Spacing, geometry, and icons

Spacing expresses grouping; geometry expresses care. Most "looks slightly off" reports trace to a small number of shared values.

## Spacing system

- Use a 4-point base with an 8-point rhythm for layout (4, 8, 12, 16, 20, 24, 32, 40, 48, 64). Values outside the scale need a reason, such as an optical correction owned by a component.
- Keep two layers. **Primitive** tokens hold the scale (`space.4 = 16`). **Semantic** tokens state intent (`inset.screen`, `inset.card`, `gap.stack.related`, `gap.section`, `gap.inline.icon`). Components reference semantic tokens, so a density change edits one mapping.
- Proximity communicates grouping: space inside a group must be clearly smaller than space between groups. A common failure is equal spacing everywhere, which removes structure.
- Screen gutters: iPhone layouts commonly use 16–20 pt matching system margins; prefer the platform's layout-margin or list inset values. Material compact windows use 16 dp margins, medium windows 24 dp (Guideline). One gutter per window class, applied everywhere, keeps edges aligned between screens.
- Vertical rhythm: section separation typically 24–32 between groups, 8–12 inside groups, 4 between a label and its value (Heuristic). Pick a rhythm and keep it across screens.

## Geometry

- **Concentric radii.** A nested rounded shape needs inner radius = outer radius − inset. Mismatched nesting (a 16 radius card containing a 16 radius image with 12 inset) looks bloated at corners. Recent iOS design language aligns controls concentrically with device corners; respect that around sheets and bottom controls.
- **Radius scale.** Use a small set (for example 4, 8, 12, 16, 28, full) mapped to component size. Larger components take larger radii; mixing near-identical radii (10, 12, 14) reads as error.
- **Borders.** Use one or two border weights. Hairlines (`1 / screen scale`) for separators; 1 pt/dp for control outlines. A border, a shadow, and a surface tint on the same element are usually redundant; choose the one that the surface system uses.
- **Component dimensions.** Share heights across peer controls (input, select, button in one row). Standard minimums: list rows 44 pt on iOS; Material list items 56/72/88 dp for one/two/three lines.
- **Touch targets.** iOS 44 × 44 pt and Android 48 × 48 dp minimum hit areas (Guideline); WCAG 2.2 target size minimum 24 × 24 CSS px (Required where WCAG applies). The visual can be smaller if the hit area is extended and does not overlap neighbors.

## Optical alignment

Geometric centering aligns bounding boxes; people perceive mass. Correct optically, inside the component, never per screen.

- Text boxes include ascender and descender space; centering a text box vertically in a button often places capitals low or high depending on the font. Fix through line-height and font metrics in the type token, or a component-level offset, then verify rendered.
- Asymmetric glyphs (play triangles, chevrons, arrows) need offsets toward their visual center; circles and triangles must slightly exceed squares to look equal in size.
- Icon plus label: the gap between them should be smaller than the button's horizontal padding, and padding on the icon side often reads larger; many systems reduce leading padding next to an icon.
- Align left edges of text, not the edges of icons or containers, when text is the dominant column. Hang list icons in a consistent leading column so titles align.
- Distinguish a real misalignment (values differ in source or render) from a perceived one (values equal, shapes differ). Report which.

## Icons

- Use one family with consistent stroke width, corner treatment, perspective, and metaphor. Mixing 1.5 and 2 px strokes or rounded and sharp terminals is visible at a glance.
- Size icons in step with type: 16–20 inline with body, 24 for standard controls and navigation. Prefer the platform icon system: SF Symbols match text weight and baseline automatically; Material Symbols expose fill, weight, grade, and optical-size axes. Use the optical size intended for the rendered size.
- Selected states often switch outline to filled (iOS tab bars, Material navigation bars); keep this convention consistent.
- Icon-only controls need an accessible name and a recognizable metaphor; if the meaning needs a tooltip to understand, add a label instead.
- Mirror directional icons (back, forward, progress) in right-to-left layouts; do not mirror logos, media controls with real-world direction, or checkmarks.

## Assets

- Prefer vectors. Raster assets need @2x/@3x on iOS and density buckets up to xxxhdpi on Android; check for blurring at 3x and file size.
- App icons: Android adaptive icons with a monochrome layer for themed icons; recent iOS versions add dark, tinted, and layered icon appearances. Verify current requirements before shipping icon changes.
- Brand marks keep their geometry, clear space, and colors; never redraw, stretch, or recolor them outside brand rules.

## Defects to detect

Equal spacing between unrelated groups; inconsistent card padding for the same hierarchy; nested radii that are not concentric; gutters that change between screens; icon glyphs vertically off-center from their label; mixed icon families; one-off margins that fix one screen while the component stays wrong; targets smaller than the minimum with no extended hit area.

## Verify

Check source values against tokens, then confirm in a render: overlay alignment guides or compare screenshots at identical scale. State measured values only from a capture or layout inspector.

Sources: Apple HIG Layout and SF Symbols; Material 3 Layout, Shape, and Icons; WCAG 2.5.8 (see sources.md).
