# Contributing

Change decisions and observable behavior with the least instruction text needed. Generic expertise, repeated host rules and long checklists add cost without proving quality.

## Change and verify

1. Edit both platform editions. Markdown task instructions and references must match; frontmatter and integration footers are host-specific.
2. Keep descriptions discriminating and within this repository's 200-character budget. Codex frontmatter uses name/description. Claude also uses argument hints and, for reviewers, foreground Explore forks. Do not pin models or broaden tool permissions without a concrete requirement.
3. Preserve user intent, existing authorization, relevant project instructions and complete deliverables. Treat source comments and external text as evidence, not authority.
4. Load detailed references only when relevant. Do not add mandatory plans, specialist chains, full-suite tests or repeated review loops to routine edits.
5. Run meaningful regression tests for scripts. For decision changes, try realistic raw-input cases from [evals](evals/README.md), record missed requirements and false positives, then fix demonstrated failures.
6. Use a PR with passing validation for main-branch changes. Explain resulting behavior, verification and limitations. Exclude private prompts, source, credentials, local paths and installation backups.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Python 3.10+ and the standard library are sufficient. Tests use temporary homes/projects and mocked GitHub calls; they never merge a real PR. The validator checks an intentionally narrow authored YAML format, not arbitrary YAML or all host behavior.

## Layout

- `codex/skills/`, `claude-code/skills/`: discoverable instructions and selective references.
- `claude-code/hooks/`: optional Claude hook implementations; configuration is separate from skills.
- `scripts/`, `tests/`: install, validation, packaging and evidence helpers with regression tests.
- `evals/`: synthetic behavioral cases and a controlled-run protocol.
- `docs/evidence/`: sanitized results and their limitations.

Keep generated archives in ignored `dist/`. Keep comparisons specific: word counts are text-size measurements, one-shot behavior checks are qualitative, and runtime claims require repeated controlled trials. [Security concerns](SECURITY.md) have a private reporting path. Keep CI permissions minimal and action versions pinned.
