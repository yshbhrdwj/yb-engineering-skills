# YB Engineering Skills

[![Validate](https://github.com/yshbhrdwj/yb-engineering-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/yshbhrdwj/yb-engineering-skills/actions/workflows/validate.yml)

Ten focused, stack-agnostic skills for **Claude Code and Codex**, covering product discovery through design, implementation, review, testing, and operations.

Each skill plans proportionately, follows relevant best practices, preserves requirements, and distinguishes evidence from assumptions. Short entrypoints carry the core decisions; detailed references load only when needed. Use one specialist for a small task or combine roles for a larger delivery.

## The skills

| Skill | Responsibility |
| --- | --- |
| [`yb-product-strategist`](codex/skills/yb-product-strategist/SKILL.md) | Explore ideas, challenge business assumptions, define UX, create architecture and engineering handoffs |
| [`yb-solution-architect`](codex/skills/yb-solution-architect/SKILL.md) | Explain complete, implementable system designs to technical and nontechnical readers |
| [`yb-software-engineer`](codex/skills/yb-software-engineer/SKILL.md) | Plan and design before implementing and verifying changes |
| [`yb-frontend-engineer`](codex/skills/yb-frontend-engineer/SKILL.md) | Design and build coherent, accessible, responsive interfaces with complete interactions |
| [`yb-frontend-reviewer`](codex/skills/yb-frontend-reviewer/SKILL.md) | Review UI/UX, visual quality, accessibility, responsive behavior, and interactions |
| [`yb-code-design-reviewer`](codex/skills/yb-code-design-reviewer/SKILL.md) | Review clean code, contextual SOLID, maintainability, and architecture consistency |
| [`yb-code-correctness-reviewer`](codex/skills/yb-code-correctness-reviewer/SKILL.md) | Review correctness, algorithms, performance, concurrency, and data consistency |
| [`yb-qa-engineer`](codex/skills/yb-qa-engineer/SKILL.md) | Test requirements and user journeys; report acceptance evidence and gaps |
| [`yb-security-privacy`](codex/skills/yb-security-privacy/SKILL.md) | Trace security threats, authorization weaknesses, and privacy lifecycle risks |
| [`yb-release-operator`](codex/skills/yb-release-operator/SKILL.md) | Assess releases, execute authorized operations, and plan recovery and retirement |

Links above open the Codex edition. The [Claude Code edition](claude-code/skills) shares the same core instructions, with its own host guidance.

## Install

Clone and inspect the repository. The optional installer requires **Python 3.10 or later** and uses only the standard library. The installed skills themselves need no Python runtime, extra plugin, API key, or hook.

```sh
git clone https://github.com/yshbhrdwj/yb-engineering-skills.git
cd yb-engineering-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

On Windows, use `py -3` in place of `python3`. Choose `--target codex` or `--target claude-code` to install only one edition.

| Target | Personal skill location | Project skill location |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `<project>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |

For a project installation, add `--project /path/to/existing/project`. To install manually, copy complete `yb-*` folders from the relevant platform's `skills/` directory; retain references and Codex metadata. Compare existing copies before replacing them.

### Update

```sh
git pull --ff-only
python3 scripts/install.py --target both --update --dry-run
python3 scripts/install.py --target both --update
```

The installer refuses conflicting files unless `--update` is explicit. Updates back up affected skills under `.yb-engineering-skills-backups/` in the installation base, outside the discoverable skill folders. Identical files are left alone; unrelated skills and additional files are preserved. Inspect the reported backup location to restore a previous version.

Skills become available when the host refreshes discovery; start a new session if needed. See the [Codex guide](codex/README.md) and [Claude Code guide](claude-code/README.md) for host-specific usage. This targets local Codex and Claude Code skills; uploading an archive to an ordinary chat does not install them.

## Use

Codex:

```text
Use $yb-product-strategist to discuss my idea and create a brief for architecture and engineering.
Use $yb-frontend-engineer to design and implement this interface in the existing project.
Use $yb-code-correctness-reviewer to review this diff against its requirements. Do not edit code.
```

Claude Code:

```text
/yb-product-strategist Discuss my idea and create a brief for architecture and engineering.
/yb-frontend-engineer Design and implement this interface in the existing project.
/yb-code-correctness-reviewer Review this diff against its requirements. Do not edit code.
```

The skills also support automatic selection for matching requests. They respect host instructions, tools, planning modes, and permissions. Review roles remain read-only unless changes are requested; release planning does not itself authorize deployment.

## Workflow and evidence

Product brief → architecture → implementation → QA and focused reviews → release and operations → learning. Carry stable requirement IDs and artifact revisions between roles. Accepted intent, implemented behavior, verified behavior, and release authorization remain separate.

- [Start here](START-HERE.md) and [SDLC handoffs](SDLC-WORKFLOW.md)
- [Validation and its limits](VALIDATION.md)
- [Token-efficiency measurements](TOKEN-EFFICIENCY.md)
- [Ponytail scope comparison](PONYTAIL-COMPARISON.md)

The documented trials are small qualitative checks, not a guarantee of production quality or a benchmark of superiority. Text-size reductions are not measured runtime token savings. Browser and independent Claude Code runtime coverage remain limited as documented.

## Maintain and package

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Validation checks both platform editions, metadata, references, and shared-content consistency. Packaging creates platform ZIPs under `dist/`. CI runs validation, installer/validator tests, and packaging on Linux, macOS, and Windows.

See [contribution guidance](CONTRIBUTING.md) and [private security reporting](SECURITY.md). Changes to common skill instructions belong in both platform editions; CI catches drift.

## License

A license has not been selected yet. This repository currently includes no open-source license grant.
