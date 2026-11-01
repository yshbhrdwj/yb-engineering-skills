# Streak design authority

Approved 2026-10-20 by the product owner. Synthetic fixture for evaluation cases.

## Direction

Streak helps people build small daily habits. It should feel calm, focused, and encouraging; never noisy or guilt-inducing. One primary action per screen.

## Tokens

Values live in `tokens.ts`. Components use semantic tokens and color roles for both themes; no raw values.

## Rules

- Cards: `inset.card` padding, `radius.lg`, `surfaceRaised`, no borders or shadows.
- Numbers: timers and counts use `type.metric` (tabular figures).
- Overlays: editing uses native form sheets with detents.
- Destructive actions: a visible path in addition to any gesture, plus undo.

## Accepted exceptions

- Tab bar labels cap text scaling at 1.5× (2026-10-20) because the bar cannot reflow.
