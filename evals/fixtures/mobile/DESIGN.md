# Hearth design authority

Approved 2026-10-12 by the product owner. Synthetic fixture for evaluation cases.

## Direction

Hearth helps families keep a calm, shared rhythm of sleep, meals, and activity. It should feel warm, unhurried, and trustworthy; never clinical, competitive, or childish. Density is low; one primary action per screen.

## Tokens

Values live in `tokens.ts`. Use semantic tokens only: `inset.screen`, `inset.card`, `gap.section`, `radius.lg` for cards, `radius.sm` for elements inside cards, `type.*` roles, and `color.*` roles for both themes.

## Components

- Cards: `inset.card` padding, `radius.lg`, `surfaceRaised` background, no borders or shadows.
- Primary actions: `PrimaryButton`, one per screen, full width on phones.
- Overlays: native form sheets with detents; no custom JS sheets.
- Member identity: name plus avatar initial; member color never used alone.

## Platform stance

Shared tokens and content; native navigation, back behavior, sheets, and haptics per platform.

## Accepted exceptions

- Tab labels cap text scaling at 1.5× (2026-10-12) because the five-tab bar cannot reflow.
