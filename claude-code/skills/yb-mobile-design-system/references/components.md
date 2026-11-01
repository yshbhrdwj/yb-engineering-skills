# Components: shared contract, navigation, actions, inputs

Read the shared contract, then only the section for the component in question.

## Shared contract

Specify a component with these fields; omit a field only when it truly does not apply.

1. **Purpose and use**: the job, when to use it, and the nearest alternative it should not replace.
2. **Anatomy**: named parts (container, leading element, label, supporting text, trailing element, indicator).
3. **Hierarchy**: which part is read first and why.
4. **Geometry**: height, padding, gap, radius, border, and icon size as semantic tokens; minimum target size.
5. **Type and color**: type roles and color roles per part, in both themes.
6. **States**: default, pressed, focused (keyboard and switch access), selected or checked, disabled, loading, success, error, empty, and dragged, only where the component supports them. Each changes at least one non-color property. Loading and failure behavior says what the user sees and can do.
7. **Gestures, keyboard, and accessibility**: supported gestures and their visible alternatives; keyboard type and return action for inputs; role, name source, state and value exposure, grouping, announcements, behavior at the largest text size.
8. **Platform differences**: what stays shared (tokens, content, brand) and what follows the platform (navigation, pickers, sheets, haptics, pressed feedback).
9. **Responsive behavior**: compact, medium, and expanded widths; long and localized content.
10. **Common defects** and **verification**: which states and settings to render.

Shared rules that apply to every component:

- Variants are justified by different jobs, not by different screens. Prefer one component with a few props over near-duplicates.
- All visual values come from tokens; optical corrections live inside the component.
- Heights grow with text; never clip labels.
- Pressed feedback is immediate; disabled states explain themselves where possible.

## Navigation

- **Bottom tabs / navigation bar**: three to five top-level destinations with icon and label; selected state uses fill or indicator plus label color; badges for counts carry an accessible description. iOS: tab bar with platform material, minimize-on-scroll where supported. Android: Material navigation bar with active indicator, always visible. Defects: action items in tabs, more than five destinations, unlabeled icons, content under the bar.
- **Headers / top app bars**: title, back or up, at most two or three actions plus overflow. Large titles (iOS) or medium/large app bars (Android) for top-level screens only. Defects: centered titles on Android where the system uses leading alignment without reason; overloaded action sets; custom back that breaks gestures.
- **Top tabs**: switching between peer views of the same content; swipeable on Android; segmented control on iOS for two to five views. Defects: tabs that change data scope unexpectedly; scrolling tabs with hidden active item.
- **Navigation rail and drawer**: rail for medium and expanded widths with three to seven destinations; drawer for many or infrequent destinations. Defects: drawers as the only navigation on phones for frequent destinations.
- **Back controls**: platform-native; labeled back on iOS; system back on Android, with up arrow in the app bar. Confirm only for unsaved input.
- **Search**: system search field or a search destination; recent and suggested queries; clear button; cancel returns to prior state; results stay while refining; empty results suggest alternatives.
- **Step-based navigation**: for linear tasks (checkout, onboarding, applications), show position ("Step 2 of 4" or a progress bar), keep back non-destructive, preserve entered data between steps, and allow review before commit. Breadcrumbs rarely fit phones; use a clear title, back label, or a step indicator instead.

## Actions

- **Primary button**: one per view or section; filled; label is a specific verb ("Pay $24.00", "Save workout"). Height 44–56 depending on product density; full width on compact phones for primary flows, intrinsic width otherwise. Loading shows progress inside the button and blocks duplicates. Defects: multiple competing primaries; generic labels ("Submit", "OK"); disabled primaries with no explanation of what is missing.
- **Secondary and tertiary**: tonal, outlined, or text buttons; visibly lower emphasis but still clearly tappable (3:1 boundary contrast for outlined).
- **Icon button**: 24 icon in a 44 pt / 48 dp target; accessible name; tooltip or long-press label on Android where helpful. Toggle icon buttons expose selected state.
- **Floating action**: Android FAB for the primary constructive action; avoid on iOS unless the product design system deliberately uses it. Keep clear of navigation bars and snackbars.
- **Segmented control / button group**: two to five mutually exclusive options of the same type; equal widths when labels allow; selected state not by color alone.
- **Destructive actions**: separated from safe actions, destructive styling, confirmation that names the consequence, undo when feasible instead of confirmation for reversible deletes.
- **Contextual and swipe actions**: context menus (long press) and swipe actions accelerate frequent actions on list items; every one also appears in a visible place (detail screen, overflow menu, edit mode) and as an accessibility custom action. Full-swipe triggers only safe or undoable actions.

## Inputs

- **Text field**: persistent visible label (not placeholder-only); supporting text for format or constraints; error replaces or augments supporting text with a specific fix; correct keyboard and autofill; clear button for search-style fields. Height grows with scaled text. States: empty, focused, filled, error, disabled, read-only.
- **Search field**: leading search icon, clear button once text exists, cancel on iOS, search keyboard action; results update with debounce and keep focus; recent searches are removable.
- **Selectors and pickers**: platform picker or menu for short lists; searchable list screen for long lists; show the selected value in the field. Dates use platform date pickers unless a custom calendar adds real value (ranges, availability).
- **Checkbox, radio, switch**: checkbox for independent multi-select; radio for one of a small set (consider a list with checkmarks on iOS); switch only for immediate effect. Entire row is the target; label is clickable.
- **Slider**: continuous or stepped values where approximate is fine; show the value; provide a text or stepper alternative for precise input; expose value to assistive technology.
- **Stepper / numeric field**: numeric keyboard; bounds communicated; long press to repeat only with clear feedback.
- **Financial amount**: decimal keyboard with the locale's separator; format as typed without moving the cursor; currency shown once in a fixed position; tabular figures; limits and fees shown before confirmation; the value read aloud with its currency.
- **OTP / verification code**: one logical field (even if drawn as boxes) with one-time-code autofill, paste support, numeric keyboard, resend timer with accessible countdown, and clear error for expired codes.
- **Forms and multistep forms**: ask only what is needed; group related fields under headings; validate on blur or submit, not on every keystroke for incomplete input; place errors at the field and, for long forms, summarize with links to each; keep the submit action reachable above the keyboard and labeled with its outcome; save drafts for long or interruptible forms; split into steps only when steps are meaningful units.

Sources: Apple HIG components; Material 3 components (see sources.md).
