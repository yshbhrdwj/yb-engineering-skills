# Specialized SDLC skills

Ten stack-agnostic YB roles for Claude Code and Codex, from idea discussion to operation and product learning. Each includes a rule to follow applicable best practices, verify uncertain/version-sensitive guidance, and explain justified exceptions or conflicts with obsolete conventions.

| Skill | Responsibility |
| --- | --- |
| `yb-product-strategist` | Discuss ideas, explore concepts, test business assumptions, define UX and scope, produce architect/engineer handoffs |
| `yb-solution-architect` | Turn the brief into an understandable, implementable system design |
| `yb-software-engineer` | Plan before coding, implement, and verify the requested change |
| `yb-frontend-engineer` | UI/UX direction, visual systems, responsive implementation, accessible interactions |
| `yb-frontend-reviewer` | Evidence-based UI/UX, visual, accessibility, responsive, and interaction review |
| `yb-qa-engineer` | Risk-based QA, test creation/execution, user-journey and quality evidence |
| `yb-code-design-reviewer` | Clean code, SOLID, maintainability, architectural consistency |
| `yb-code-correctness-reviewer` | Functional correctness, DSA, performance, concurrency, consistency |
| `yb-security-privacy` | Security controls, threats, permissions, personal-data lifecycle |
| `yb-release-operator` | Release readiness, authorized deployment, observability, recovery, incidents, maintenance, retirement |

[Claude Code setup](claude-code/README.md) · [Codex setup](codex/README.md) · [SDLC workflow](SDLC-WORKFLOW.md)

## Start with an idea

In Codex:

```text
Use $yb-product-strategist to discuss my idea: [describe it].
Challenge the assumptions, explore different approaches, and help me choose what to validate first.
```

When ready:

```text
Use $yb-product-strategist to finalize our decisions into one product brief
with separate architect and engineer handoffs. Preserve open questions and scope boundaries.
```

In Claude Code, use `/yb-product-strategist` with the same request. The skill uses founder and product-design judgment without inventing professional credentials or research.

## How the roles connect

A substantial product usually flows from product brief → architecture → implementation → QA/review → release/operations → learning. Security, privacy, accessibility, and operability are addressed at the stages where they matter. Small fixes use only the relevant roles.

The product brief is the source of product intent. Stable requirement IDs connect it to architecture decisions, implementation, tests, and release evidence. Accepted intent, implementation progress, verified behavior, and release authorization remain distinct. The workflow is guidance, not an automatic pipeline or continuous monitoring service.

## Token efficiency

Short skill entrypoints carry essential decisions and evidence rules. Detailed checklists are separate references loaded only for relevant work. Skills favor targeted inspection, concise findings, one authoritative requirements register, and updates to changed decisions. They avoid repeated summaries and mandatory full-lifecycle reviews for small tasks.

Conciseness never permits missing requirements, invented results, skipped meaningful checks, or incomplete requested deliverables. See [validation](VALIDATION.md) and [measured text reductions](TOKEN-EFFICIENCY.md). Text reduction is not a guarantee of proportional runtime token or cost savings.

Both platform editions share the core engineering rules and have their own host guidance; Codex also includes display metadata. Each skill works independently with the host's available tools. No extra plugin, API key, or runtime hook is required by the pack.

## Frontend work

Use `yb-frontend-engineer` to turn the product journey and architecture constraints into a coherent UI and working code. Use `yb-frontend-reviewer` for an independent assessment of rendered UI and frontend behavior. Both preserve the accepted brand and distinguish verified evidence from assumptions. They work independently; the other eight roles are used only when needed.

```text
Use $yb-frontend-engineer to design and implement [surface] in this project.
Use $yb-frontend-reviewer to review [route or change] for UX, visual quality, accessibility, responsive behavior, and interaction defects.
```

Claude Code uses `/yb-frontend-engineer` and `/yb-frontend-reviewer` with the same requests.
