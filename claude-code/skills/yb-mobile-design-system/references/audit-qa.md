# Audits, design QA, and rendered inspection

## Audit procedure

1. **Scope.** Confirm the requested scope: component, flow, or full app. Pin revision, platforms, and available tools.
2. **Foundations.** Detect stack and versions; read design authority, tokens, and shared components once; note gaps in the authority itself.
3. **Inventory.** List flows and states in scope. For a full app, enumerate inspected flows and mark uninspected ones; never imply full coverage.
4. **Inspect** through the QA layers below, rendered when tools allow, otherwise from source with findings labeled accordingly.
5. **Trace.** Map each issue to a token, shared component, or pattern; count affected screens instead of listing each.
6. **Prioritize** by user impact: blocks the task or excludes users; misleads or erodes trust; slows repeated use; polish.
7. **Report.** Findings in the format from `visual-quality.md`, a token and component correction plan, the coverage table, and outstanding checks.

## QA layers

Run the layers the scope needs; a Mode 1 change usually needs layers 2, 3, and 7 only.

1. **Structure**: hierarchy, navigation, content organization, task clarity.
2. **System consistency**: tokens, component reuse, type roles, spacing, shapes, icons, color roles.
3. **Optical precision**: baselines, icon centering, optical weight, internal padding, dividers, proportions.
4. **Native interaction**: touch feedback, gestures, keyboard, navigation and back, safe areas, sheets and dialogs.
5. **Accessibility**: text scaling, contrast, focus and reading order, names and roles, targets, alternate input, reduced motion.
6. **Rendered validation**: representative screens and interactions on iOS and Android when tools exist.
7. **Regression safety**: the change does not break navigation, data display, input, critical states, or screens that share the changed token or component.

## Static sweep

Run before reading files one by one, over the whole scope, excluding token and theme files where noted. Every hit is a candidate: open it and confirm against tokens, authority, and context. React Native and Expo patterns (extended regular expressions; `\|` in the table is an escaped `|`, so type a plain `|` in commands):

| Concern | Pattern | Confirm |
| --- | --- | --- |
| Raw color | `#[0-9A-Fa-f]{3,8}['"]\|rgba?\(` | Outside token files, map to a role; compute contrast |
| Raw type, space, shape | `(fontSize\|lineHeight\|letterSpacing\|fontWeight\|padding[A-Za-z]*\|margin[A-Za-z]*\|gap\|borderRadius):\s*[0-9'"]` | Matches the token scale and authority; nested radii concentric |
| Fixed size | `(height\|maxHeight\|width):\s*[0-9]` | Does text inside clip at the largest size? |
| Scaling caps | `allowFontScaling=\{false\}\|maxFontSizeMultiplier` | Allowed only by an accepted exception on non-reflowable text |
| Truncation | `numberOfLines=` | Is the truncated content essential? |
| Theme pinning | `color\.light\|useColorScheme\|Appearance` | Does every screen follow the system theme? |
| Controls | `<(Pressable\|Touchable[A-Za-z]*)\|onPress=` | Role, accessible name, pressed state, target or `hitSlop` |
| Stateful roles | `accessibilityRole="(checkbox\|switch\|radio\|tab\|togglebutton)"\|role="(checkbox\|switch\|radio\|tab)"` | `accessibilityState` reflects checked, selected, or disabled |
| Selection | `selected\|isActive\|focused` | Shown by more than color |
| Gestures | `Swipeable\|Gesture\.(Pan\|Fling\|LongPress)\|onLongPress\|PanResponder` | Visible alternative and undo for destructive actions |
| Motion | `withRepeat\|Animated\.loop\|repeat` with `ReduceMotion\|useReducedMotion\|isReduceMotionEnabled` | Loops and large movements honor reduced motion |
| Insets | `SafeAreaView\|useSafeAreaInsets\|KeyboardAvoidingView\|position:\s*'absolute'\|bottom:\s*0\|paddingBottom:\s*[0-9]` | Bottom bars, sheets, and fixed controls clear home indicator, navigation bar, and keyboard; no inset handling in a scope with bottom bars or sheets is itself a candidate |
| Numbers | `toFixed\|toLocaleString\|Intl\.\|padStart\|tabular-nums` | Changing or compared numbers use tabular figures and locale formatting |
| Back | `BackHandler\|gestureEnabled:\s*false\|beforeRemove` | System back and edge swipe preserved; confirm only unsaved input |
| Inputs | `<TextInput\|placeholder=\|keyboardType\|textContentType\|autoComplete` | Visible label, keyboard type, autofill, inline errors |
| Overlays | `<Modal\|transparent\|onRequestClose\|presentation:` | Dismissal never discards input silently; matches authority's overlay choice |
| Icons | `@expo/vector-icons\|react-native-vector-icons\|lucide` | One family and consistent sizes |
| Alignment | `alignItems:\s*'center'` | Rows mixing text sizes align by baseline |

