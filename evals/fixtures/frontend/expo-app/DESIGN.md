# Parcel design authority

Approved 2026-10-02 by the product owner. Synthetic fixture for evaluation cases.

## Direction

Parcel tracks deliveries for busy people. Calm, legible, and quick to scan; one primary action per screen.

## Tokens

Values live in `theme.ts`. Use theme values only; no raw colors or sizes in components.

## Components

- List rows: `space.lg` horizontal and `space.md` vertical padding, minimum height `minTouch`.
- Buttons: minimum target `minTouch`; primary uses `color.accent` with `color.onAccent` text.
- Forms: visible labels; the focused field and primary action stay above the keyboard.

## Platform stance

Shared tokens; native stack navigation, back behavior, and sheets per platform. Text scaling is never disabled on body or titles.

## Accepted exceptions

None.
