# Visual quality

Judge an interface across seven lenses, then report a few precise, evidence-labeled findings that point to root causes. Audit procedure and rendered inspection live in `audit-qa.md`.

## Lenses

| Lens | Ask | Typical root cause |
| --- | --- | --- |
| Composition | Is there one clear entry point? Do grouping, rhythm, proportion, balance, and negative space match importance? | Equal spacing and equal weights; too many surfaces |
| Typography | Can levels be told apart at a glance? Are baselines, tracking, line height, and numerals consistent? | Missing type roles; raw sizes in components |
| Geometry | Are paddings, heights, radii, borders, and icon sizes systematic and optically aligned? | Primitive values used directly; per-screen overrides |
| Color | Do roles carry meaning consistently across themes and states? Is contrast sufficient? | Hex in components; dark theme by inversion |
| Interaction | Is feedback immediate, are gestures native and discoverable, is motion meaningful and interruptible? | Custom controls replacing native ones |
| Experience | Is the task clear, learnable, recoverable, accessible, and efficient on repeat use? | Missing states; flows designed for the happy path |
| Identity | Does it fit the audience, feel coherent across screens, and have a reason to be recognizable? | Borrowed style without product reasoning |

## Finding format

Weak: "Cards have inconsistent spacing."

Strong: "Card padding differs between components serving the same hierarchy (`ActivityCard` 12, `GoalCard` 16 in source), weakening the screen's alignment rhythm. Consolidate both on the existing `inset.card` token and verify the rendered layout at the largest text size." *(source; Heuristic)*

Each finding states:

1. **Location**: screen, component, state, platform.
2. **Observation** with evidence label: source, rendered, measured, tested, or assumed.
3. **Why it matters** for the user or for system consistency.
4. **Strength**: Required (a named criterion that is actually failed), Guideline (name the platform), Heuristic, or Taste. Split a finding whose parts differ: a missing accessible name fails WCAG 4.1.2, while a 30 pt target misses platform guidance but passes WCAG 2.5.8. Taste appears only as an optional suggestion.
5. **Root-cause fix**: the token, component, or pattern to change, not a one-off nudge. Note any tradeoff the fix introduces.
6. **Retest**: the specific state and setting that confirms it.

Say "appears" for rendered judgments without measurement. Merge findings with a shared cause. Five strong findings beat twenty repetitive ones. Reporting no defects is a valid result for good work.

## Scoring, only when asked

Score each lens 1–4 and cite the findings behind each score. Never give a score without evidence or an overall number that hides a critical defect.

| Level | Anchor |
| --- | --- |
| 1 Broken | Blocks the task, excludes users, or misleads (unreadable contrast, clipped content at supported settings, broken back) |
| 2 Inconsistent | Works, but the system is not applied: one-off values, competing emphasis, mixed component styles |
| 3 Coherent | System applied consistently; hierarchy clear; platform conventions respected; minor polish issues only |
| 4 Exceptional | Coherent plus deliberate identity, optical precision, complete states, and graceful behavior at extreme settings |

## Subtle defects worth checking

- **Type**: baselines misaligned between adjacent sizes; capitals visually off-center in buttons; captions below 11 pt; titles so large they push the task down; levels too close to distinguish; long text set too wide or too tight.
- **Geometry**: non-concentric nested radii; near-duplicate radii, grays, and paddings; gutters that change between screens; edges that do not align down the page.
- **Icons**: mixed families or optical sizes; glyphs off-center from labels; inconsistent selected states.
- **Numbers**: proportional digits in changing values; decimals not aligned; inconsistent precision or units.
- **Surfaces**: ladders that collapse in dark theme; borders, shadows, and tints stacked on one element; separators heavier than content.
- **Feedback**: missing or inconsistent pressed states; similar transitions with different durations.
- **Content**: screens that work only with short sample text; empty and error states designed less carefully than the default.

## Distinguishing defects from taste

A finding is a defect when it has a user effect (misread, missed, mis-tapped, excluded, slowed, distrusted) or breaks the accepted system. Different-but-valid choices, personal preferences, and pattern bans without an effect are Taste and stay optional.
