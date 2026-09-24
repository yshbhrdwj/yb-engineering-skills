"""Repository-level mutation tests; all changes stay inside temporary copies."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_validator", REPOSITORY / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidateRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="yb-validation-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for platform in ("codex", "claude-code"):
            shutil.copytree(REPOSITORY / platform / "skills", self.root / platform / "skills", symlinks=True)
        (self.root / "README.md").write_text(
            "# Test repository\n\n[Skill](codex/skills/yb-frontend-reviewer/SKILL.md)\n",
            encoding="utf-8",
        )

    def skill(self, platform="codex", name="yb-frontend-reviewer"):
        return self.root / platform / "skills" / name

    def assert_error(self, text):
        errors = validator.validate(self.root)
        self.assertTrue(any(text in error for error in errors), errors)

    def test_clean_tree(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_missing_reference_is_reported_even_when_both_platforms_match(self):
        for platform in ("codex", "claude-code"):
            (self.skill(platform) / "references/interaction-probes.md").unlink()
        self.assert_error("missing local link target 'references/interaction-probes.md'")

    def test_shared_core_drift(self):
        path = self.skill("claude-code") / "SKILL.md"
        path.write_text(path.read_text().replace("Assess how the interface", "Reconsider how the interface", 1))
        self.assert_error("shared core differs from Codex")

    def test_reference_drift(self):
        path = self.skill("claude-code") / "references/interaction-probes.md"
        path.write_text(path.read_text() + "\nA platform-specific change.\n")
        self.assert_error("reference differs or is missing between platforms")

    def test_exact_skill_inventory(self):
        self.skill().rename(self.skill().with_name("yb-renamed-reviewer"))
        self.assert_error("missing expected skill directory")
        self.assert_error("unexpected entry")

    def test_frontmatter_name_and_description(self):
        path = self.skill() / "SKILL.md"
        text = path.read_text().replace("name: yb-frontend-reviewer", "name: Invalid_Name", 1)
        lines = text.splitlines()
        lines[2] = "description: " + "x" * 201
        path.write_text("\n".join(lines) + "\n")
        self.assert_error("frontmatter name must match")
        self.assert_error("200-character portable limit")

    def test_missing_host_footer(self):
        path = self.skill() / "SKILL.md"
        path.write_text(path.read_text().split("\n## Codex integration", 1)[0])
        self.assert_error("complete Codex integration footer at the end")

    def test_frontmatter_rejects_yaml_nonstrings_and_decoded_controls(self):
        path = self.skill() / "SKILL.md"
        original = path.read_text()
        for value, expected in [('null', 'ambiguous YAML scalar'),
                                ('Review: code', 'ambiguous YAML scalar'),
                                ('"\\u0000"', 'nonempty single-line string')]:
            with self.subTest(value=value):
                lines = original.splitlines()
                lines[2] = "description: " + value
                path.write_text("\n".join(lines) + "\n")
                self.assert_error(expected)

    def test_metadata_must_invoke_its_skill(self):
        path = self.skill() / "agents/openai.yaml"
        path.write_text(path.read_text().replace("$yb-frontend-reviewer", "$yb-software-engineer"))
        self.assert_error("default_prompt must explicitly invoke $yb-frontend-reviewer")

    def test_metadata_rejects_duplicate_unquoted_and_short_fields(self):
        path = self.skill() / "agents/openai.yaml"
        path.write_text('interface:\n  display_name: "First"\n  display_name: "Second"\n'
                        '  short_description: "tiny"\n  default_prompt: unquoted\n')
        self.assert_error("duplicate interface field")
        self.assert_error("JSON-quoted string")
        self.assert_error("25–64 characters")

    def test_docs_links_and_heading_anchors(self):
        (self.root / "Guide with spaces.md").write_text("# Guide\n\n## Details\n\n## Details\n")
        path = self.root / "README.md"
        path.write_text('# Readme\n[guide](<Guide with spaces.md#details-1>)\n'
                        '[reference][guide]\n[guide]: Guide%20with%20spaces.md#details\n'
                        '`[not a link](missing.md)`\n```md\n[example](also-missing.md)\n```\n')
        self.assertEqual(validator.validate(self.root), [])
        path.write_text(path.read_text() + "\n[bad](Guide%20with%20spaces.md#absent)\n")
        self.assert_error("unknown heading anchor")

    def test_docs_missing_and_escaping_links(self):
        (self.root / "README.md").write_text("[missing](absent.md)\n[outside](../outside.md)\n")
        self.assert_error("missing local link target")
        self.assert_error("local link escapes the repository")

    def test_malformed_local_link_is_an_error_not_an_exception(self):
        (self.root / "README.md").write_text("[invalid](bad%00path.md)\n")
        self.assert_error("invalid local link")

    def test_binary_and_unexpected_payloads(self):
        (self.skill() / "references/payload.md").write_bytes(b"\x00binary")
        (self.skill() / "payload.zip").write_bytes(b"PK\x03\x04")
        self.assert_error("binary/control-byte payload")
        self.assert_error("unexpected skill payload")

    def test_symlink_is_rejected_without_following_it(self):
        target = self.root / "outside.md"
        target.write_text("# Not a packaged reference\n")
        link = self.skill() / "references/linked.md"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assert_error("symlinks are not allowed")

    def test_cli_has_actionable_nonzero_exit(self):
        (self.skill() / "agents/openai.yaml").unlink()
        result = subprocess.run(
            [sys.executable, str(REPOSITORY / "scripts/validate.py"), "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("yb-frontend-reviewer/agents/openai.yaml", result.stderr)
        self.assertIn("missing readable Codex display metadata", result.stderr)


if __name__ == "__main__":
    unittest.main()
