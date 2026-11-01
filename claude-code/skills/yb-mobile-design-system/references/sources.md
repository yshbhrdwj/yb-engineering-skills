# Sources

Open only to verify a version-sensitive claim the answer depends on. Primary sources outrank secondary design systems and exemplary products, which are inspiration, not authority.

**Strength**: normative (a standard, law, or store rule), recommended (official platform guidance), reference (official API documentation). **Checked** gives the last verification; "stable" means long-standing guidance not rechecked on 1 November 2026; "verify" means confirm before relying on specifics. When a primary source is inaccessible, keep the uncertainty explicit.

## Apple

| Source | Topic | Strength | Checked | Version assumptions |
| --- | --- | --- | --- | --- |
| Human Interface Guidelines, https://developer.apple.com/design/human-interface-guidelines/ | Navigation, tab bars, sheets, alerts, menus, lists, layout, color, materials, motion, haptics, accessibility | recommended | stable for principles; verify iOS 26+ material and tab-bar specifics (pages render client-side and could not be read during authoring) | iOS 26 material system and later revisions |
| HIG Typography, https://developer.apple.com/design/human-interface-guidelines/typography | Dynamic Type sizes, text styles | recommended | stable | Default sizes at the Large setting |
| SF Symbols, https://developer.apple.com/sf-symbols/ | System iconography | recommended | stable | Symbol availability varies by OS |
| App Review Guidelines, https://developer.apple.com/app-store/review/guidelines/ | Account deletion, login services, subscriptions | normative (store) | verify wording | Revised periodically |
| Accessibility, https://developer.apple.com/accessibility/ | VoiceOver, Dynamic Type, display settings | recommended | stable | — |

## Google and Android

| Source | Topic | Strength | Checked | Version assumptions |
| --- | --- | --- | --- | --- |
| Material 3, https://m3.material.io/ | Roles, type scale, shape, state layers, components, Expressive updates | recommended | stable for roles and scales; verify Expressive components per library version | Material 3 Expressive (2025) |
| Edge-to-edge design, https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge | Insets, protection, cutouts | recommended | checked 1 Nov 2026 | Android 15+ |
| Android 16 behavior changes, https://developer.android.com/about/versions/16/behavior-changes-16 | Edge-to-edge opt-out removed, predictive back default, large-screen restrictions ignored | reference | checked 1 Nov 2026 via official page summaries | Target API 36 |
| Predictive back, https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture | Back callbacks and animations | reference | verify | API 33+ |
| Adaptive layouts, https://developer.android.com/develop/ui/compose/layouts/adaptive | Window size classes, canonical layouts | recommended | stable; verify newer size classes | — |
| Font scaling, https://developer.android.com/about/versions/14/features | Nonlinear scaling to 200% | reference | stable | Android 14+ |
| Accessibility, https://developer.android.com/guide/topics/ui/accessibility | TalkBack, targets, semantics | recommended | stable | — |

## Accessibility standards

| Source | Topic | Strength | Checked | Version assumptions |
| --- | --- | --- | --- | --- |
| WCAG 2.2, https://www.w3.org/TR/WCAG22/ | Success criteria | normative where adopted | stable | 2.2 |
| WCAG2ICT, https://www.w3.org/TR/wcag2ict-22/ | Applying WCAG to native apps | recommended (W3C note) | stable | — |
| European Accessibility Act, https://eur-lex.europa.eu/eli/dir/2019/882/oj | Legal accessibility duties for covered services | normative (law) | stable | Applies since June 2025; national law and sector determine scope |

## Frameworks

| Source | Topic | Strength | Checked | Version assumptions |
| --- | --- | --- | --- | --- |
| React Native, https://reactnative.dev/docs/ | Core components and APIs | reference | verify per installed version | — |
| Expo changelog, https://expo.dev/changelog | SDK features and defaults | reference | checked 1 Nov 2026 (SDK 57 with React Native 0.86) | Newer releases likely |
| React Navigation, https://reactnavigation.org/docs/ | Native stack, tabs, headers, sheets | reference | verify per installed version | — |
| Flutter, https://docs.flutter.dev/ | Theming, adaptive widgets, semantics | reference | verify per installed version | — |
| SwiftUI, https://developer.apple.com/documentation/swiftui | Views, accessibility, materials | reference | verify availability by OS | — |
| Compose Material 3, https://developer.android.com/jetpack/androidx/releases/compose-material3 | Components, expressive APIs | reference | verify per installed version | — |

## Heuristics used

Response-time thresholds (about 0.1, 1, and 10 seconds), type ratios, spacing rhythms, and motion durations in these references are heuristics from common practice and usability research, labeled as such where they appear.

## UI/UX Pro Max

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT License, copyright 2024 Next Level Builder). Version 2.15.0 was inspected on 1 November 2026.
- Concepts considered: master-plus-page-override persistence, product-type reasoning, searchable catalogs, pre-delivery checklists, and query discipline. This skill reuses the persistence convention by reference and otherwise contains original text. No upstream datasets, code, or prose are copied, so no MIT notice is required here; retain upstream notices if any of its material is later copied.
- Differences: this skill is mobile- and platform-specific, routes by task mode, labels requirement strength and evidence, and treats catalogs as candidates rather than authority.
