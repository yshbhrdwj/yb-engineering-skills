# Tally design authority

Approved 2026-09-30. Synthetic fixture for evaluation cases. Shared by the web app and the mobile app.

## Tokens

Values live in `packages/ui/tokens.ts`; both apps import them. Add new values there, never in an app.

## Status badge

- Light theme: neutral badge text `#374151` on `#F3F4F6`.
- Dark theme (approved 2026-10-28): neutral badge text `#6B7280` on `#1F2937`, chosen to keep badges quiet next to amounts.
- Badges are 12/16 semibold text with 4 by 8 padding and fully rounded corners.

## Platform stance

Shared tokens and content. Web follows browser conventions; mobile follows native conventions.
