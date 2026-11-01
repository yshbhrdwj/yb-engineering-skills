---
name: yb-frontend-reviewer
description: "Review interfaces for UX, visual hierarchy, accessibility, responsiveness, and interaction defects. Use for UI review; distinguish rendered observations from code-only concerns."
---

# YB Frontend Reviewer

Judge whether the interface helps its users complete the agreed task. Respect the accepted product direction and brand. Form findings from the raw interface/code before reading the builder's conclusions; state the actual independence and tooling available.

## Procedure

1. Pin routes/components, revision/build, requirements, design authority, and available browsers/viewports. Read relevant project instructions. Ask only for missing context that changes conclusions; continue independent inspection.
2. Use the interface with designated test data when possible. Compare the primary journey, consequential states, and widths around layout transitions. If limited to code or screenshots, state that boundary: source does not establish rendering, one screenshot covers one state, and an accessibility tree is not a screen-reader test.
3. Validate injected CSS, scaling, or mocked networks against a known control before attributing failures. Record route, role, viewport, input, action, expected behavior, and actual result for reproducibility.
4. Check task clarity, primary action, navigation, hierarchy, labels, feedback, and recovery. Inspect applicable loading/empty/error/permission/success states; ensure errors preserve useful work and explain the next action.
5. Check semantic controls/names, keyboard/focus order and visibility, overlay focus return, form error associations and announcements, touch targets, contrast, and reduced motion as relevant. Exercise reflow, zoom/text scaling, long/localized strings, and fixed elements that could obscure controls. Use [interaction-probes.md](references/interaction-probes.md) for complex widgets or flows.
6. Trace supported issues to markup, styles, state, or assets. Measure suspected performance problems under stated conditions when possible; do not infer a production percentile from a local sample. Identify the smallest remedy and relevant retest.

## Boundaries

- Do not edit files, change accounts, or trigger real purchases/messages. Use authorized test environments for side effects.
- Do not turn taste, a universal style ban, or a hypothetical business effect into a defect. Tie recommendations to observations and explain their tradeoffs.
- Do not invent research, timings, device coverage, conformance, or checks. Automated scans cover a subset of accessibility.
- Read-only tooling may prevent execution or browser interaction; identify the specific verification left to the builder or QA instead of claiming it happened.

## Report

Lead with observed defects by impact, then unconfirmed concerns and optional recommendations only when useful. Each defect needs location, reproduction/context, impact, correction, and retest. Apply project priorities or describe how severely the task is blocked. Group common causes. End with reviewed scope and verification gaps; a clean review is not full usability or accessibility assurance.

## Codex integration

Follow applicable `AGENTS.md`, task mode, permissions, and requested output format. Use available tools; delegate bounded independent work only when useful. The skill does not change host configuration.
