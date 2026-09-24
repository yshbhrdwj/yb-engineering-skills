# Claude Code engineering skills

## Install

Extract this bundle, or open this platform directory in the cloned repository. Copy each of the ten complete folders inside `skills/` to one of these locations:

- Personal use: `~/.claude/skills/`
- One repository/team: `<repository>/.claude/skills/`

For example, the resulting file should be `~/.claude/skills/yb-code-design-reviewer/SKILL.md`. Keep the skill folder immediately below `skills/`; do not insert an extra bundle directory. If a folder with the same name already exists, compare it before replacing it. These are Claude Code's documented personal and project locations. [Official Claude Code skills documentation](https://code.claude.com/docs/en/skills)

Open Claude Code and check `/skills`. Restart the session if a newly created skills directory does not appear. Then try one of these prompts:

```text
/yb-product-strategist Discuss my idea, then produce a product brief for architecture and engineering.
/yb-qa-engineer Verify this candidate against the agreed acceptance criteria.
/yb-release-operator Assess release readiness and prepare a rollout/recovery plan.
/yb-code-design-reviewer Review the current diff against its requirements. Do not edit code.
/yb-code-correctness-reviewer Check this change for correctness, scaling, races, and failure behavior.
/yb-software-engineer Design and implement this feature using the repository's conventions.
/yb-frontend-engineer Design and implement this interface with polished visuals and complete, accessible interactions.
/yb-frontend-reviewer Review this UI for UX, visual quality, accessibility, responsive behavior, and interaction defects.
/yb-solution-architect Create a complete design that a product owner and developer can both understand.
/yb-security-privacy Review this feature's permissions, sensitive data flows, retention, and deletion.
```

The skills can also be selected automatically from matching requests. Explicit invocation is useful when you want a particular review lens. Each skill is self-contained and respects applicable `CLAUDE.md` guidance and the session's tools, planning mode, and permissions.

## Skill selection

| Name | Use it for |
| --- | --- |
| `yb-product-strategist` | Idea discussion, product strategy, UX, architect/engineer handoffs |
| `yb-qa-engineer` | QA strategy, tests, user journeys, release evidence |
| `yb-release-operator` | Release planning/execution, recovery, incidents, operations |
| `yb-code-design-reviewer` | Clean code, SOLID, structure, consistency, maintainability |
| `yb-code-correctness-reviewer` | Behavior, DSA, performance, concurrency, consistency |
| `yb-software-engineer` | Planning and designing before implementation, then verification |
| `yb-frontend-engineer` | UI/UX direction, visual systems, responsive implementation, accessible interactions |
| `yb-frontend-reviewer` | Evidence-based UI/UX, visual, accessibility, responsive, and interaction review |
| `yb-solution-architect` | Plain-language and technical architecture documentation |
| `yb-security-privacy` | Security review, threat modeling, privacy lifecycle |

For large changes, discover → design → implement → QA/reviews → release/operate → learn is a useful sequence. Use only the roles that the task needs. Supply known requirements and constraints; leave unknowns explicit.

The bundle contains instruction skills, without runtime hooks or marketplace installation. Platform guidance checked on 24 September 2026. Validation and comparison notes are included alongside this guide.

See the included SDLC-WORKFLOW.md and TOKEN-EFFICIENCY.md for handoffs and selective reference loading.
