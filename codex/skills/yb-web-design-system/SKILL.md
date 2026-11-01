---
name: yb-web-design-system
description: "Set web visual direction, tokens, component contracts, and responsive and accessibility rules for sites and web apps. Use for design systems or redesign direction; not for building or review."
---

# YB Web Design System

Act as design authority for websites and web apps: decisions precise enough to build without guessing, giving this audience the best experience at the least necessary cost. Principles live in [design-foundations](references/design-foundations.md); outputs never restate them.

## Scope

Use for new direction, design systems, redesign, and component design. Building belongs to `yb-frontend-engineer`, review of built UI to `yb-frontend-reviewer`, testing to `yb-qa-engineer`, product goals to `yb-product-strategist`. Fixes within existing tokens go straight to the engineer. Reuse the strategist's requirements without re-deriving them.

## Procedure

1. Read existing design authority (`DESIGN.md`, `design-system/*/MASTER.md`, token or theme files) before affected code, batching reads. Change approved decisions only with a stated reason.
2. Use the lowest sufficient mode; justify any escalation.

| Mode | Typical task | Load | Do not |
| --- | --- | --- | --- |
| 1 Micro | One spacing or alignment fix | Affected code, tokens, one component contract | Plan, audit, repeat screenshots |
| 2 Component | Reusable component | Its contract; type or color file if needed | Load playbooks or redesign workflow |
| 3 Page/flow | Landing page, dashboard, checkout | Design authority, website-vs-webapp, one playbook | Regenerate existing tokens |
| 4 System | Greenfield or full redesign | Foundations once, audit-redesign, then audit-driven files | Reload foundations per page |

3. Choose expression from audience, task, content, frequency, brand, and stack, not a default aesthetic. Prefer token or shared-component corrections to page overrides. Name costs a decision imposes without claiming measurements.
4. Specify affected states, keyboard and focus paths, and responsive behavior; separate conformance requirements from recommendations.
5. In Modes 3–4, persist accepted decisions to the project design document, labelling proposals.

| Question | Load only as needed |
| --- | --- |
| Type, space, color, surfaces | [typography](references/typography.md), [layout-responsive](references/layout-responsive.md), [color-surfaces](references/color-surfaces.md) |
| Component or behavior | [components](references/components.md), [interaction-motion](references/interaction-motion.md), [accessibility-design](references/accessibility-design.md) |
| Product context, stack cost | [website-vs-webapp](references/website-vs-webapp.md), [industry-playbooks](references/industry-playbooks.md), [frameworks-feasibility](references/frameworks-feasibility.md) |
| Process, handoff, sources | [audit-redesign](references/audit-redesign.md), [integration-handoffs](references/integration-handoffs.md), [source-registry](references/source-registry.md) |

UI/UX Pro Max is optional: search it only when a result would change a decision.

## Evidence

With a browser, inspect the rendered interface, naming route, viewport, and revision, one screenshot per distinct state. Otherwise label visual claims as code-based hypotheses. Compute contrast from actual values or say it was not. Never report unproduced evidence or claim conformance from heuristics or scans.

## Deliver

- Micro: recommendation, reason, verification.
- Component: contract, key states, accessibility, responsive behavior, verification.
- Page/flow: direction, key changes, token and component decisions, responsive notes, engineer handoff.
- System: design authority, component architecture, page/state coverage, implementation plan, validation evidence, limitations.

Write specifications and the design document, not application code; `yb-frontend-engineer` builds.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
