# Platform, design authority, and handoffs

Use when the platform or design authority is not evident. Decide platform, then authority, then path; state the decision in one line. A fast-path fix in a known stack needs none of this.

## Evidence

Search once, batched:

| Evidence | Indicates |
| --- | --- |
| `react-native` or `expo` in `package.json`, `app.json`/`app.config.*`, `ios/` and `android/` | React Native or Expo; `react-native-web` or a `web` platform/script adds a browser target |
| `pubspec.yaml` | Flutter |
| `*.xcodeproj`, `Package.swift`, SwiftUI imports | Native iOS |
| `build.gradle(.kts)` with Compose imports | Native Android |
| `next.config.*`, `nuxt.config.*`, `svelte.config.*`, `angular.json`, web framework dependencies | Web |
| `workspaces` in `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json` | Monorepo; resolve the affected client first |

## Decide

Apply in order; the first input that settles it wins: the requested deliverable, the target runtime, the affected client in a monorepo (scope reads and checks to it), existing architecture, then framework evidence.

- An Expo or React Native app targeting iOS/Android leads with mobile authority. An Expo Web or `react-native-web` screen used in browsers also takes web interaction and accessibility rules: keyboard, focus, URLs, semantics.
- Load one authority. Consult both only for a genuinely cross-platform decision, such as a token or component shared by web and native clients, and say why.
- For an unrecognized framework, say what was found and follow project conventions; ask only when the choice changes the result. Never invent framework support.

## Design authority

| Platform | Consult | If absent |
| --- | --- | --- |
| Web | `yb-web-design-system` | Project design document (`DESIGN.md` or design-system docs), token/theme files, existing components |
| Native mobile | `yb-mobile-design-system` | The same project sources |

Confirm the skill is installed (host skill list or skills folder) before relying on it. If absent, say so in one line and use project sources; never describe what an unread skill contains. An authority is consulted for direction, tokens, and component specifications, not run as an agent. Approved design decisions stay authoritative: implement them, and raise constraints or conflicts as design questions rather than silent deviations.

## Precedence

Explicit user requirement → accepted product decision → approved project design system → platform and accessibility requirements → specialized design guidance → external inspiration. Normative accessibility and safety requirements are never waived because a design system conflicts; state the conflict and its resolution instead of following whichever reference loaded last.

## Handoffs

Pass these fields by file reference; omit any that do not apply. An authority's own handoff table, when present, governs design content.

- **Design → engineering:** platform; affected surfaces; accepted direction; token sources; interaction specifications; accessibility requirements; acceptance criteria.
- **Engineering → reviewer:** revision/build; changed scope; requirements; design authority; raw artifacts (diff, routes or screens, captures); test environment and tools. Never the builder's conclusions.
- **Reviewer → engineering:** confirmed finding; reproduction; impact; correction; verification to rerun.
- **Engineering → QA:** changed functionality; affected journeys; risk areas; test setup (environment, data, devices, flags); existing coverage.
