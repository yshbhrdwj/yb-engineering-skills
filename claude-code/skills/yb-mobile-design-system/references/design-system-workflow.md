# Design-system workflow and handoffs

Use for Mode 4 (new identity, app-wide redesign, fragmented library) and for persisting design decisions. Product discovery belongs to `yb-product-strategist`; reuse its brief instead of repeating discovery.

## Workflow

1. **Inspect.** Product brief or requirements, existing authority and tokens, component inventory (search for duplicated buttons, cards, inputs), and a representative set of screens covering primary journeys, dense data, forms, and empty or error states.
2. **Retain.** Name what works and should survive: recognizable brand elements, well-performing patterns, and accessible components.
3. **Direct.** Write a direction brief (method in `design-direction.md`), grounded in the product and its users. Consult the matching industry section only.
4. **Explore only if undecided.** Two or three genuinely distinct directions applied to the same one or two key screens, compared against the brief's qualities. Do not generate concepts that will not be evaluated.
5. **Define tokens.** Color (both themes), type roles, spacing, radius, border, elevation, motion, icon sizes, component dimensions, and adaptive breakpoints. Check contrast for every role pair. Scale the token system to the app: primitives plus semantic roles suffice for most apps; add component tokens only where variants need independent theming.
6. **Specify components.** Contracts for the components the inventory shows are shared or duplicated, starting with the highest-use ones.
7. **Apply incrementally.** Tokens first, then shared components, then screens by traffic or risk. Each slice is shippable, verifiable, and preserves existing behavior. Hand implementation to `yb-frontend-engineer` with tokens and contracts.
8. **Validate.** Render representative flows on both platforms, compact and large widths, largest text, both themes. Compare against the direction, not against taste.
9. **Document.** Persist decisions in the project's authority file.
10. **Report gaps.** Uncovered flows, deferred components, unverified states.

## Design authority file

Store accepted decisions where the project already keeps them. If none exists, propose `DESIGN.md` at the project root (or the project's docs folder) containing:

- Direction (a short paragraph) and principles specific to the product.
- Token tables or links to the token source of truth in code.
- Component contracts or links to them.
- Platform stance: what is shared, what follows each platform.
- Accepted exceptions with reasons, and a change log with dates.

Code tokens remain the source of truth for values; the document explains intent. Update the document when a change is accepted; propose changes as deltas; never rewrite an approved file wholesale without explicit approval. Page-level overrides are allowed only with a reason and should be rare.

If the project uses UI/UX Pro Max persistence (`design-system/<project>/MASTER.md` with `pages/` overrides), treat `MASTER.md` as the authority and page files as overrides; do not regenerate or force-overwrite it.

## Optional UI/UX Pro Max integration

UI/UX Pro Max (MIT licensed, separately installed) is available only when the host lists its skill or the project contains it; never assume a machine-specific path. It provides searchable palettes, font pairings, style catalogs, product reasoning, and stack guidelines. Use it as a candidate generator, not as authority:

- Mode 4 exploration: one `--design-system` query with product type, audience, and tone; optionally one `--domain color` or `--domain typography` query for a distinct open question.
- Evaluate candidates against platform conventions, accessibility, the product's industry, and existing brand before adopting. Reject web-centric patterns (hover states, landing-page layouts) for native screens.
- Do not use it for Modes 1–2 or to settle questions already answered by authority. This skill does not bundle or require its data.

## Handoff contracts

Pass only what the next role needs, by reference to files where possible.

| To | Contents |
| --- | --- |
| `yb-frontend-engineer` (implements the accepted design) | Scope; authority file and token paths; component contracts or deltas; required states; platform differences; acceptance checks (rendered states, text sizes, themes, screen-reader expectations). The engineer applies framework judgment within the design; conflicts come back as design questions, not silent deviations |
| `yb-frontend-reviewer` (independent UI/UX inspection) | Raw target (revision, screens, build), authority file, acceptance criteria; not the designer's own findings. The reviewer may report flaws in the design system itself |
| `yb-qa-engineer` (behavior and regression validation) | Testable behaviors: states, platform expectations, accessibility requirements, devices and settings to cover, screens sharing changed tokens or components |
| From product intent (brief, requirements, or `yb-product-strategist` when used) | Users, goals, primary journeys, constraints, success measures; reuse instead of rediscovering; never silently redefine requirements |

## Defects to detect in a system

Duplicate components for one job; tokens named by value (`blue16`) instead of role; missing dark-theme or state tokens; one-off overrides that outnumber token use; documentation that disagrees with code; a redesign applied to some screens but not their shared components.