Example: `grep -rnE --include='*.tsx' --include='*.ts' -e 'allowFontScaling=\{false\}|maxFontSizeMultiplier' src/`. Other stacks: Flutter `Color\(0x|fontSize:|textScaler|GestureDetector|\.repeat\(`; SwiftUI `Color\(red:|\.system\(size:|\.frame\(height:|lineLimit|onLongPressGesture|repeatForever`; Compose `Color\(0x|fontSize = |\.height\(|maxLines|contentDescription = null|infiniteRepeatable`.

## Contrast computation

Compute; never estimate. Pass `foreground:background` hex pairs; composite any alpha over its background first.

```sh
python3 -c "import sys
def L(h):
 h=h.lstrip('#'); h=''.join(c*2 for c in h) if len(h)==3 else h
 c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
 c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
 return .2126*c[0]+.7152*c[1]+.0722*c[2]
for p in sys.argv[1:]:
 a,b=p.split(':'); x,y=sorted((L(a),L(b)),reverse=True); print(p, round((x+.05)/(y+.05),2))" 5B6763:FFFFFF A3AFAA:1A2320
```

Thresholds: 4.5:1 for text; 3:1 for large text (about 18 pt regular or 14 pt bold), icons, focus indicators, and component boundaries. Check both themes and every state that changes color.

## Rendered inspection

Use the host's simulator, emulator, or device tools when available; otherwise these standard commands (confirm availability for the installed tooling):

| Need | iOS Simulator | Android emulator or device |
| --- | --- | --- |
| Screenshot | `xcrun simctl io booted screenshot out.png` | `adb exec-out screencap -p > out.png` |
| Dark theme | `xcrun simctl ui booted appearance dark` | `adb shell cmd uimode night yes` |
| Largest text | `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large` | `adb shell settings put system font_scale 2.0` |
| Remove animations | Reduce Motion in Settings > Accessibility | `adb shell settings put global animator_duration_scale 0` |
| Other widths | Boot a smaller and a larger device | `adb shell wm size` and `adb shell wm density` |
| Accessibility tree | Accessibility Inspector | `adb shell uiautomator dump` |

Restore changed settings afterward. Converting screenshot pixels: iOS points = pixels ÷ device scale (2 or 3); Android dp = pixels ÷ (density ÷ 160). Compare before and after at identical scale and state. An accessibility tree confirms names and roles, not the spoken experience; a screenshot proves one state.

## Quality gates

- Do not claim perfect design, or a test, screen, device, or screen-reader result that did not happen.
- Do not present Taste as a defect or apply a universal measurement without platform and context.
- Do not change unrelated screens without authorization.
- Do not call an audit complete when only part of its scope was inspected.
- Do not approve work with a known critical usability or accessibility defect.
- State what was checked, what passed, and what remains unverified.

## Coverage table

| Flow / screen | Platforms | States checked | Evidence | Not checked |
| --- | --- | --- | --- | --- |

Group full-audit findings by root cause, not by screen. Keep the report compact.
