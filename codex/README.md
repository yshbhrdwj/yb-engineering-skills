# Codex engineering skills

## Install

Extract this bundle, or open this platform directory in the cloned repository. Copy each of the ten complete folders inside `skills/` to one of these locations:

- Personal use: `~/.agents/skills/`
- One repository/team: `<repository>/.agents/skills/`

For example, the resulting file should be `~/.agents/skills/yb-code-design-reviewer/SKILL.md`. Keep its `agents/openai.yaml` file with it. Do not insert an extra bundle directory. If a folder with the same name already exists, compare it before replacing it. These are the current documented local skill locations. [Official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills)

In Codex CLI or the IDE extension, check `/skills` or type `$` to select the skill. In a ChatGPT interface that exposes these skills, use its `@` selector. If discovery does not refresh, restart the host. The target here is the Codex/local-skill workflow; merely attaching the ZIP to an ordinary chat does not install it. [Official invocation and discovery guidance](https://learn.chatgpt.com/docs/build-skills)

Example Codex prompts:

```text
Use $yb-product-strategist to discuss my idea, then produce a product brief for architecture and engineering.
Use $yb-qa-engineer to verify this candidate against the agreed acceptance criteria.
Use $yb-release-operator to assess release readiness and prepare a rollout/recovery plan.
Use $yb-code-design-reviewer to review the current diff against its requirements. Do not edit code.
Use $yb-code-correctness-reviewer to check this change for correctness, scaling, races, and failure behavior.
Use $yb-software-engineer to design and implement this feature using the repository's conventions.
Use $yb-frontend-engineer to design and implement this interface with polished visuals and complete, accessible interactions.
Use $yb-frontend-reviewer to review this UI for UX, visual quality, accessibility, responsive behavior, and interaction defects.
Use $yb-solution-architect to create a complete design a product owner and developer can both understand.
Use $yb-security-privacy to review permissions, sensitive data flows, retention, and deletion.
```

The skills also support automatic selection for matching requests. Each is self-contained and respects applicable `AGENTS.md` guidance and the task's tools, collaboration mode, sandbox, and permissions. Codex display metadata supplies a readable name and starting prompt.

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
