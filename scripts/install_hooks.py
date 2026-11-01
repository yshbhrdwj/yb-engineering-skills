#!/usr/bin/env python3
"""Explicitly install optional Claude hooks; preserve unrelated settings and backups."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import ntpath
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

FILES = ("yb_merge_gate.py", "yb_stop_check.py")
LEGACY = ("yb-merge-gate.sh", "yb-stop-check.sh")


class InstallError(Exception):
    pass


def safe_path(value):
    path = Path(value).expanduser().absolute()
    if ".." in path.parts:
        raise InstallError("parent traversal is not allowed")
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError(f"symlinks are not allowed: {part}")
        if part != path and part.exists() and not part.is_dir():
            raise InstallError(f"expected a directory: {part}")
    return path


def command_for(path):
    args = [sys.executable, str(path)]
    return subprocess.list2cmdline(args) if os.name == "nt" else shlex.join(args)


def owned(command, folder, home, args=None):
    if not isinstance(command, str):
        return False
    scripts = {str(folder / name) for name in FILES}
    python_name = r"python(?:[0-9]+(?:\.[0-9]+)*)?(?:\.exe)?"
    if args is not None:
        return (isinstance(args, list) and len(args) == 1 and isinstance(args[0], str) and args[0] in scripts
                and re.fullmatch(python_name, ntpath.basename(command), re.I) is not None)
    candidates = {command_for(folder / name) for name in FILES}
    candidates.update(str(folder / name) for name in LEGACY)
    candidates.update(shlex.quote(str(folder / name)) for name in LEGACY)
    if folder == home / ".claude" / "hooks":
        candidates.update(f"$HOME/.claude/hooks/{name}" for name in LEGACY)
        candidates.update(f'"$HOME/.claude/hooks/{name}"' for name in LEGACY)
        candidates.update(f"~/.claude/hooks/{name}" for name in LEGACY)
    if command in candidates:
        return True
    # Existing settings can contain list2cmdline or POSIX shlex quoting, including
    # after an interpreter upgrade or a move between shell environments. Parse
    # both representations; never infer ownership from a path substring.
    for posix in (False, True):
        try:
            tokens = shlex.split(command, posix=posix)
        except ValueError:
            continue
        if len(tokens) != 2:
            continue
        interpreter, script = (
            token[1:-1] if len(token) >= 2 and token[0] in {"'", '"'} and token[-1] == token[0] else token
            for token in tokens
        )
        if (re.fullmatch(python_name, ntpath.basename(interpreter), re.I)
                and script in scripts):
            return True
    return False


def updated_settings(original, folder, home):
    result = json.loads(json.dumps(original))
    hooks = result.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise InstallError("settings hooks must be an object")
    for event in ("PreToolUse", "Stop"):
        groups = hooks.get(event, [])
        if not isinstance(groups, list):
            raise InstallError(f"{event} hooks must be a list")
        kept = []
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                raise InstallError(f"invalid {event} hook group")
            group = dict(group)
            group["hooks"] = [hook for hook in group["hooks"]
                              if not (isinstance(hook, dict) and hook.get("type") == "command"
                                      and owned(hook.get("command"), folder, home, hook.get("args")))]
            if group["hooks"]:
                kept.append(group)
        file = FILES[0] if event == "PreToolUse" else FILES[1]
        group = {"hooks": [{"type": "command", "command": sys.executable,
                             "args": [str(folder / file)], "onFailure": "block",
                             "timeout": 120 if event == "PreToolUse" else 330}]}
        if event == "PreToolUse":
            group["matcher"] = "Bash"
        kept.append(group)
        hooks[event] = kept
    return result


def read_object(path, default):
    if not path.exists():
        return default
    if not path.is_file():
        raise InstallError(f"expected a file: {path}")
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InstallError(f"invalid JSON: {path}") from exc
    if not isinstance(result, dict):
        raise InstallError(f"expected a JSON object: {path}")
    return result


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".yb-hooks-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def install(repo, base, home, *, reviewers=None, project_reviewers_only=False, update=False, dry_run=False):
    repo, base, home = safe_path(repo), safe_path(base), safe_path(home)
    if not base.is_dir():
        raise InstallError("the selected home/project must already exist")
    folder = safe_path(base / ".claude" / "hooks")
    settings_path = safe_path(base / ".claude" / "settings.json")
    config_path = safe_path(base / ".claude" / "yb-hooks.json")
    original = read_object(settings_path, {})
    config = read_object(config_path, {})
    if project_reviewers_only and reviewers is not None:
        raise InstallError("project-reviewers-only cannot install a global reviewer allowlist")
    if reviewers is not None:
        if not reviewers or any(not re.fullmatch(r"[A-Za-z0-9_-]+(?:\[bot\])?", x) for x in reviewers):
            raise InstallError("trusted reviewer logins must be exact GitHub account names")
        config["trusted_reviewers"] = list(dict.fromkeys(reviewers))
        config["project_reviewers_only"] = False
    if project_reviewers_only:
        config["project_reviewers_only"] = True
        config.pop("trusted_reviewers", None)
    elif not config.get("project_reviewers_only"):
        config.setdefault("trusted_reviewers", [])
    config.setdefault("check_timeout_seconds", 120)
    writes = {settings_path: encode(updated_settings(original, folder, home)), config_path: encode(config)}
    source_root = repo / "claude-code" / "hooks"
    if not source_root.is_dir():
        source_root = repo / "hooks"
    for name in FILES:
        source = safe_path(source_root / name)
        if not source.is_file():
            raise InstallError(f"missing hook source: {source}")
        writes[safe_path(folder / name)] = source.read_bytes()
    for path in writes:
        if path.exists() and not path.is_file():
            raise InstallError(f"expected a regular file: {path}")
    removals = [safe_path(folder / name) for name in LEGACY if (folder / name).exists() or (folder / name).is_symlink()]
    for path in removals:
        if not path.is_file():
            raise InstallError(f"expected a regular legacy hook: {path}")
    changed = {path: data for path, data in writes.items() if not path.exists() or path.read_bytes() != data}
    conflicts = [path for path in changed if path.exists()] + removals
    if conflicts and not update:
        raise InstallError("existing hook files/settings would change; rerun with --update to back them up first")
    backup = None
    if conflicts:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = safe_path(base / ".yb-engineering-skills-backups" / f"hooks-{stamp}")
    for path in changed:
        print(f"{'Would write' if dry_run else 'Write'}: {path}")
    for path in removals:
        print(f"{'Would retire' if dry_run else 'Retire'}: {path}")
    if backup:
        print(f"{'Would back up' if dry_run else 'Backups'}: {backup}")
    if dry_run:
        print("Dry run: no files written.")
        return
    if backup:
        backup.mkdir(parents=True, exist_ok=False)
        for path in conflicts:
            destination = backup / path.relative_to(base)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    for path, content in changed.items():
        atomic_write(path, content)
    for path in removals:
        path.unlink()
    print("Claude hooks installed. An empty trusted_reviewers list blocks merges until configured.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--user", action="store_true", help="install for your Claude user")
    target.add_argument("--project", type=Path, help="install in an existing project's .claude directory")
    parser.add_argument("--home", type=Path, help="override the home directory for --user (also useful for isolated tests)")
    parser.add_argument("--trusted-reviewer", action="append", dest="reviewers", help="exact account login; repeat for multiple trusted reviewers")
    parser.add_argument("--project-reviewers-only", action="store_true", help="user hook requires each repository to configure its own trusted reviewers")
    parser.add_argument("--update", action="store_true", help="back up and replace existing managed hook files/settings")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.home and not args.user:
        parser.error("--home requires --user")
    if args.project_reviewers_only and not args.user:
        parser.error("--project-reviewers-only requires --user")
    home = args.home or Path.home()
    try:
        install(Path(__file__).resolve().parents[1], args.project or home, home,
                reviewers=args.reviewers, project_reviewers_only=args.project_reviewers_only,
                update=args.update, dry_run=args.dry_run)
    except (InstallError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
