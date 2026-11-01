# Claude Code edition

Copy the ten complete folders from `skills/` into `~/.claude/skills/` or `<project>/.claude/skills/`. The source repository installer supports dry runs, backups and migration. Restart the session if discovery does not refresh.

```text
/yb-software-engineer Fix the defect and verify the affected behavior.
/yb-code-reviewer Review this diff against these requirements. Report only.
/yb-merge-pr Merge this PR after checking its exact head, reviews and CI.
```

Descriptions support matching requests automatically. Invocation does not authorize an unrequested merge, deployment or external message. Skills omit model/effort overrides and respect host routing, project instructions and session permissions. [Official skills documentation](https://code.claude.com/docs/en/skills)

The code, frontend and security reviewers use `context: fork`, `agent: Explore`, `background: false`. They receive raw target artifacts and explicit requirements rather than the author's conversation. The built-in Explore agent is read-only; commands or browser capabilities may be unavailable. A user/project agent named Explore overrides the built-in, so inspect its tool policy if one is configured. Reports must say what was actually checked. Foreground mode waits for the result; it does not grant additional tools. [Official subagent documentation](https://code.claude.com/docs/en/sub-agents)

No skill pre-approves broad Bash access or pins a model. `allowed-tools` grants pre-approval in Claude; it is not a read-only tool allowlist, so this pack does not use it as one.

The normal skill installer does not alter settings. Optional merge/Stop hooks have a [separate installation and configuration guide](HOOKS.md). Only opted-in project checks run; hooks supplement permissions, human review, branch rules and CI.

`yb-code-reviewer` replaces the former correctness and design reviewers. Use the source installer's `--update --migrate` to back up and retire those copies. This edition targets Claude Code, not generic claude.ai skill uploads, which accept a different frontmatter subset.
