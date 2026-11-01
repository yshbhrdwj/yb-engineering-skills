# Android and Material 3

Android users expect system back, edge-to-edge content, Material component behavior, and layouts that adapt across phones, foldables, and tablets.

Why it matters: system back, edge-to-edge, and Material component behavior are shared across every app, and Android users switch between gesture and three-button navigation. Respecting them keeps the app predictable and accessible. An app with a deliberate cross-platform identity need not look like Material, but it must still behave like Android: system back, insets, IME, font scaling, and TalkBack semantics.

Version note: Material 3 Expressive (2025) added motion, shape, type emphasis, and new or revised components; availability depends on the Compose Material 3 or library version. Apps targeting Android 15 (API 35) are edge-to-edge by default; apps targeting Android 16 (API 36) cannot opt out, and predictive back animations are enabled by default. Google Play's target-level deadline makes API 36 the practical baseline for current updates. Check `targetSdkVersion` and library versions before recommending APIs.

## Navigation

- **Navigation bar** for three to five top-level destinations on compact widths. It stays visible while scrolling. Selected destinations use an active indicator and usually a filled icon; always show labels unless space and recognition clearly allow otherwise.
- **Navigation rail** for medium and expanded widths; expanded rails can replace drawers in current Material guidance (verify against the version in use). **Navigation drawer** suits many destinations or infrequent sections.
- **Top app bars**: small or center-aligned for most screens; medium and large for top-level screens with prominent titles, collapsing on scroll. Actions limited to the most important two or three, with an overflow menu.
- **Back**: system back (gesture or button) always works and pops one logical level. Predictive back previews the destination as the gesture progresses, so the outgoing screen must look correct when partially revealed. Intercept back only for meaningful state such as unsaved input or an open sheet, and do it through the platform callback APIs so the preview still works.
- **Up** in the app bar navigates within the app hierarchy; back follows history. They can differ after deep links.

## Components and behavior

- **FAB** for the single most important constructive action on a screen; not for destructive or minor actions. Extended FAB adds a label; it may collapse to an icon while scrolling.
- **Buttons** by emphasis: filled, tonal, elevated, outlined, text. Expressive adds button groups, split buttons, and size variants.
- **Bottom sheets**: standard (coexists with content) or modal (scrim, dismissed by back, drag, or scrim tap). Show a drag handle when resizable.
- **Dialogs**: basic for decisions that block the task; full-screen dialogs for complex input on compact widths. Confirm/dismiss buttons are text buttons at the trailing edge.
- **Snackbars** for brief, low-priority feedback with at most one action; place above the navigation bar and FAB; never for critical errors or information that must persist.
- **Menus**: dropdown and exposed dropdown menus for selection; avoid nested menus on phones.
- **Text fields**: filled or outlined, used consistently; label stays visible (floats when focused or filled); supporting text below, replaced by the error message on error; character counter when limits matter.
- **Selection**: checkboxes for multi-select, radio buttons for one of several, switches for immediate on/off, chips for filters and compact choices, segmented or connected button groups for view switching.

## Color, shape, and elevation

- Color roles (primary, secondary, tertiary, error, surface containers, outline, inverse) derive from tonal palettes. Dynamic color (Android 12 and later) generates the scheme from the wallpaper; always ship a static fallback scheme and test several wallpapers.
- Shape scale: extra small 4, small 8, medium 12, large 16, extra large 28 dp, plus full; Expressive adds increased sizes and a shape library with morphing. Map component families to shape roles rather than raw radii.
- Elevation levels use tonal surface change first, shadow for floating components.

## Motion

Material motion uses spring-based schemes in Expressive (spatial springs for movement, effects springs for color and opacity) and duration/easing tokens in earlier versions. Container transforms, shared axis, and fade-through patterns express relationships. Honor the system animator-duration scale, including "Remove animations".

## Edge-to-edge and insets

- Draw backgrounds and scrolling content behind system bars; keep tappable and draggable content out of system bar and gesture insets.
- Top app bars protect the status bar area; custom headers need a matching protection gradient or solid background.
- With gesture navigation, keep the navigation area transparent; with three-button navigation, add a scrim when a bottom bar animates away.
- Lists pad their content by the bottom inset so the last item clears the navigation bar; FABs and snackbars sit above it. Handle the IME inset so focused fields and primary actions stay visible.
- Display cutouts: solid app bar backgrounds may extend into the cutout; text and controls stay inset; horizontal carousels may scroll through it.
- IME: the keyboard resizes the available area under edge-to-edge only if the app applies the IME inset. Keep the focused field and primary action visible, set the input type and IME action (next, done, search, send), and do not let the keyboard cover a bottom sheet's actions.

## Large screens and foldables

- Use window size classes (compact under 600 dp, medium 600–839, expanded 840 and wider) rather than device type.
- Canonical layouts: list-detail, supporting pane, feed. Avoid stretched single-column phone layouts at expanded widths.
- On Android 16, apps targeting API 36 cannot rely on orientation or resizability restrictions on large displays; layouts must handle any size and aspect ratio. Avoid placing content across a hinge; consider tabletop posture for media and camera.

## Accessibility

TalkBack labels and roles; 48 × 48 dp targets; font scale up to 200% with nonlinear scaling; Switch Access and keyboard focus order; color correction and high-contrast text settings; never disable font scaling globally.

## Defects to detect

Content hidden behind the navigation bar or under the status bar; double status-bar protection; hidden navigation bar on scroll; snackbars carrying critical errors; back that exits the app from a nested state or skips unsaved-input confirmation; custom back interception that breaks the predictive preview; iOS-style back chevrons and swipe-only patterns ported unchanged; dynamic color applied without a fallback or breaking brand moments; phone layouts stretched across tablets.

Sources: Material 3 guidelines and Expressive updates; Android edge-to-edge, predictive back, Android 15/16 behavior changes, large-screen guidance (see sources.md).
