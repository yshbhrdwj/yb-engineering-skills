# iOS and iPadOS

Native iOS behavior is a usability contract: people expect edge-swipe back, sheets that dismiss downward, and controls that respond like system controls. Brand lives in content, color, type, and iconography, not in reinventing these behaviors.

Why it matters: people build muscle memory across every app on the device. Matching system behavior means nothing new to learn, assistive technologies work as expected, and the app inherits future OS improvements. A coherent custom visual style is fine; custom behavior that breaks these expectations is a usability cost that needs a reason.

Version note: iOS 26 introduced a new material system (Liquid Glass) for navigation and controls, floating and minimizing tab bars, and concentric control shapes; later releases adjusted it. Check the deployment target and the SDK the app builds with, and verify current guidance before depending on version-specific behavior.

## Navigation

- **Hierarchical (push).** Navigation bar with back button labeled by the previous title (or a chevron when space is short). Never block the interactive edge-swipe back gesture, including in custom headers; a screen with unsaved work should confirm on leave rather than disable back.
- **Large titles** suit top-level and content-browsing screens and collapse into the inline bar on scroll; use the standard title for detail and task screens. Do not mix both in one level.
- **Tab bar** switches between top-level peer sections; it is never an action launcher. Keep three to five tabs on iPhone (Guideline). Tabs preserve their own navigation state; re-tapping the active tab scrolls to top or pops to root. Hide the tab bar only for immersive or focused tasks, consistently. Current iOS versions float the tab bar over content, can minimize it on scroll, and support a distinct search tab and an accessory above the bar; content must remain readable underneath it.
- **Toolbars** hold actions for the current screen. Group related actions; put the primary action at the trailing edge of the navigation bar (Done, Save) and keep destructive actions separated.
- **Search** uses the system search field in the navigation bar or a search tab; show recent and suggested results before typing when helpful.

## Presentation

- **Sheets** for scoped tasks that return to context. Use detents (medium, large, custom) only when the partially expanded state is useful on its own. Show the grabber when resizing is possible. Swipe-down dismissal must not lose input silently: confirm or save a draft.
- **Full-screen modals** for immersive or multistep tasks, with explicit Cancel and Done or Save.
- **Alerts** are for critical information or confirming destructive, irreversible actions; keep them rare, titles short, and buttons verbs. Mark destructive actions with the destructive style; Cancel uses the cancel style.
- **Confirmation dialogs and menus**: pull-down menus attach to a button for related actions; context menus appear on long press and must have a visible alternative path. Action sheets present choices about an action the person started.
- **Popovers** on iPad anchor to their source; on iPhone the same content usually becomes a sheet.

## Lists, forms, and controls

- Inset grouped lists for settings and forms; plain lists for content feeds. Section headers and footers explain groups; footers carry consequences or help text.
- Swipe actions: trailing for destructive or primary actions, leading for secondary; full swipe only for safe or undoable actions. Provide the same actions in a context menu or edit mode.
- Use system controls: toggles for immediate binary settings, segmented controls for two to five mutually exclusive views of the same content, steppers for small increments, date pickers in compact, inline, or wheel style according to context.
- Text input: correct keyboard type, content type for autofill (one-time codes, passwords, addresses), return key labeled for the action. The keyboard can be dismissed interactively by scrolling; keep the focused field visible and offer an input accessory only when it adds real controls.
- System iconography: SF Symbols for system concepts (share, delete, more) keep meaning familiar; custom icons for brand concepts.

## Feedback, haptics, and motion

- Haptics follow system meaning: selection changes, impacts for physical collisions, notifications for success, warning, and error. Use them for confirmation of meaningful events, not every tap. They respect system settings automatically through the standard APIs.
- Motion is spring-based and interruptible; navigation transitions should follow the gesture and reverse when released early. Respect Reduce Motion by replacing movement with fades or cross-dissolves.

## Layout and environment

- Respect safe areas, the Dynamic Island and camera housing, and the home indicator region. Backgrounds extend edge to edge; controls stay inside safe areas.
- Support Dynamic Type through all accessibility sizes for content; switch horizontal layouts to vertical at accessibility sizes.
- Honor Bold Text, Increase Contrast, Reduce Transparency, Button Shapes, Smart Invert (exclude photos and media), and Differentiate Without Color.
- Status bar style matches the content beneath it in both themes.

## iPad

- Use regular size classes for split views and sidebars; tab-based apps can adapt to a sidebar. Layouts must survive multitasking widths, window resizing, and rotation.
- Support pointer hover effects and keyboard shortcuts for frequent actions; keep targets usable by touch.
- Constrain reading widths; avoid stretched phone layouts.

## Requirements commonly missed (verify current text)

- App Review requires in-app account deletion when the app supports account creation.
- Apps offering third-party or social login must also offer an equivalent privacy-preserving login option under current App Review rules; check exceptions.
- Subscription screens must show price, period, and renewal terms clearly before purchase.

## Defects to detect

Custom back buttons that disable edge swipe; tab bars used for actions; modal stacks more than one level deep; sheets that lose input on dismiss; alerts for non-critical information; non-system controls that ignore Dynamic Type; content hidden under a floating tab bar or home indicator; large titles on detail screens; hamburger drawers replacing a tab bar without a reason.

Sources: Apple HIG (Navigation, Tab bars, Sheets, Alerts, Menus, Lists, Haptics, Motion, Accessibility, Layout); App Review Guidelines (see sources.md).
