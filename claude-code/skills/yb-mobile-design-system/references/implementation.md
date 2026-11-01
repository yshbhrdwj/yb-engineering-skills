# Implementation mapping

Map design decisions onto the project's actual stack. Read `package.json`, `app.json`/`app.config.*`, `pubspec.yaml`, Gradle, or the Xcode project first; match the installed versions and the styling library already in use. Do not migrate styling systems, add UI kits, or replace navigation libraries as a side effect of design work. APIs named here change between releases; confirm them against the installed version when the recommendation depends on them.

## Shared versus platform layers

| Layer | Shared across platforms? | Examples |
| --- | --- | --- |
| Visual identity | Yes | Brand color, display type, illustration, voice |
| Semantic tokens | Yes, with platform values where needed | Roles shared; values may differ (iOS 17 pt body, Android 16 sp) |
| Component behavior | Mostly | States, validation, content rules |
| Interaction conventions | No | Back, navigation chrome, sheets, pickers, pressed feedback, haptics, text selection |
| System integration | No | Dynamic color, widgets, share sheets, notifications, permissions, biometrics |

Usability differences that matter most: iOS back is an edge swipe plus a labeled button, Android back is a system gesture or button that must always work; iOS tab bars and Android navigation bars differ in material and behavior; iOS uses wheel, compact, and inline pickers, Android uses dialogs; pressed feedback is highlight on iOS and ripple or state layer on Android; Android FABs and snackbars have no direct iOS equivalent.

## Choosing dependencies

Prefer what is installed. Before recommending a library, check maintenance activity, compatibility with the installed framework version and architecture, performance on low-end devices, implementation complexity, accessibility support, and license. Popularity alone is not a reason.

## React Native and Expo

**Detect.** React Native version, Expo SDK, New Architecture status, router (Expo Router or React Navigation), styling approach (StyleSheet, NativeWind, Unistyles, Tamagui, Restyle, styled-components), animation (Reanimated, Animated), gesture handler, safe-area and keyboard libraries.

**Tokens and theming.**
- One typed theme module exporting primitives, semantic roles, and component tokens; components consume roles through the project's existing theming mechanism (context, hook, or library).
- Light and dark from `useColorScheme()` with the app config set to follow the system appearance. Platform system colors are available through `PlatformColor` when the design calls for native semantic colors.
- Platform divergence: `Platform.select` for values, `.ios.tsx` / `.android.tsx` files only when structure genuinely differs.

**Typography.**
- Leave `allowFontScaling` on. Use `maxFontSizeMultiplier` only on elements that cannot reflow (tab labels, compact badges), never on body content. Read the current scale from `useWindowDimensions().fontScale` to switch layouts at large sizes.
- `fontVariant: ['tabular-nums']` for numbers; `numberOfLines` with an explicit `ellipsizeMode`.
- Custom fonts: embed at build time through the Expo font config plugin or native assets; register one family name per weight file and verify Android picks the intended weight.
- `alignItems: 'baseline'` aligns mixed text sizes in a row. Android adds font padding to text boxes; correct vertical centering in the type token or component, and verify on both platforms.

**Layout.**
- Safe areas from `react-native-safe-area-context` (`useSafeAreaInsets` or its `SafeAreaView`); core `SafeAreaView` is iOS-only and deprecated in recent React Native.
- Android edge-to-edge is the default in current React Native and Expo releases; pad scroll content and bottom controls by insets rather than relying on the system to push content.
- Keyboard: `KeyboardAvoidingView` behavior differs per platform; `react-native-keyboard-controller` is a common, more consistent option when already present or justified. Keep the focused field and primary action visible.
- Large titles with scroll views on iOS need `contentInsetAdjustmentBehavior="automatic"`.

**Navigation and overlays.**
- Native stack (React Navigation native stack, Expo Router `Stack`) uses platform navigation controllers, giving native back gestures and transitions. Prefer it to JS stacks unless custom transitions are central.
- Header options cover large titles, translucent or blurred headers, and native search bars. Native tabs implementations (in Expo Router and React Navigation) render the platform tab bar, including current iOS tab bar materials; check the version's stability label before adopting.
- Native sheets: `presentation: 'formSheet'` with allowed detents in native stack. JS sheet libraries (for example `@gorhom/bottom-sheet`) allow custom visuals at the cost of native feel; keep one approach per app.
- Android back: React Navigation integrates the system callback; custom `BackHandler` interception should be limited to unsaved-state confirmation and checked against predictive back.

**Interaction.**
- `Pressable` with a pressed style and `android_ripple` for touch feedback; `hitSlop` to extend small visuals to minimum targets.
- Haptics through `expo-haptics` (selection, impact, notification) or the installed equivalent.
- Gestures with `react-native-gesture-handler`; animations with Reanimated on the UI thread. Read reduced-motion through `AccessibilityInfo` or Reanimated's reduced-motion hook and swap movement for fades.
- Long lists: `FlatList` with stable keys and item layout, or FlashList if installed. Images: `expo-image` with placeholders and fixed aspect ratios.

**Accessibility props.** `accessibilityRole`/`role`, `accessibilityLabel`/`aria-label`, `accessibilityState` (selected, disabled, checked, expanded), `accessibilityValue` for sliders and progress, `accessibilityActions` for swipe alternatives, `accessible` on containers to group a card, `importantForAccessibility` and `accessibilityElementsHidden` for decorative content, `AccessibilityInfo.announceForAccessibility` or `accessibilityLiveRegion` for updates.

**Verify.** Type-check and run affected tests; render on an iOS simulator and an Android emulator when available. React Native Testing Library queries by role and label check semantics, not visuals. Flow tools (Maestro, Detox) cover journeys when the project already uses them.

## Flutter

`ThemeData` with `ColorScheme.fromSeed` or explicit schemes; Material 3 is the default in current Flutter. Custom tokens through `ThemeExtension`. `TextTheme` roles map to type tokens. Use `.adaptive` constructors or Cupertino widgets where native iOS behavior matters. Respect `MediaQuery.textScalerOf` (nonlinear) and `MediaQuery.disableAnimationsOf`; `SafeArea` and view padding for insets; `Semantics` for labels and grouping; `FontFeature.tabularFigures()` for numbers.

## SwiftUI

Semantic fonts (`.body`, `.headline`) and `Font.custom(_:size:relativeTo:)` for custom faces; `@ScaledMetric` for scaled spacing and icon sizes; `ViewThatFits` or `dynamicTypeSize` checks for accessibility layouts; `.monospacedDigit()`. Colors from asset catalogs with appearance variants. `.sensoryFeedback` for haptics. `accessibilityLabel`, `.accessibilityElement(children: .combine)`, and `@Environment(\.accessibilityReduceMotion)`. New material and concentric-shape APIs require the matching SDK and availability checks.

## Jetpack Compose

`MaterialTheme(colorScheme, typography, shapes)`; `dynamicLightColorScheme`/`dynamicDarkColorScheme` with static fallback; expressive theme APIs only in versions that ship them. `enableEdgeToEdge()`, `Scaffold` inner padding, and `WindowInsets` for system bars and IME. Window size classes for adaptive layouts. `Modifier.semantics` and `minimumInteractiveComponentSize`. Predictive back through the activity/Compose back handlers.

## Defects to detect

Hardcoded sizes and colors bypassing the theme; font scaling disabled globally; JS reimplementation of native navigation that loses back gestures; `SafeAreaView` from core on Android; insets applied twice; a new styling or animation library added for one screen; platform checks scattered through components instead of tokens.

Sources: React Native, Expo, React Navigation, Flutter, SwiftUI, and Jetpack Compose documentation (see sources.md).
