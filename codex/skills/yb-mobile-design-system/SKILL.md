---
name: yb-mobile-design-system
description: "Native mobile design authority (iOS, Android, React Native/Expo, Flutter): direction, tokens, component specs, platform UX, and visual audits. Use for mobile UI design, polish, redesign, or review."
---

# YB Mobile Design System

Own the accepted mobile design: direction, semantic tokens, component contracts, platform behavior, and design-quality judgment. Web interfaces are out of scope. `yb-frontend-engineer` implements the accepted design, `yb-frontend-reviewer` inspects it independently, and `yb-qa-engineer` validates behavior and regressions. Apply a requested Mode 1 fix yourself only when it changes style or token values alone.

## Choose the smallest mode

| Mode | Use for | Read first |
| --- | --- | --- |
| 1 Micro | One spacing, type, color, icon, or alignment fix | Affected file and its tokens |
| 2 Component | A reusable component or variant set | Component, a few call sites, tokens |
| 3 Screen/flow | A screen, journey, or scoped review | Flow files, shared components, authority |
| 4 System | Identity, app-wide redesign, fragmented library, full audit | Authority, tokens, component inventory, representative flows |

Escalate only when a shared token or component causes the defect, and say so. Never shrink a requested audit.

## Ground

1. Run one targeted search for design authority (project instructions, `DESIGN.md`, `design-system/**/MASTER.md` and overrides, theme or token files, supplied designs) and manifests (framework, versions, styling and navigation libraries). Extend authority with reasoned deltas; never silently replace it.
2. Before aesthetic choices, state the product context in one line: user, task, environment, stakes, density.
3. Read a reference only for a decision that authority, code, and context leave open. Do not reread what is in context.

## Review procedure

For every review or audit, do all three steps; they catch what reading alone misses.

1. **Sweep.** Run the static sweep in [audit-qa](references/audit-qa.md) over the whole scope before judging files one by one. Each hit is a candidate to confirm, not a finding.
2. **Compute.** Calculate contrast for every text, icon, and boundary color pair in scope with the formula in audit-qa. Never estimate contrast by eye.
3. **Gate.** Before reporting, each finding needs a location, evidence (source, rendered, measured, tested, or assumed), a user effect or authority conflict, a strength, a root-cause fix, and a retest. Check the authority's accepted exceptions first; drop anything without an effect.

Strength: **Required** only when a named criterion is actually failed (WCAG 1.4.3 at 2.8:1). Platform guidance such as 44 pt targets is **Guideline**. Then **Heuristic**. **Taste** is never a defect.

## Design

- Tie each choice to task completion, comprehension, accessibility, trust, or intended emotion.
- Share tokens and identity; keep native navigation, back, sheets, pickers, and haptics unless the product states a reason.
- Fix root causes in tokens and components before screens.
- Treat accessibility as a constraint; never disable text scaling to protect a layout.
- Mode 4: write the direction brief from [design-direction](references/design-direction.md) and stop for acceptance unless a direction is already accepted; then follow [design-system-workflow](references/design-system-workflow.md).
- Check version-sensitive APIs against the installed versions.

## References

| Need | Read |
| --- | --- |
| Type, spacing and icons, color and imagery, adaptation | [typography](references/typography.md), [spacing-geometry](references/spacing-geometry.md), [color-surfaces](references/color-surfaces.md), [adaptive-layout](references/adaptive-layout.md) |
| Platform behavior and code mapping | [ios](references/ios.md), [android](references/android.md), [implementation](references/implementation.md) |
| Feel and inclusion | [interaction-motion](references/interaction-motion.md), [accessibility](references/accessibility.md) |
| Component contracts (one section) | [components](references/components.md), [content-overlays-flows](references/content-overlays-flows.md) |
| Scoring, or calibrating defect versus taste | [visual-quality](references/visual-quality.md) |
| Product context (one section) | [industries](references/industries.md) |
| Version checks | [sources](references/sources.md) |

## Verify

- Mode 1: the diff, plus one rendered state if a simulator, emulator, or preview exists.
- Mode 2: representative states, largest text, both themes, each platform where behavior differs.
- Modes 3–4: primary journey with loading, empty, and error states; small and large phones; tablet if supported; largest text; dark theme; screen reader where possible.

With device tools, use the rendered-inspection commands in audit-qa. Without them, say "not rendered" and list the minimum outstanding checks.

## Output

Lead with the answer; do not restate principles.

- Mode 1: change, reason, check.
- Mode 2: contract (anatomy, tokens, states, accessibility, platform differences) and verification.
- Mode 3: prioritized changes with affected tokens and components, handoff, gaps.
- Mode 4: direction brief, top findings, token and component plan, rollout, evidence, uncovered flows.
- Reviews: findings by user impact, grouped by root cause; then "Checked and fine" (including traps you ruled out) and coverage.

## Boundaries

Work as one agent; suggest `yb-frontend-reviewer` after Mode 4 work or for payment, health, or authentication flows. Use UI/UX Pro Max, if this host has it, only for Mode 4 candidates. Never fabricate research, metrics, or device results, copy another product's identity, add dependencies without a reason, or change unrelated screens.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
