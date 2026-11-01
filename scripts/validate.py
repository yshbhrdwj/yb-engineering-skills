#!/usr/bin/env python3
"""Validate this repository's authored skill format using only the standard library.

This is deliberately not a general YAML or CommonMark parser. Frontmatter uses
flat plain/JSON-quoted strings and explicitly typed Claude fields; openai.yaml uses one interface mapping with three
JSON-quoted strings. Markdown checks cover inline/reference links and ordinary
GitHub heading anchors, ignoring fenced and inline code. Remote URLs are not fetched.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


EXPECTED_NAMES = frozenset({
    "yb-code-reviewer", "yb-merge-pr",
    "yb-frontend-engineer", "yb-frontend-reviewer", "yb-mobile-design-system",
    "yb-product-strategist",
    "yb-qa-engineer", "yb-release-operator", "yb-security-privacy",
    "yb-software-engineer", "yb-solution-architect", "yb-web-design-system",
})
REVIEWERS = {"yb-code-reviewer", "yb-frontend-reviewer", "yb-security-privacy"}
REVIEWER_AGENTS = {name: "general-purpose" if name == "yb-frontend-reviewer" else "Explore"
                   for name in REVIEWERS}
CLAUDE_FIELDS = {"argument-hint", "context", "agent", "background"}
FOOTERS = {
    "codex": (
        "## Codex integration\n\n"
        "Follow applicable `AGENTS.md`, task mode, permissions, and requested output "
        "format. Use available tools; delegate bounded independent work only when "
        "useful. Load each applicable named skill; for delegated work, pass the "
        "relevant skill path or instructions with the requirements and raw artifacts. "
        "The skill does not change host configuration."
    ),
    "claude-code": (
        "## Claude Code integration\n\n"
        "Follow applicable `CLAUDE.md`, the active planning mode, and permissions. "
        "Use available tools; delegate bounded independent work only when useful. "
        "Load each applicable named skill; for delegated work, pass the relevant "
        "skill path or instructions with the requirements and raw artifacts. "
        "The skill does not change host configuration."
    ),
}
SKIP_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__"}
INLINE_LINK = re.compile(
    r"!?\[(?:\\.|[^\]\\\n])*\]\(\s*"
    r"(?P<target><[^>\n]*>|(?:\\.|[^\s()\\]|\([^()\n]*\))*)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\n)]*\)))?\s*\)"
)
REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[([^\]\n]+)\]:\s*(<[^>\n]*>|\S+)", re.MULTILINE
)
REFERENCE_USE = re.compile(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]")


def without_fences(text: str) -> str:
    """Blank fenced-code contents, preserving line numbers for diagnostics."""
    output = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and marker:
            fence = marker.group(1)
            output.append("\n" if line.endswith("\n") else "")
        elif fence is not None:
            if re.match(r"^ {0,3}" + re.escape(fence[0]) +
                        "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    return "".join(output)


def markdown_anchors(text: str) -> set[str]:
    """Resolve ordinary authored headings, duplicate headings, and explicit IDs."""
    text = without_fences(text)
    anchors = set(re.findall(r"\b(?:id|name)=[\"']([^\"']+)[\"']", text))
    used = set()
    lines = text.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        title = heading.group(1) if heading else None
        if title is None and index + 1 < len(lines) and line.strip():
            if re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
                title = line.strip()
        if title is None:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]+>", "", title).lower()
        # GitHub retains letters/numbers/underscores/hyphens and replaces spaces.
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        anchor, suffix = slug, 0
        while anchor in used:
            suffix += 1
            anchor = f"{slug}-{suffix}"
        used.add(anchor)
        anchors.add(anchor)
    return anchors


class Validator:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.errors: list[str] = []
        self.texts: dict[Path, str] = {}

    def error(self, path: Path, message: str) -> None:
        try:
            location = path.relative_to(self.root).as_posix()
        except ValueError:
            location = str(path)
        self.errors.append(f"{location}: {message}")

    def read_text(self, path: Path) -> str | None:
        if path in self.texts:
            return self.texts[path]
        if path.is_symlink():
            self.error(path, "symlinks are not allowed; use a regular authored file")
            return None
        if not path.is_file():
            self.error(path, "required regular file is missing")
            return None
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            self.error(path, f"cannot read UTF-8 text ({exc})")
            return None
        if any(ord(char) < 32 and char not in "\t\r\n" for char in text):
            self.error(path, "binary/control-byte payload is not allowed")
            return None
        self.texts[path] = text
        return text

    def skill_files(self, folder: Path, platform: str) -> dict[str, str]:
        """Read authored files without following links or permitting payloads."""
        files = {}
        for current, directories, filenames in os.walk(folder, followlinks=False):
            current_path = Path(current)
            for name in list(directories):
                path = current_path / name
                relative = path.relative_to(folder)
                allowed = relative.parts[0] == "references" or (
                    platform == "codex" and relative.parts == ("agents",)
                )
                if path.is_symlink():
                    self.error(path, "symlink directories are not allowed")
                    directories.remove(name)
                elif not allowed:
                    self.error(path, "unexpected skill directory; expected references/ or Codex agents/")
                    directories.remove(name)
            for name in filenames:
                path = current_path / name
                relative = path.relative_to(folder).as_posix()
                allowed = relative == "SKILL.md" or (
                    relative.startswith("references/") and path.suffix == ".md"
                ) or (platform == "codex" and relative == "agents/openai.yaml")
                if path.is_symlink():
                    self.error(path, "symlinks are not allowed")
                elif not allowed:
                    self.error(path, "unexpected skill payload; only SKILL.md, Markdown references, and Codex agents/openai.yaml are supported")
                else:
                    text = self.read_text(path)
                    if text is not None:
                        files[relative] = text
        return files

    def frontmatter(self, path: Path, text: str, name: str, platform: str) -> None:
        lines = text.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            self.error(path, "expected opening/closing --- frontmatter delimiters")
            return
        end = lines.index("---", 1)
        fields = {}
        for number, line in enumerate(lines[1:end], 2):
            match = re.fullmatch(r"([a-z][a-z_-]*): (.+)", line)
            if not match:
                self.error(path, f"line {number}: expected a flat key: string frontmatter field")
                continue
            key, value = match.groups()
            if key in fields:
                self.error(path, f"line {number}: duplicate frontmatter field {key!r}")
            if platform == "claude-code" and key == "background":
                if value not in {"true", "false"}:
                    self.error(path, f"line {number}: background must be an unquoted boolean")
                else:
                    fields[key] = value == "true"
                continue
            if value.startswith('"'):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    self.error(path, f"line {number}: malformed JSON-quoted string for {key}")
                    continue
            elif value.startswith(("'", "|", ">", "[", "{", "&", "*", "!")):
                self.error(path, f"line {number}: use a plain or JSON-quoted single-line string")
                continue
            elif (re.search(r":(?:\s|$)|(?:^|\s)#", value)
                  or value.lower() in {"null", "~", "true", "false", "yes", "no", "on", "off"}
                  or re.fullmatch(r"[-+]?(?:\d[\d_.eE+-]*|\.(?:inf|nan))", value, re.IGNORECASE)):
                self.error(path, f"line {number}: quote this ambiguous YAML scalar as a JSON string")
                continue
            if not isinstance(value, str) or not value.strip() or any(ord(char) < 32 for char in value):
                self.error(path, f"line {number}: {key} must be a nonempty single-line string")
                continue
            fields[key] = value
        required = {"name", "description"}
        allowed = required | (CLAUDE_FIELDS if platform == "claude-code" else set())
        if not required <= fields.keys() or fields.keys() - allowed:
            self.error(path, f"frontmatter requires name and description; allowed {platform} fields: {', '.join(sorted(allowed))}")
        if platform == "claude-code":
            if name in REVIEWERS:
                if any(fields.get(key) != value for key, value in
                       {"context": "fork", "agent": REVIEWER_AGENTS[name], "background": False}.items()):
                    self.error(path, f"reviewers require context: fork, agent: {REVIEWER_AGENTS[name]}, background: false")
            elif fields.keys() & {"context", "agent", "background"}:
                self.error(path, "forked reviewer fields belong only on reviewer skills")
        if fields.get("name") != name or not re.fullmatch(r"yb-[a-z0-9]+(?:-[a-z0-9]+)*", fields.get("name", "")):
            self.error(path, f"frontmatter name must match the skill directory: {name}")
        if len(fields.get("description", "")) > 200:
            self.error(path, "description exceeds the 200-character portable limit")
        if not "\n".join(lines[end + 1:]).strip():
            self.error(path, "skill instructions are empty")

    def shared_core(self, path: Path, text: str, platform: str) -> str | None:
        footer = FOOTERS[platform]
        heading = footer.splitlines()[0]
        if text.count(heading) != 1 or not text.rstrip().endswith("\n\n" + footer):
            self.error(path, f"expected exactly one complete {heading[3:]} footer at the end")
            return None
        # Runtime frontmatter is deliberately host-specific; compare the actual
        # instructions, not Claude's fork/argument configuration with Codex's.
        lines = text.splitlines()
        if not lines or lines[0] != "---" or "---" not in lines[1:]:
            return None
        body = "\n".join(lines[lines.index("---", 1) + 1:]).strip()
        core = body[:-len(footer)].rstrip()
        for other, value in FOOTERS.items():
            if other != platform and value.splitlines()[0] in core:
                self.error(path, f"contains the wrong platform's {other} integration section")
        return core

    def metadata(self, path: Path, text: str, name: str) -> None:
        lines = text.splitlines()
        if not lines or lines[0] != "interface:":
            self.error(path, "expected one interface: mapping with JSON-quoted string fields")
            return
        fields = {}
        required = {"display_name", "short_description", "default_prompt"}
        for number, line in enumerate(lines[1:], 2):
            if not line.strip():
                continue
            match = re.fullmatch(r"  ([a-z_]+): (\".*\")", line)
            if not match:
                self.error(path, f"line {number}: expected two-space indentation and a JSON-quoted string")
                continue
            key, encoded = match.groups()
            if key in fields:
                self.error(path, f"line {number}: duplicate interface field {key!r}")
            try:
                value = json.loads(encoded)
            except json.JSONDecodeError:
                self.error(path, f"line {number}: invalid JSON-quoted value for {key}")
                continue
            if not isinstance(value, str) or not value.strip() or any(ord(char) < 32 for char in value):
                self.error(path, f"line {number}: {key} must be a nonempty single-line string")
                continue
            fields[key] = value
        if set(fields) != required:
            self.error(path, "interface must contain exactly display_name, short_description, and default_prompt")
        if "short_description" in fields and not 25 <= len(fields["short_description"]) <= 64:
            self.error(path, "short_description must be 25–64 characters")
        if "default_prompt" in fields and not re.search(r"\$" + re.escape(name) + r"(?![\w-])", fields["default_prompt"]):
            self.error(path, f"default_prompt must explicitly invoke ${name}")

    def check_skills(self) -> None:
        packages = {}
        cores = {}
        for platform in FOOTERS:
            if (self.root / platform).is_symlink():
                self.error(self.root / platform, "platform directory must not be a symlink")
                continue
            root = self.root / platform / "skills"
            if root.is_symlink() or not root.is_dir():
                self.error(root, f"expected a regular directory containing the {len(EXPECTED_NAMES)} skills")
                continue
            entries = {path.name: path for path in root.iterdir()}
            for name in sorted(EXPECTED_NAMES - entries.keys()):
                self.error(root / name, "missing expected skill directory")
            for name in sorted(entries.keys() - EXPECTED_NAMES):
                self.error(entries[name], f"unexpected entry; this package must contain exactly the {len(EXPECTED_NAMES)} YB skills")
            for name in sorted(EXPECTED_NAMES & entries.keys()):
                folder = entries[name]
                if folder.is_symlink() or not folder.is_dir():
                    self.error(folder, "skill must be a regular directory, not a symlink or file")
                    continue
                files = self.skill_files(folder, platform)
                packages[platform, name] = files
                if "SKILL.md" not in files:
                    self.error(folder / "SKILL.md", "missing readable skill entrypoint")
                else:
                    self.frontmatter(folder / "SKILL.md", files["SKILL.md"], name, platform)
                    cores[platform, name] = self.shared_core(folder / "SKILL.md", files["SKILL.md"], platform)
                if platform == "codex":
                    if "agents/openai.yaml" not in files:
                        self.error(folder / "agents/openai.yaml", "missing readable Codex display metadata")
                    else:
                        self.metadata(folder / "agents/openai.yaml", files["agents/openai.yaml"], name)
        for name in sorted(EXPECTED_NAMES):
            left, right = ("codex", name), ("claude-code", name)
            if left not in packages or right not in packages:
                continue
            if cores.get(left) is not None and cores.get(right) is not None and cores[left] != cores[right]:
                self.error(self.root / "claude-code/skills" / name / "SKILL.md", "shared core differs from Codex; synchronize content before platform footers")
            # Description is discovery guidance and must also agree, even though
            # other frontmatter differs between hosts.
            def description(files):
                return next((line for line in files.get("SKILL.md", "").splitlines()
                             if line.startswith("description: ")), None)
            if description(packages[left]) != description(packages[right]):
                self.error(self.root / "claude-code/skills" / name / "SKILL.md", "description differs from Codex")
            a = {k: v for k, v in packages[left].items() if k.startswith("references/")}
            b = {k: v for k, v in packages[right].items() if k.startswith("references/")}
            for relative in sorted(a.keys() | b.keys()):
                if a.get(relative) != b.get(relative):
                    self.error(self.root / "claude-code/skills" / name / relative, "reference differs or is missing between platforms")

    def check_link(self, source: Path, target: str, line: int) -> None:
        target = target.removeprefix("<").removesuffix(">")
        target = re.sub(r"\\([ ()\[\]])", r"\1", target)
        try:
            url = urlsplit(target)
        except ValueError:
            self.error(source, f"line {line}: malformed link {target!r}")
            return
        if url.scheme and url.scheme.lower() != "file":
            return
        if url.netloc and not url.scheme:  # Protocol-relative external URL.
            return
        local = unquote(url.path)
        if url.scheme == "file" or local.startswith(("/", "\\")):
            self.error(source, f"line {line}: local link must use a repository-relative path: {target!r}")
            return
        path = source.parent / local if local else source
        try:
            resolved = path.resolve()
            exists = resolved.exists()
        except (OSError, RuntimeError, ValueError) as exc:
            self.error(source, f"line {line}: invalid local link {target!r} ({exc})")
            return
        if not resolved.is_relative_to(self.root):
            self.error(source, f"line {line}: local link escapes the repository: {target!r}")
            return
        if not exists:
            self.error(source, f"line {line}: missing local link target {target!r}")
            return
        if url.fragment and resolved.suffix.lower() == ".md":
            text = self.read_text(resolved)
            if text is not None and unquote(url.fragment) not in markdown_anchors(text):
                self.error(source, f"line {line}: unknown heading anchor in {target!r}")

    def check_markdown(self) -> None:
        for current, directories, filenames in os.walk(self.root, followlinks=False):
            directories[:] = sorted(name for name in directories if name not in SKIP_DIRECTORIES and not (Path(current) / name).is_symlink())
            for name in sorted(filenames):
                path = Path(current) / name
                if path.suffix.lower() != ".md":
                    continue
                text = self.read_text(path)
                if text is None:
                    continue
                text = without_fences(text)
                # Ignore code spans, retaining line numbers.
                text = re.sub(r"(`+)(.*?)\1", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
                definitions = {}
                for match in REFERENCE_DEFINITION.finditer(text):
                    key = " ".join(match.group(1).lower().split())
                    definitions[key] = match.group(2)
                    self.check_link(path, match.group(2), text.count("\n", 0, match.start()) + 1)
                for match in INLINE_LINK.finditer(text):
                    self.check_link(path, match.group("target"), text.count("\n", 0, match.start()) + 1)
                for match in REFERENCE_USE.finditer(text):
                    key = " ".join((match.group(2) or match.group(1)).lower().split())
                    if key not in definitions:
                        self.error(path, f"line {text.count(chr(10), 0, match.start()) + 1}: undefined link reference {key!r}")

    def run(self) -> list[str]:
        if not self.root.is_dir():
            self.error(self.root, "repository directory does not exist")
            return self.errors
        self.check_skills()
        self.check_markdown()
        return self.errors


def validate(root: Path) -> list[str]:
    return Validator(root).run()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="repository root (default: the parent of scripts/)")
    args = parser.parse_args(argv)
    errors = validate(args.root)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(EXPECTED_NAMES)} skills for each platform: names, metadata, footers, shared content, references, payloads, and local Markdown links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
