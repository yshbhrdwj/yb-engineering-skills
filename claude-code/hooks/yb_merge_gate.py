#!/usr/bin/env python3
"""Claude PreToolUse guard for supported direct gh pr merge commands (read-only)."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
from urllib.parse import urlsplit

TIMEOUT = 15
SHA = re.compile(r"[0-9a-fA-F]{40}")
REPOSITORY = re.compile(r"(?:(?P<host>[a-zA-Z0-9.-]+)/)?(?P<owner>[A-Za-z0-9_.-]+)/(?P<name>[A-Za-z0-9_.-]+)")
QUERY = """query($owner:String!,$name:String!,$number:Int!) {
 repository(owner:$owner,name:$name) { pullRequest(number:$number) {
 number state isDraft headRefOid mergeable mergeStateStatus author { login }
 reviews(first:100) { pageInfo { hasNextPage } nodes { state submittedAt author { login } commit { oid } } }
 reviewThreads(first:100) { pageInfo { hasNextPage } nodes { isResolved } }
 } }
}"""


class Block(Exception):
    pass


def command_tokens(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    return list(lexer)


def gh_merge(tokens):
    """Find merge only in command position, including common wrappers."""
    remaining = list(tokens)
    while remaining and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*=.*", remaining[0]):
        remaining.pop(0)
    if not remaining:
        return False
    executable = Path(remaining[0]).name
    if executable in {"bash", "sh", "zsh", "dash", "fish"}:
        for flag in ("-c", "-lc", "-ic"):
            if flag in remaining and remaining.index(flag) + 1 < len(remaining):
                return contains_merge(command_tokens(remaining[remaining.index(flag) + 1]))
        return False
    if executable in {"command", "exec", "sudo", "env", "nohup", "time"}:
        return any(gh_merge(remaining[i:]) for i in range(1, len(remaining)) if Path(remaining[i]).name == "gh")
    if executable != "gh":
        return False
    i = 1
    while i < len(remaining):
        if remaining[i] in {"-R", "--repo"}:
            i += 2
        elif remaining[i].startswith("--repo="):
            i += 1
        else:
            break
    if i < len(remaining) and remaining[i] == "pr":
        j = i + 1
        while j < len(remaining):
            if remaining[j] in {"-R", "--repo"}:
                j += 2
            elif remaining[j].startswith("--repo="):
                j += 1
            else:
                if remaining[j] == "merge":
                    return True
                break
    return any(remaining[j:j + 2] == ["pr", "merge"] for j in range(i, len(remaining)))


def contains_merge(tokens):
    segment = []
    for token in tokens + [";"]:
        if token and all(c in ";&|()<>\n" for c in token):
            if gh_merge(segment):
                return True
            segment = []
        else:
            segment.append(token)
    return False


def strip_quoted_heredocs(command):
    """Omit literal quoted heredoc bodies; leave unsupported forms conservative."""
    lines = command.splitlines(keepends=True)
    output, delimiters = [], []
    for line in lines:
        if delimiters:
            if line.rstrip("\r\n") == delimiters[0]:
                delimiters.pop(0)
            output.append("\n" if line.endswith("\n") else "")
            continue
        output.append(line)
        try:
            lexer = shlex.shlex(line, posix=False, punctuation_chars=";&|()<>")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            continue
        pending = []
        for index, token in enumerate(tokens[:-1]):
            if token == "<<":
                delimiter = tokens[index + 1]
                if len(delimiter) >= 3 and delimiter[0] in {"'", '"'} and delimiter[-1] == delimiter[0]:
                    pending.append(delimiter[1:-1])
                else:
                    pending = []
                    break
        delimiters = pending
    return "".join(output)


def substitution_contains_merge(command):
    """Find literal merge invocations in expanding substitutions, not single quotes."""
    quote, index = None, 0
    while index < len(command):
        char = command[index]
        if quote == "'":
            if char == "'":
                quote = None
            index += 1
            continue
        if char == "\\":
            index += 2
            continue
        if char == "'" and quote is None:
            quote = "'"
            index += 1
            continue
        if char == '"':
            quote = None if quote == '"' else '"'
            index += 1
            continue
        if char == "`":
            end = index + 1
            while end < len(command):
                if command[end] == "\\":
                    end += 2
                elif command[end] == "`":
                    break
                else:
                    end += 1
            inner = command[index + 1:end]
            try:
                if contains_merge(command_tokens(inner)) or substitution_contains_merge(inner):
                    return True
            except ValueError:
                if re.search(r"\bgh\b.*\bpr\s+merge\b", inner):
                    return True
            index = end + 1
            continue
        if command.startswith("$(", index):
            end, depth = index + 2, 1
            while end < len(command) and depth:
                if command[end] == "\\":
                    end += 2
                    continue
                depth += (command[end] == "(") - (command[end] == ")")
                end += 1
            inner = command[index + 2:end - 1 if depth == 0 else end]
            try:
                if contains_merge(command_tokens(inner)) or substitution_contains_merge(inner):
                    return True
            except ValueError:
                if re.search(r"\bgh\b.*\bpr\s+merge\b", inner):
                    return True
            index = end
            continue
        index += 1
    return False


def parse_command(command, environment):
    command = strip_quoted_heredocs(command)
    if substitution_contains_merge(command):
        raise Block("merge commands in substitutions are unsupported; use one direct gh pr merge command")
    try:
        tokens = command_tokens(command.strip())
    except ValueError:
        if re.search(r"\bgh\b.*\bpr\s+merge\b", command):
            raise Block("cannot parse the merge command; use one direct gh pr merge command")
        return None
    if not contains_merge(tokens):
        return None
    if any(t and all(c in ";&|()<>\n" for c in t) for t in tokens):
        raise Block("compound/wrapped merge commands are unsupported; use one direct gh pr merge command")
    env = environment.copy()
    while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*=.*", tokens[0]):
        key, value = tokens.pop(0).split("=", 1)
        if key not in {"GH_REPO", "GH_HOST"}:
            raise Block("only GH_REPO/GH_HOST assignments are supported before a direct merge")
        env[key] = value
    if not tokens or tokens[0] != "gh":
        raise Block("wrapped/absolute-path merges are unsupported; use one direct gh pr merge command")
    repo = None

    def repository_option(index):
        nonlocal repo
        token = tokens[index]
        if token in {"-R", "--repo"}:
            if index + 1 >= len(tokens):
                raise Block(f"{token} needs a repository value")
            value, following = tokens[index + 1], index + 2
        elif token.startswith("--repo="):
            value, following = token.split("=", 1)[1], index + 1
        else:
            return None
        if repo is not None or not value:
            raise Block("provide exactly one repository value")
        repo = value
        return following

    # Parse in command order: a value belonging to --body/--subject is never a flag.
    i = 1
    for command_word in ("pr", "merge"):
        while i < len(tokens) and tokens[i] != command_word:
            following = repository_option(i)
            if following is None:
                raise Block(f"unsupported global command option {tokens[i]}; use direct gh pr merge")
            i = following
        if i >= len(tokens):
            raise Block("use a direct gh pr merge command")
        i += 1
    target, pin, method = None, None, None
    methods = {"--squash": "squash", "-s": "squash", "--merge": "merge", "-m": "merge", "--rebase": "rebase", "-r": "rebase"}
    values = {"--match-head-commit", "--body", "--subject", "-b", "-t"}
    while i < len(tokens):
        token = tokens[i]
        following = repository_option(i)
        if following is not None:
            i = following
        elif token in methods:
            if method is not None:
                raise Block("provide exactly one merge method")
            method = methods[token]
            i += 1
        elif token in {"--delete-branch", "-d"}:
            i += 1
        elif token in values or any(token.startswith(flag + "=") for flag in values if flag.startswith("--")):
            if "=" in token:
                flag, value = token.split("=", 1)
                i += 1
            else:
                flag = token
                if i + 1 >= len(tokens):
                    raise Block(f"{flag} needs a value")
                value = tokens[i + 1]
                i += 2
            if flag == "--match-head-commit":
                if pin is not None:
                    raise Block("provide the head pin only once")
                pin = value
        elif token.startswith("-"):
            raise Block(f"unsupported merge option {token}; auto/admin merges are not guarded")
        elif target is None:
            target = token
            i += 1
        else:
            raise Block("use a PR number or URL and supported merge options")
    if not pin or not SHA.fullmatch(pin):
        raise Block("pass --match-head-commit with the full reviewed head SHA")
    return target, repo, pin.lower(), env


def run_gh(args, cwd, env, *, allow_no_checks=False):
    try:
        result = subprocess.run(["gh", *args], cwd=cwd, env=env, text=True,
                                capture_output=True, timeout=TIMEOUT, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Block(f"could not obtain GitHub evidence ({type(exc).__name__})") from exc
    if result.returncode:
        if allow_no_checks and result.returncode == 1 and re.search(
                r"^no required checks reported(?: on .*)?\s*$", result.stderr.strip(), re.I):
            return []
        raise Block("GitHub evidence lookup failed; check gh authentication, target and network")
    try:
        return json.loads(result.stdout)
    except (ValueError, TypeError) as exc:
        raise Block("GitHub returned incomplete or invalid evidence") from exc


def repo_parts(value, default_host):
    match = REPOSITORY.fullmatch(value or "")
    if not match:
        raise Block("repository must be [HOST/]OWNER/REPO")
    return match.group("host") or default_host, match.group("owner"), match.group("name")


def target_parts(target):
    if target is None or re.fullmatch(r"[1-9][0-9]*", target):
        return None
    parsed = urlsplit(target)
    match = re.fullmatch(r"/([^/]+)/([^/]+)/pull/([1-9][0-9]*)/?", parsed.path)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment or not match:
        raise Block("target must be a positive PR number or HTTPS pull request URL")
    owner, name, number = match.groups()
    return (parsed.hostname, owner, name), int(number)


def config_for(cwd):
    installed = Path(__file__).resolve().parents[1] / "yb-hooks.json"
    try:
        policy = json.loads(installed.read_text(encoding="utf-8")) if installed.is_file() else {}
        if not isinstance(policy, dict) or not isinstance(policy.get("project_reviewers_only", False), bool):
            raise Block("invalid installed hook policy")
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd,
                                capture_output=True, text=True, timeout=5, check=False)
        project = Path(result.stdout.strip()) / ".claude" / "yb-hooks.json"
        has_project = result.returncode == 0 and project.is_file()
        if policy.get("project_reviewers_only") and not has_project:
            raise Block("this installation uses project reviewers only; configure trusted_reviewers in the repository's .claude/yb-hooks.json")
        config = json.loads(project.read_text(encoding="utf-8")) if has_project else policy
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        raise Block("configure trusted_reviewers in .claude/yb-hooks.json before merging") from exc
    if not isinstance(config, dict):
        raise Block("hook configuration must be a JSON object")
    reviewers = config.get("trusted_reviewers")
    if not isinstance(reviewers, list) or not reviewers or any(not isinstance(x, str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:\[bot\])?", x) for x in reviewers):
        raise Block("trusted_reviewers must list exact approved GitHub account logins")
    return {x.casefold() for x in reviewers}


def validate_evidence(pr, trusted, expected_head):
    if not isinstance(pr, dict) or pr.get("state") != "OPEN" or pr.get("isDraft") is not False:
        raise Block("the PR must be open and ready for review")
    head = pr.get("headRefOid", "").lower()
    if head != expected_head:
        raise Block("the requested head pin is stale; review the current head before merging")
    if pr.get("mergeable") != "MERGEABLE":
        raise Block("GitHub has not confirmed this PR is mergeable")
    if pr.get("mergeStateStatus") not in {"CLEAN", "HAS_HOOKS"}:
        raise Block("GitHub reports blocked, incomplete or nonpassing merge conditions")
    latest = {}
    for group in ("reviews", "reviewThreads"):
        data = pr.get(group)
        if not isinstance(data, dict) or data.get("pageInfo", {}).get("hasNextPage") is not False or not isinstance(data.get("nodes"), list):
            raise Block("review evidence is incomplete or exceeds the 100-item guard limit")
    if any(thread.get("isResolved") is not True for thread in pr["reviewThreads"]["nodes"]):
        raise Block("resolve and answer every review thread before merging")
    for review in sorted(pr["reviews"]["nodes"], key=lambda x: x.get("submittedAt") or ""):
        login = (review.get("author") or {}).get("login", "").casefold()
        state = review.get("state")
        if state in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}:
            if not login:
                raise Block("a decisive review has no identifiable author")
            latest[login] = review
    if any(x.get("state") == "CHANGES_REQUESTED" for x in latest.values()):
        raise Block("a reviewer still requests changes")
    author = (pr.get("author") or {}).get("login", "").casefold()
    if not author:
        raise Block("the PR author identity is unavailable")
    if not any(login in trusted and login != author and review.get("state") == "APPROVED"
               and (review.get("commit") or {}).get("oid", "").lower() == head
               for login, review in latest.items()):
        raise Block("no trusted non-author APPROVED review exists for the exact current head")


def gate(payload, environment=None):
    command = payload.get("tool_input", {}).get("command", "")
    if not isinstance(command, str):
        raise Block("invalid Bash hook input")
    parsed = parse_command(command, environment or os.environ)
    if parsed is None:
        return
    target, explicit_repo, pin, env = parsed
    cwd = payload.get("cwd")
    if not cwd or not Path(cwd).is_dir():
        raise Block("a valid working directory is required")
    trusted = config_for(cwd)
    default_host = env.get("GH_HOST", "github.com")
    if not re.fullmatch(r"[A-Za-z0-9.-]+", default_host):
        raise Block("GH_HOST must be a hostname")
    url_target = target_parts(target)
    configured_repo = explicit_repo or env.get("GH_REPO")
    repository = repo_parts(configured_repo, default_host) if configured_repo else None
    if url_target:
        url_repo, number = url_target
        if explicit_repo and repository != url_repo:
            raise Block("PR URL and explicit repository disagree")
        repository = url_repo
    else:
        if repository is None:
            current = run_gh(["repo", "view", "--json", "nameWithOwner,url"], cwd, env)
            repository = repo_parts(current.get("nameWithOwner"), urlsplit(current.get("url", "")).hostname or default_host)
        number = int(target) if target and re.fullmatch(r"[1-9][0-9]*", target) else None
    host, owner, name = repository
    full_repo = f"{host}/{owner}/{name}"
    if number is None:
        view = run_gh(["pr", "view", "--repo", full_repo, "--json", "number"], cwd, env)
        number = view.get("number")
    if not isinstance(number, int) or number <= 0:
        raise Block("a positive pull request number is required")
    response = run_gh(["api", "graphql", "--hostname", host, "-f", f"query={QUERY}",
                       "-F", f"owner={owner}", "-F", f"name={name}", "-F", f"number={number}"], cwd, env)
    if response.get("errors"):
        raise Block("GitHub returned partial review evidence")
    pr = (response.get("data", {}).get("repository") or {}).get("pullRequest")
    if not isinstance(pr, dict) or pr.get("number") != number:
        raise Block("GitHub returned a different or missing PR")
    validate_evidence(pr, trusted, pin)
    checks = run_gh(["pr", "checks", str(number), "--repo", full_repo, "--required", "--json", "name,state,bucket"], cwd, env, allow_no_checks=True)
    if not isinstance(checks, list) or any(x.get("bucket") not in {"pass", "skipping"} for x in checks):
        raise Block("required CI checks must pass before merging")
    fresh = run_gh(["pr", "view", str(number), "--repo", full_repo, "--json", "headRefOid"], cwd, env)
    if fresh.get("headRefOid", "").lower() != pin:
        raise Block("the head changed during verification; review the new head")


def main():
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise Block("invalid hook input")
        gate(payload)
    except (Block, ValueError, TypeError, AttributeError) as exc:
        print(f"yb-merge-gate: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
