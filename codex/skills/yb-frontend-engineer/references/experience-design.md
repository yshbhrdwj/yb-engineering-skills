# Experience and visual design

Read relevant sections for a new surface, substantial redesign, or complex journey. Produce only artifacts needed to make decisions and implement the requested scope.

## Choose a direction

Explain the design in a few concrete terms: intended audience/task, visual character, information hierarchy, layout logic, typography, color roles, and one or two distinctive details. Offer alternative concepts only when direction is materially unresolved; do not make every task a moodboard exercise.

Match expression to purpose. Task-heavy applications need efficient scanning and predictable controls; reading surfaces need a comfortable measure and clear structure; marketing needs a credible story and clear action; galleries can let the work dominate. These are decision lenses, not compulsory page templates.

Preserve an established identity on refinements. If no design system exists, define a small coherent set of type, space, color, radius, elevation, and motion decisions; derive reusable tokens without creating an entire component library first. Maintain visual rhythm and content density across actual screens and states. Neither minimalism nor elaborate animation is a universal mark of quality.

## Model the journey

For a meaningful flow, specify entry → decision → action → feedback → next step. Reduce unnecessary choices; reveal advanced controls when needed. Keep location, status, and consequences understandable. Do not hide costs, manufacture urgency, preselect unwanted consent, or obstruct cancellation.

Use realistic content and data extremes. Separate no data, no results, no permission, failure, and loading; each needs an appropriate explanation and next action. Design recovery without losing completed work. For destructive actions, match safeguards to consequences rather than confirming every harmless click.

For complex widgets, record semantics, accessible name, keyboard mapping, focus entry/exit, dismissal, selection, and state announcements. Prefer a simpler native control when a custom one adds little value. Verify platform and assistive-technology behavior rather than assuming that roles alone implement it. [WAI ARIA guidance](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)

## Design across conditions

- Reflow by priority and content needs; check narrow, intermediate, and wide arrangements where layout changes. Tables may need contained scrolling or a different presentation while preserving comparisons.
- Test text enlargement, long names, localization, bidirectional content when supported, and meaningful empty/maximum data. Do not clip necessary labels or disable browser zoom.
- Give controls discernible states and adequate separation. Hover cannot be the only way to discover or operate essential actions. Motion must not be the only carrier of meaning.
- Choose contrast and focus treatment against actual adjacent colors and imagery, including disabled/error/selected variants. Validate the project's applicable WCAG version/level and relevant exceptions; avoid blanket conformance claims. [WCAG reference](https://www.w3.org/WAI/WCAG22/quickref/)

## Compact design handoff

For substantial work, link the source brief and provide: selected direction with rationale, journey/layout, token/component decisions, state and interaction rules, responsive/accessibility behavior, content/assets, accepted versus proposed decisions, and acceptance checks. Keep product policies and unresolved architecture dependencies explicit. Screenshots illustrate an implementation; they do not replace behavior specifications.
