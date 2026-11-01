# Optional Claude Code hooks

These hooks are opt-in guardrails for Claude Code Bash merges and project checks. They do not install with the skills, do not run in Codex, and do not replace GitHub branch protection or repository rulesets. They never request reviews, post comments, or merge a PR themselves.

## Install or repair

Requires Python 3.10+, Git, and authenticated `gh` for merge checks. No `jq`, `bc`, or third-party Python package is needed. The installer uses exec-form `command` plus `args` with `onFailure: "block"`, so Python paths need no shell quoting and invocation failures block instead of silently bypassing the check. Choose a user installation or an existing project:

```sh
python3 scripts/install_hooks.py --user --trusted-reviewer 'your-reviewer-account' --dry-run
python3 scripts/install_hooks.py --user --trusted-reviewer 'your-reviewer-account' --update
# Or install only for one project:
python3 scripts/install_hooks.py --project /path/to/project --trusted-reviewer 'your-reviewer-account' --dry-run
```

For a user installation that must use each project’s configured reviewers only, use `--user --project-reviewers-only --update`. This stores `project_reviewers_only: true`, removes the global reviewer list, and requires every merging repository to provide its own `.claude/yb-hooks.json` with an explicit `trusted_reviewers` list. A project cannot disable the installed project-only policy. No project file is created by that option.

Repeat `--trusted-reviewer` for multiple exact GitHub logins when a global or project-specific list is intended. Choose the actual trusted human or bot account; a mention such as `@codex` is not an account login. An installation without reviewers is permitted and blocks merges until configured. `--update` backs up changed settings/configuration and managed hook files outside skill discovery. It retires the two legacy YB `.sh` hooks and their exact settings entries, preserving other hook entries and unrelated settings. `--dry-run` writes nothing. `--home /path` with `--user` supports isolated installation; the default is the current home.

Configuration is `.claude/yb-hooks.json` under the installation base:

```json
{
  "trusted_reviewers": ["your-reviewer-account"],
  "check_timeout_seconds": 120
}
```

A repository's `.claude/yb-hooks.json` takes precedence for merge trust. Review that configuration as code. Restart Claude Code after installation or use its hook settings UI to confirm the active commands. Project and user hooks can both run; prefer one scope for these hooks.

## Merge checks

The merge hook accepts one direct command with a PR number, HTTPS PR URL, or the current branch's PR:

```sh
gh pr merge 123 --repo OWNER/REPO --squash --match-head-commit FULL_REVIEWED_HEAD_SHA
```

Supported options are `--repo`/`-R` (including `[HOST/]OWNER/REPO`), one merge method, delete-branch, subject/body, and the full 40-character head pin. Values for subject/body are consumed as text, even when they resemble repository or method flags. Simple leading `GH_REPO` and `GH_HOST` assignments are resolved; explicit repository selection and URL conflicts are checked. The hook reads the exact host/repository/PR, requires an open, non-draft, mergeable PR, a trusted non-author `APPROVED` review on that head, no outstanding latest `CHANGES_REQUESTED` decision from any reviewer, and no unresolved review threads. A later comment does not clear a change request. Dismissed reviews, issue comments, and reactions never count as approval.

GitHub must report merge state `CLEAN` or `HAS_HOOKS`, as well as no merge conflicts. Required CI checks must pass or be skipped as accepted by GitHub. An explicit “no required checks reported” result is allowed only after that server merge-state check; missing checks can otherwise be absent from the CLI’s returned list. `BLOCKED`, `BEHIND`, `UNKNOWN`, `UNSTABLE`, and unrecognized states block. This deliberately conservative rule can also stop a PR because of optional failing checks or a merge queue; those workflows require their repository’s documented server-enforced process rather than an automatic exception in this guard. API errors, pending/failing checks, incomplete evidence, or more than 100 reviews/threads block the merge. The head is read again after checks, and `--match-head-commit` protects against a pushed commit between the hook and the merge.

Compound commands, shell wrappers, command substitutions, `--auto`, `--admin`, and unrecognized merge options stop with an instruction to use a supported direct command. Ordinary `echo`/commit-message prose mentioning the command is ignored. Literal bodies of quoted heredocs are ignored; unquoted or otherwise unsupported heredocs containing executable-looking merge commands may be conservatively rejected. Do not rewrite a rejected command to evade the guard.

This parser is deliberately finite. Aliases, arbitrary scripts, other executables, and direct API merges are outside its coverage. The hook matches the Bash tool; PowerShell tool calls are outside this parser, including on Windows hosts that use PowerShell as their primary shell. Review dismissal or CI changes can race the hook; only GitHub protection enforces those conditions at the server. Use required reviews/checks and stale-approval dismissal in branch protection for enforcement.

## Project checks on Stop

The Stop hook runs only when the repository opts in with a regular executable `.claude/yb-check.sh`. The script is trusted project code and runs from the repository root; inspect it before enabling. A POSIX shell environment is needed for this `.sh` convention. Example:

```sh
#!/bin/sh
set -eu
python3 scripts/validate.py
python3 -m unittest discover -s tests -q
```

Keep the script focused on checks appropriate for that project. The hook applies to every role in that repository, rather than inferring which skill ran. It fingerprints HEAD, index state, unstaged changes, untracked nonignored file contents, and the check script. A stable successful state runs once per Claude session; failures and checks that change files are never cached as success. Any dirty submodule disables caching, because Git’s superproject diff does not describe its changing file contents. Ignored dependency/build outputs are outside the fingerprint, so use a new session after changing the tool environment without changing tracked inputs.

Checks default to 120 seconds; `check_timeout_seconds` in the project's config may set 1–300 seconds. Timeout stops the check's process group on POSIX. A failed check blocks the first Stop with bounded diagnostic output. On the subsequent `stop_hook_active` turn the hook permits finishing, preventing an infinite loop; the agent must report any unresolved failure and must not claim validation passed. A missing executable check script means no project checks ran.

## Evidence and removal

Tests execute hook entrypoints against local Git fixtures and a stub `gh`; no real PR is merged. They cover review states, trust, exact-head matching, target selection, required checks, failures, Stop caching, recursion, and timeout. Installation tests use disposable homes/projects.

To disable, remove only the Python hook entries whose `args` point to `yb_merge_gate.py` and `yb_stop_check.py` from the selected `.claude/settings.json`. The backup contains previous settings and retired scripts; restoring the entire settings file also restores its other settings as of that backup, so compare before restoring.

Configuration and hook semantics checked on 1 November 2026 against the [Claude Code hooks reference](https://code.claude.com/docs/en/hooks), [GitHub CLI merge reference](https://cli.github.com/manual/gh_pr_merge), and [checks reference](https://cli.github.com/manual/gh_pr_checks). Local checks and hooks are evidence aids; approval and deployment authority still come from the user and repository policy.
