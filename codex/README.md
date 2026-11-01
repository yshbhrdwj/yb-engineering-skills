# Codex edition

Copy the eleven complete folders from `skills/` into `~/.agents/skills/` or `<project>/.agents/skills/`, retaining `agents/openai.yaml`. The repository installer supports dry runs, backups and migration; see the root README when using the source checkout. Restart Codex if discovery does not refresh.

```text
Use $yb-software-engineer to fix the defect and verify the affected behavior.
Use $yb-code-reviewer to review this change against the supplied requirements. Report only.
Use $yb-merge-pr to merge this PR after checking its exact head, reviews and CI.
```

Codex can select skills from matching descriptions, or you can invoke them through `$` or `/skills`. The edition keeps name/description in `SKILL.md` and UI prompts in `agents/openai.yaml`. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)

The skills inherit the selected model, effort, tools, permissions and applicable `AGENTS.md`. A review skill asks for an independent reviewer with raw artifacts when the host supports delegation. It does not itself enforce a new context or read-only tools; those are host controls. If delegation is unavailable, report that limitation and perform a separately scoped review without claiming independence.

The optional Claude hooks are not installed into Codex. Use the shared merge procedure with existing Codex permissions, repository rules, required checks and reviewer configuration. Automatic skill selection is not authorization for a merge, deployment or external message.

`yb-code-reviewer` replaces the former correctness and design reviewers. Use `--update --migrate` in the source installer to back up and retire those copies. The bundle includes skills and platform documentation; source repository helpers and behavioral cases remain available on GitHub.
