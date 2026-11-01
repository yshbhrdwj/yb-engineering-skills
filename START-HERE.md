# Start here

Use one role for a small task. Add specialists only where they resolve a distinct risk or requested question.

| Request | Start with |
| --- | --- |
| Explore an idea or decide scope | `yb-product-strategist` |
| Decide contracts, data or system boundaries | `yb-solution-architect` |
| Implement a feature or fix | `yb-software-engineer` |
| Build or refine an interface | `yb-frontend-engineer` |
| Decide mobile visual direction, tokens, component specs or a design audit | `yb-mobile-design-system` |
| Review a code change | `yb-code-reviewer` |
| Review the interface people use | `yb-frontend-reviewer` |
| Check security or personal-data handling | `yb-security-privacy` |
| Verify acceptance and readiness | `yb-qa-engineer` |
| Merge an authorized PR | `yb-merge-pr` |
| Plan or execute operations | `yb-release-operator` |

In Codex, mention `$yb-software-engineer`. In Claude Code, invoke `/yb-software-engineer`. Supply the target, intended behavior, known constraints and relevant evidence. A reviewer in Claude runs in a fresh subagent (Explore for code/security, general-purpose for frontend); include requirements and exact target in the invocation because it cannot see the author's conversation.

For a routine fix, the engineer inspects the affected path and callers, uses the smallest complete solution, and runs targeted checks. Shared state, retries, authorization and migrations warrant a short design and focused independent review. A requested full document remains complete; compact chat reporting does not limit the deliverable.

For changes that keep state, check applicable cases: two operations at once; old code or data meeting new code; failure followed by retry; the first item beyond a limit. A documented shortcut is still reviewed against actual requirements.

Installation and migration commands are in the [README](README.md). Platform details are in the [Claude Code](claude-code/README.md) and [Codex](codex/README.md) guides. Optional hooks have a [separate setup](claude-code/HOOKS.md).

For frontend work (redesign, defect hunt, new page or screen, small visual fix), the [frontend routing table](SDLC-WORKFLOW.md#frontend-routing) shows which skills to use and which to skip.
