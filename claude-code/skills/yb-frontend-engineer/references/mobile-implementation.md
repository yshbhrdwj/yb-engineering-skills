# Mobile implementation

Read for native mobile work (React Native, Expo, Flutter, SwiftUI, Jetpack Compose). Reuse the project's navigation, styling, component, and state infrastructure; check APIs against installed versions. Visual and token decisions belong to the design authority; when `yb-mobile-design-system` is installed, its implementation reference maps tokens and styling to each stack.

## Navigation and lifecycle

- Use the project's router (Expo Router, React Navigation, GoRouter, NavigationStack, Navigation Compose). Native stacks keep platform back gestures and transitions; do not rebuild them in JavaScript.
- Android system back and the iOS edge swipe step back predictably from every screen and modal. Intercept back only to protect unsaved work; check predictive back where supported.
- Deep links and notifications open the intended screen with a sensible back stack, require sign-in when needed, and reject malformed or unauthorized parameters. Route parameters are untrusted input.
- Preserve drafts, scroll position, and in-progress work across background/foreground, rotation, and process restoration. Refresh stale data on resume without discarding edits.

## Layout and input

- Apply safe-area insets once with the installed solution; account for status, navigation, and gesture bars when drawing edge to edge.
- Keep the focused field and primary action visible above the keyboard. Set input type, autofill/content type, return key, and next-field order; IME composition must not trigger validation or submit early.
- Prefer platform-native controls (pickers, switches, sheets, share) unless the design says otherwise. Meet touch-target minimums by extending hit areas, not visuals.
- Resolve gesture conflicts: horizontal swipes inside vertical scrolling, row swipes versus back swipe, sheets over scroll content. Essential actions need a non-gesture alternative.
- Respect Dynamic Type and Android font scale; never disable scaling globally. Rows grow, wrap, or switch layout at large sizes instead of clipping.
- Adapt to window size and orientation, not device model; support tablets, split view, and foldables where shipped.

## Accessibility, media, and performance

- Set native accessibility role, label, state, value, grouping, hidden decoration, announcements for asynchronous results, and custom actions for gesture-only operations. Move focus to new screens and errors.
- Give images a fixed aspect ratio, placeholder, suitable resolution, caching, failure fallback, and a label or decorative marking.
- Virtualize long lists with stable keys; avoid re-rendering rows on unrelated state. Animate on the UI thread where supported, honor reduced motion, and keep input responsive.
- Distinguish offline, timeout, server, and permission-denied failures; retry or queue only where the product promises it; never lose typed input. Request permissions in context and handle denial and "don't ask again".

## Verify

Run type checks and affected component tests (React Native Testing Library, `flutter test`, XCTest, Compose UI tests). Rendered evidence needs an iOS simulator, an Android emulator, or a device-automation tool the project already uses (Maestro, Detox, Appium): one screenshot per distinct state, touch input, largest text, safe areas on notched and gesture-navigation profiles, open keyboard, and both themes when supported. Check availability; never assume it. A browser preview or Expo Web build is not native rendering, and a simulator is not a physical device. Missing tooling is a named gap.
