# Design audit and redesign workflow

Use the audit to decide what to change; use the workflow to change it coherently. The audit is a design critique for setting direction. Independent defect review of a built interface belongs to `yb-frontend-reviewer`.

## Audit lenses

1. **Aesthetic quality:** coherent direction; hierarchy that leads the eye; type, spacing, color, and surfaces drawn from consistent sets; distinctiveness against generic defaults; craft details (alignment, rhythm, proportion).
2. **Functional UX:** primary task obvious; navigation predictable; feedback and recovery present; content density fits usage frequency; no dark patterns.
3. **Consistency:** count distinct values in use (colors, font sizes, radii, shadows, spacing, control heights). Many near-duplicates mean missing tokens. Same component rendered differently across pages means missing shared components.
4. **Responsiveness:** behavior at narrow, intermediate, and wide widths, at 200% text, and with coarse pointers; primary action reachable.
5. **Accessibility:** structure, focus, contrast (computed), targets, labels and errors, motion; requirements versus recommendations as in accessibility-design.
6. **Technical practicality:** what the stack makes cheap or expensive; layout stability; asset cost.

A fast static sweep often finds the root causes: search stylesheets for raw hex values, pixel font sizes, `!important`, one-off `margin` offsets, `outline: none`, `100vh`, fixed widths, and `role="menu"` or click handlers on non-interactive elements. Report counts and locations you actually found.

## Findings format

Each material finding states:

- **What:** the observed problem in specific terms.
- **Where:** file and line, component, or route and viewport.
- **Why it matters:** the user or business consequence.
- **Evidence:** what was observed and how (rendered at route, viewport, and revision; computed value; code reading). Code-only visual claims are labelled hypotheses.
- **Root cause, if known:** missing token, divergent component, wrong pattern.
- **Correction:** the specific change, at the lowest shared level that fixes it.
- **Verification:** how to confirm the fix.

Separate **defects** (break a requirement, task, or accepted rule) from **suggestions** (optional improvements, with their tradeoff). Do not inflate taste into defects.

Banned feedback: anything that does not say what to change, such as "make it more premium", "add some polish", "make it pop", "feels off", or "modernize it". Translate the intuition into a specific decision: "Reduce the hero heading from 72px to 56px and set tracking −0.02em, so the subhead and CTA enter the first view at 1280×720."

## Redesign phases

1. **Understand.** Read the product goals and requirements from `yb-product-strategist` artifacts or the user; do not re-derive them. Identify audience, primary tasks, brand assets that must survive (logo, name, voice, colors with equity), content, stack, and constraints. Read any existing design document.
2. **Audit.** Apply the lenses; record what works as well as what fails. What works is preserved by default.
3. **Explore a few directions.** Two or three genuinely different directions only when direction is unresolved; one well-argued direction when the brief already constrains it. Describe each by intent, type, color, layout, density, and one or two signature details, and show it on the product's real key screen, not on a generic sample. Recommend one with reasons tied to audience and goals.
4. **Establish authority.** Once a direction is accepted, define tokens (ramps and roles, type scale, spacing, radii, elevation, motion), surfaces, shared component contracts, responsive rules, motion rules, and accessibility requirements. Write them to the project design document (integration-handoffs) and into the stack's token source.
5. **Apply consistently.** Redesign shared components first, then templates, then pages. Pages change by composing shared parts; page-level overrides need a recorded reason. Never change unrelated behavior: routes, form actions, analytics, data contracts, copy with legal meaning, and URLs stay unless the scope says otherwise.
6. **Validate.** With a browser, check the key routes at representative widths and states, one screenshot per distinct state, naming route, viewport, and revision. Without one, list the visual checks still required. Compute contrast for new pairs.
7. **Document and persist.** Record accepted decisions, rejected alternatives worth remembering, and open questions in the design document; hand implementation and verification to the other roles.

## Greenfield versus redesign

Greenfield starts at phase 1 with no audit; spend the saved effort on direction and on contracts for the components the first release actually needs, not a speculative library. Redesign starts from evidence of what exists and earns every change against it.
