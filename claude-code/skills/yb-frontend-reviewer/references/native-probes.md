# Native mobile probes

Use for iOS, Android, React Native, Expo, Flutter, SwiftUI, or Compose interfaces. Platform conventions come from the project's design authority, or `yb-mobile-design-system` when installed; findings still come from inspection. Use only the probes relevant to the scope.

## Evidence rules

- Source inspection is not rendered evidence.
- A browser preview or Expo Web build is not device testing.
- Simulator or emulator evidence is not physical-device coverage. Name the OS version, device profile, and settings used.
- One screenshot covers one state at one size. An accessibility inspector is not a VoiceOver or TalkBack test.

## Probes

- **Platform conventions:** native back, tabs, sheets, pickers, and pressed feedback; intended iOS and Android differences versus accidental divergence; web patterns such as hover-only affordances on native screens.
- **Navigation and back:** Android system back and the iOS edge swipe from every changed screen, including modals, nested stacks, and deep-link entry; unsaved-work protection; no dead ends or loops.
- **Safe areas and system bars:** content and controls clear of the notch or Dynamic Island, status bar, home indicator, and gesture bar; no doubled insets; legible status-bar content in both themes.
- **Keyboard:** the focused field and submit action stay visible; next and done keys move as expected; dismissal restores the layout; hardware keyboards where supported.
- **Touch targets and gestures:** targets meet the authority's minimum with adequate spacing (an extended hit area counts); swipes do not fight scrolling or back; essential actions have a non-gesture alternative.
- **Text scaling:** largest Dynamic Type and Android font scale; wrapping, truncation, clipping, overlap, and whether layouts reflow rather than shrink.
- **Feedback and failure:** pressed states, designed haptics, loading without layout jumps, offline and server failures, permission denial, and retry that keeps input.
- **Lifecycle:** backgrounding, return, rotation, and interrupted flows keep state.

## Report precisely

Tie each finding to screen, platform and OS, device profile, setting, and steps. Actionable: "Android 15 emulator, Pixel 8 profile, font scale 2.0: on Checkout the total wraps beneath the 36 dp Pay button; expected a 48 dp target with the total above it." Vague: "Checkout feels cramped on Android." Mark findings reasoned from source as unconfirmed until rendered.
