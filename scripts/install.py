#!/usr/bin/env python3
"""Install the repository's skills without modifying host configuration."""

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import sys
import tempfile


TARGETS = {"codex": ".agents", "claude-code": ".claude"}
SKILL_NAME = re.compile(r"yb-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
RETIRED_SKILLS = ("yb-code-correctness-reviewer", "yb-code-design-reviewer")


class InstallError(Exception):
    """A preflight condition prevents a safe installation."""


def safe_path(path):
    """Reject traversal and symlinks before resolving or creating any path."""
    path = Path(path).expanduser()
    if ".." in path.parts:
        raise InstallError(f"Parent traversal ('..') is not allowed: {path}")
    path = path.absolute()
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError(f"Symlinks are not allowed: {part}")
        if part != path and part.exists() and not part.is_dir():
            raise InstallError(f"Expected a directory: {part}")
    return path


def inspect_tree(root):
    """List regular files, rejecting links and special files, including extras."""
    root = safe_path(root)
    if not root.is_dir():
        raise InstallError(f"Expected a skill directory: {root}")
    files = []
    for child in sorted(root.iterdir()):
        safe_path(child)
        if child.is_dir():
            files.extend(inspect_tree(child))
        elif child.is_file():
            files.append(child)
        else:
            raise InstallError(f"Expected a regular file or directory: {child}")
    return files


@dataclass
class Plan:
    target: str
    source: Path
    destination: Path
    changed: list
    conflicts: list


def make_plans(repo, base, targets):
    plans = []
    for target in targets:
        source_root = safe_path(repo / target / "skills")
        destination_root = safe_path(base / TARGETS[target] / "skills")
        if not source_root.is_dir():
            raise InstallError(f"Source skills directory is missing: {source_root}")
        sources = sorted(source_root.iterdir())
        if not sources:
            raise InstallError(f"No source skills found: {source_root}")

        for source in sources:
            if not SKILL_NAME.fullmatch(source.name):
                raise InstallError(f"Invalid skill folder name: {source.name}")
            files = inspect_tree(source)
            if source / "SKILL.md" not in files:
                raise InstallError(f"Missing SKILL.md: {source}")
            destination = safe_path(destination_root / source.name)
            if destination.exists():
                inspect_tree(destination)

            changed, conflicts = [], []
            for file in files:
                relative = file.relative_to(source)
                installed = safe_path(destination / relative)
                if installed.exists() and not installed.is_file():
                    raise InstallError(f"File/directory conflict: {installed}")
                if not installed.exists() or file.read_bytes() != installed.read_bytes():
                    changed.append(relative)
                    if installed.exists():
                        conflicts.append(relative)
            plans.append(Plan(target, source, destination, changed, conflicts))
    return plans


def install(repo, base, targets, *, update=False, dry_run=False, migrate=False):
    repo, base = safe_path(repo), safe_path(base)
    if not base.is_dir():
        raise InstallError(f"Home or project directory must already exist: {base}")
    plans = make_plans(repo, base, targets)
    if migrate and not update:
        raise InstallError("--migrate requires --update so retired skills are backed up before removal")
    retired = []
    for target in targets:
        if not any(plan.target == target and plan.source.name == "yb-code-reviewer" for plan in plans):
            continue
        for name in RETIRED_SKILLS:
            path = safe_path(base / TARGETS[target] / "skills" / name)
            if path.exists():
                inspect_tree(path)
                retired.append((target, path))
    conflicts = [plan for plan in plans if plan.conflicts]
    if conflicts and not update:
        details = "\n".join(
            f"  {plan.destination / file}" for plan in conflicts for file in plan.conflicts
        )
        raise InstallError(f"Conflicting files; rerun with --update to back up and replace them:\n{details}")

    backup_root = None
    if conflicts or (migrate and retired):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup_root = safe_path(base / ".yb-engineering-skills-backups" / stamp)
        if backup_root.exists():
            raise InstallError(f"Backup path already exists: {backup_root}")

    for plan in plans:
        action = "unchanged" if not plan.changed else "update" if plan.conflicts else "install"
        prefix = "Would " if dry_run else "Plan: "
        print(f"{prefix}{action}: {plan.destination} ({len(plan.changed)} files)")
    for _, path in retired:
        if migrate:
            print(f"{'Would' if dry_run else 'Plan:'} back up and retire: {path}")
        else:
            print(f"Retired skill still installed: {path}. Use --update --migrate to back up and retire it.")
    if dry_run:
        if backup_root:
            print(f"Would back up conflicting skills under: {backup_root}")
        print("Dry run: no files written.")
        return

    # Finish every backup before overwriting any installed file.
    if backup_root:
        backup_root.mkdir(parents=True, exist_ok=False)
        for plan in conflicts:
            inspect_tree(plan.destination)
            backup = backup_root / plan.target / plan.source.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(plan.destination, backup)
        if migrate:
            for target, path in retired:
                backup = backup_root / target / path.name
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(path, backup)
        print(f"Backups: {backup_root}")

    for plan in plans:
        for relative in plan.changed:
            source = safe_path(plan.source / relative)
            destination = safe_path(plan.destination / relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Replace each file atomically, leaving any other hard links untouched.
            with tempfile.NamedTemporaryFile(prefix=".yb-install-", dir=destination.parent,
                                             delete=False) as staged:
                temporary = Path(staged.name)
            try:
                shutil.copy2(source, temporary)
                temporary.replace(destination)
            finally:
                if temporary.exists():
                    temporary.unlink()
    if migrate:
        for _, path in retired:
            inspect_tree(path)
            shutil.rmtree(path)
    print("Installation complete. Unrelated skills and extra files were preserved.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=(*TARGETS, "both"),
                        help="Which platform's skills to install")
    parser.add_argument("--project", type=Path,
                        help="Use an existing project directory instead of your home")
    parser.add_argument("--update", action="store_true",
                        help="Back up conflicting skills outside the skills roots, then replace conflicting files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preflight and show changes without writing files")
    parser.add_argument("--migrate", action="store_true",
                        help="With --update, back up and retire the two superseded code reviewer skills")
    args = parser.parse_args(argv)
    targets = tuple(TARGETS) if args.target == "both" else (args.target,)
    try:
        install(Path(__file__).absolute().parent.parent, args.project or Path.home(),
                targets, update=args.update, dry_run=args.dry_run, migrate=args.migrate)
    except (InstallError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
