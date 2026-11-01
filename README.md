# YB Engineering Skills


Ten focused skills for **Claude Code and Codex**. Small changes take a short path: inspect the affected code, reuse what fits, implement, and run relevant checks. Deeper design and independent review follow the risk of the change.

## Choose a skill

| Skill | Use it for |
| --- | --- |
| [`yb-product-strategist`](codex/skills/yb-product-strategist/SKILL.md) | Product choices, UX, assumptions, first-release scope and briefs |
| [`yb-solution-architect`](codex/skills/yb-solution-architect/SKILL.md) | Contracts, data, consequential decisions, failure handling and delivery plans |
| [`yb-software-engineer`](codex/skills/yb-software-engineer/SKILL.md) | Features, fixes and refactors with focused verification |
| [`yb-frontend-engineer`](codex/skills/yb-frontend-engineer/SKILL.md) | Interfaces, complete interaction states and rendered verification |
| [`yb-code-reviewer`](codex/skills/yb-code-reviewer/SKILL.md) | Behavior, concurrency, performance and consequential design defects |
| [`yb-frontend-reviewer`](codex/skills/yb-frontend-reviewer/SKILL.md) | Observed UX, visual, accessibility and interaction defects |
| [`yb-security-privacy`](codex/skills/yb-security-privacy/SKILL.md) | Demonstrable abuse paths, authorization and personal-data lifecycle |
| [`yb-qa-engineer`](codex/skills/yb-qa-engineer/SKILL.md) | Risk-based tests, requirement coverage and readiness evidence |
| [`yb-merge-pr`](codex/skills/yb-merge-pr/SKILL.md) | Authorized PR merges with review, CI and exact-head checks |
| [`yb-release-operator`](codex/skills/yb-release-operator/SKILL.md) | Authorized releases, incidents, recovery and maintenance |

Links open the Codex edition. The [Claude Code edition](claude-code/skills) has the same task instructions with native reviewer-fork metadata. Claude code/security reviews use Explore; frontend review uses a foreground general-purpose fork so available browser tools can be used under normal permissions. No skill pins a model or effort or grants extra permissions; host subagent routing still applies.

## Install and update

The tools require Python 3.10+ and only the standard library. Skills themselves do not require Python, an API key or a hook.

```sh
git clone https://github.com/yshbhrdwj/yb-engineering-skills.git
cd yb-engineering-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

Use `py -3` instead of `python3` on Windows if needed. Choose `--target codex` or `--target claude-code` for one host. Add `--project /path/to/project` for a project installation; otherwise the installer uses your home directory.

| Host | Personal skills | Project skills |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<project>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |

For an existing installation:

```sh
git pull --ff-only
python3 scripts/install.py --target both --update --migrate --dry-run
python3 scripts/install.py --target both --update --migrate
```

`--update` backs up conflicting skills. `--migrate` also backs up and retires the superseded `yb-code-correctness-reviewer` and `yb-code-design-reviewer`, now combined in `yb-code-reviewer`. Backups live outside discovery in `.yb-engineering-skills-backups/` under the installation base. Additional files in active skills and unrelated skills are preserved. Restart the host if discovery does not refresh.

## Use

```text
Use $yb-software-engineer to fix this bug and verify the affected behavior.
Use $yb-code-reviewer to review this diff against the requirements. Report only.
Use $yb-frontend-engineer to implement this screen using the existing design system.
```

Claude Code uses `/yb-software-engineer`, `/yb-code-reviewer`, and so on. Automatic selection is enabled for matching requests. Invocation never authorizes an otherwise unrequested deployment, merge or external message.

## Optional Claude hooks

The separate [hook guide](claude-code/HOOKS.md) covers installation, reviewer configuration and a project check script. The merge hook requires trusted exact-head approval, no outstanding negative review or unresolved thread, and passing required checks. The Stop hook runs only where the project has opted in with a check script, caches successful content checks, and avoids recursive blocking. These are Claude guardrails; Codex uses its own permissions, CI and the shared merge procedure.

The normal skill installer does not edit host settings. Hook installation is a separate explicit command and preserves unrelated settings.

## Evidence and maintenance

- [Start here](START-HERE.md) and [handoffs](SDLC-WORKFLOW.md)
- [Validation and limitations](VALIDATION.md)
- [Independent-review evidence audit](docs/evidence/gemini-review-audit.md)
- [Text size and efficiency](TOKEN-EFFICIENCY.md)
- [Ponytail comparison](PONYTAIL-COMPARISON.md)
- [Public behavioral cases](evals/README.md)

The earlier one-run comparisons do not demonstrate a runtime speed or quality improvement. Shorter instructions reduce loaded text; actual speed and precision need matched repeated trials. This repository reports those distinctions explicitly.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Automatic GitHub CI is disabled. Run the checks locally; the workflow is retained for manual use after explicitly re-enabling it. The last validation run passed on Linux, macOS and Windows. See [contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md). No open-source license grant has been selected.
