# Contributing

Keep each skill useful, focused, stack-agnostic, and concise. Improve decisions and observable behavior instead of adding generic checklists or promising expertise that instructions cannot prove.

## Make a change

1. Open an issue for a substantial scope change, or create a branch for a focused correction.
2. Edit the relevant skill under both `codex/skills/` and `claude-code/skills/`. Shared bodies and references must match; keep each platform's integration footer and Codex display metadata distinct.
3. Preserve stable requirement IDs, evidence boundaries, and existing user authorization. Avoid mandatory third-party tools, new approval gates, global style bans, or every-role workflows for small tasks.
4. Keep descriptions precise and within 200 characters. Put substantial conditional detail in linked references; do not load every reference by default.
5. Run the checks below. For changed decision-making instructions, try a realistic task with raw inputs and record the actual outcome, false positives, missed requirements, and limitations. Do not give the evaluator a desired answer.
6. Open a pull request explaining the problem, resulting behavior, and verification. Report unrun checks honestly. Do not include private prompts, personal paths, credentials, customer data, or local installation backups.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Python 3.10+ is sufficient; these scripts have no third-party dependencies. Tests use temporary directories and do not modify your real skill installation. The validator intentionally supports this repository's simple metadata format; it is not a general-purpose YAML implementation.

## Repository layout

- `codex/skills/`: Codex instructions, references, and display metadata.
- `claude-code/skills/`: Claude Code instructions and references.
- `scripts/`: installation, validation, and packaging helpers.
- `tests/`: checks of helper behavior and meaningful failure cases.
- Root guides: role selection, handoffs, evidence, and efficiency notes.

Do not commit generated `dist/` archives. Keep comparisons specific to reviewed versions and written scope; do not turn text counts or synthetic trials into unsupported quality or cost claims. Update documentation when a skill's scope or CLI changes.

## Review and maintenance

Main-branch changes should use pull requests with passing validation. Squash merges keep changes cohesive. Prefer small fixes supported by evidence; do not repeatedly run broad checks without a relevant change or unresolved concern.

Dependencies in GitHub Actions are pinned to commit hashes and reviewed through Dependabot updates. If a pinned action changes, verify its upstream release and review the permission/runtime impact. Workflow permissions should remain read-only unless a specific authorized publishing task requires more.

Treat other contributors respectfully. Discuss technical choices and evidence, avoid personal attacks, and use the private reporting path in [SECURITY.md](SECURITY.md) for sensitive issues.
