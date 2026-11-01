# Integration, handoffs, and the design document

This skill consumes product intent, produces design authority, and hands it to builders and verifiers. It does not run the other roles; it names them.

## Routing

| Request | Start with | Then |
| --- | --- | --- |
| "I don't like my website, redesign it" | This skill, Mode 4 | `yb-frontend-engineer` implements; `yb-frontend-reviewer` and `yb-qa-engineer` by scope and risk |
| "Find UI/UX issues in my app" | `yb-frontend-reviewer` | This skill only if the findings call for a new direction |
| "Fix the spacing on this button" | `yb-frontend-engineer` with existing tokens | This skill is not invoked |
| "Design a pricing page" or "a data table component" | This skill, Mode 3 or 2 | Engineer builds the accepted specification |
| "What should we build, for whom?" | `yb-product-strategist` | This skill once goals are accepted |

## Consumed from yb-product-strategist

Goals, audience, primary journeys, accepted experience requirements (`UX-` and other IDs), constraints, and open decisions. Reference them by ID; do not re-derive or rewrite them. If a design decision depends on an open product decision, say which and proceed with a labelled assumption.

## Produced for yb-frontend-engineer

Keep it compact and point to files instead of restating them:

```text
Platform: web (site | app | both); stack and versions observed
Scope: pages/routes and components affected; out of scope
Direction: accepted direction (link to design document section)
Tokens: source files (e.g. app/globals.css @theme, tokens.css); new or changed tokens
Components: contracts added or changed (link); reuse list
Interaction: states, motion tokens, keyboard and focus rules per component
Accessibility: requirements by WCAG criterion; recommendations listed separately
Responsive: content-driven breakpoints and what changes at each
Acceptance criteria: observable checks per page or component
Open decisions and assumptions
```

## Provided to yb-frontend-reviewer and yb-qa-engineer

The persisted design document is the authority they verify against. Point them to it and to the acceptance criteria; do not pre-judge their findings or run them from this skill.

## The design document

Before writing, look for an existing authority and extend it: `DESIGN.md`, `docs/design*`, `design-system/<project>/MASTER.md` (UI/UX Pro Max format: master plus `pages/<page>.md` overrides), token files, or theme config. Do not create a competing document. If none exists, create `DESIGN.md` at the project root unless the project keeps docs elsewhere.

Keep values in code and decisions in the document: the document links the token source and records intent, rules, and status. Structure:

```markdown
# <Product> design system
Status: accepted | proposed   Updated: <date>   Source revision: <commit>
Product context: audience, primary tasks, links to product brief IDs
## Direction            intent, character, signature details, what to avoid
## Tokens               link to token source; role list and usage rules
## Typography           families, scale roles, numerals, measure
## Layout and density   containers, grid, spacing tiers, breakpoints and what changes
## Color and surfaces   ramps, roles, modes, elevation, contrast pairs (computed values)
## Components           contract per shared component, or link to each
## Interaction and motion  durations, easings, reduced-motion rules
## Accessibility        target level, requirements, recommendations
## Page notes           only real exceptions, each with its reason
## Decision log         date, decision, status, reason, superseded-by
```

Rules: record a decision as accepted only when the user accepted it or it is already in shipped, approved code; otherwise mark it proposed. Supersede rather than delete. Page notes are exceptions with reasons, never per-page systems. On later tasks, read this document before any reference file, and change it only with a decision-log entry.
