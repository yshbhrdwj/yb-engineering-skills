"""Installer integration tests use only isolated temporary homes/projects."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repository"
        self.home = self.root / "home"
        self.home.mkdir()
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.repo / "scripts" / "install.py")
        for target in ("codex", "claude-code"):
            for name in ("yb-first", "yb-second"):
                source = self.repo / target / "skills" / name
                (source / "references").mkdir(parents=True)
                (source / "SKILL.md").write_text(f"{target}: {name}\n", encoding="utf-8")
                (source / "references" / "guide.md").write_text("Shared guidance\n", encoding="utf-8")

    def run_installer(self, *args, success=True):
        env = os.environ.copy()
        env.update(HOME=str(self.home), USERPROFILE=str(self.home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts" / "install.py"), *args],
            env=env, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def skill(self, platform=".agents", name="yb-first", base=None):
        return (base or self.home) / platform / "skills" / name

    def test_installs_corresponding_sources_for_both_targets(self):
        self.run_installer("--target", "both")
        for target, platform in (("codex", ".agents"), ("claude-code", ".claude")):
            for name in ("yb-first", "yb-second"):
                skill = self.skill(platform, name)
                self.assertEqual((skill / "SKILL.md").read_text(), f"{target}: {name}\n")
                self.assertEqual((skill / "references" / "guide.md").read_text(), "Shared guidance\n")

    def test_single_target_does_not_install_other_platform(self):
        self.run_installer("--target", "claude-code")
        self.assertTrue(self.skill(".claude").is_dir())
        self.assertFalse((self.home / ".agents").exists())

    def test_actual_repository_bundle_installs_in_an_isolated_project(self):
        project = self.root / "bundle-project"
        project.mkdir()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--target", "both", "--project", str(project)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for target, platform in (("codex", ".agents"), ("claude-code", ".claude")):
            for source in (SCRIPT.parents[1] / target / "skills").iterdir():
                installed = self.skill(platform, source.name, project)
                for file in source.rglob("*"):
                    if file.is_file():
                        self.assertEqual(file.read_bytes(), (installed / file.relative_to(source)).read_bytes())

    def test_identical_install_is_a_no_op(self):
        self.run_installer("--target", "codex")
        installed = self.skill() / "SKILL.md"
        os.utime(installed, ns=(1_000_000_000, 1_000_000_000))
        before = installed.stat().st_mtime_ns
        result = self.run_installer("--target", "codex", "--update")
        self.assertEqual(installed.stat().st_mtime_ns, before)
        self.assertIn("unchanged", result.stdout)
        self.assertFalse((self.home / ".yb-engineering-skills-backups").exists())

    def test_conflicts_are_preflighted_across_targets_before_any_write(self):
        conflict = self.skill(".claude", "yb-second")
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("Local content")
        result = self.run_installer("--target", "both", success=False)
        self.assertIn("--update", result.stderr)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse(self.skill(".claude").exists())
        self.assertEqual((conflict / "SKILL.md").read_text(), "Local content")

    def test_update_backs_up_original_and_preserves_extras_and_unrelated_skills(self):
        self.run_installer("--target", "codex")
        skill = self.skill()
        (skill / "SKILL.md").write_text("Local content")
        (skill / "notes.txt").write_text("Keep this extra")
        unrelated = self.skill(name="unrelated")
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("Not managed here")

        self.run_installer("--target", "codex", "--update")

        backups = list((self.home / ".yb-engineering-skills-backups").iterdir())
        self.assertEqual(len(backups), 1)
        backup = backups[0] / "codex" / "yb-first"
        self.assertEqual((backup / "SKILL.md").read_text(), "Local content")
        self.assertEqual((backup / "notes.txt").read_text(), "Keep this extra")
        self.assertEqual((skill / "SKILL.md").read_text(), "codex: yb-first\n")
        self.assertEqual((skill / "notes.txt").read_text(), "Keep this extra")
        self.assertEqual((unrelated / "SKILL.md").read_text(), "Not managed here")
        self.assertNotIn(self.home / ".agents" / "skills", backup.parents)
        self.assertFalse((backups[0] / "codex" / "yb-second").exists())

    def test_dry_run_creates_nothing(self):
        result = self.run_installer("--target", "both", "--dry-run")
        self.assertIn("no files written", result.stdout)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_updating_a_hard_link_does_not_modify_its_other_name(self):
        self.run_installer("--target", "codex")
        file = self.skill() / "SKILL.md"
        file.write_text("Local content")
        extra = self.skill() / "local-copy.md"
        os.link(file, extra)
        self.run_installer("--target", "codex", "--update")
        self.assertEqual(file.read_text(), "codex: yb-first\n")
        self.assertEqual(extra.read_text(), "Local content")

    def test_dry_run_update_changes_nothing(self):
        self.run_installer("--target", "codex")
        file = self.skill() / "SKILL.md"
        file.write_text("Local content")
        self.run_installer("--target", "codex", "--update", "--dry-run")
        self.assertEqual(file.read_text(), "Local content")
        self.assertFalse((self.home / ".yb-engineering-skills-backups").exists())

    def test_project_install_leaves_home_untouched(self):
        project = self.root / "project with spaces"
        project.mkdir()
        self.run_installer("--target", "both", "--project", str(project))
        self.assertTrue(self.skill(base=project).is_dir())
        self.assertTrue(self.skill(".claude", base=project).is_dir())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_parent_traversal_is_rejected(self):
        project = self.root / "project"
        project.mkdir()
        self.run_installer("--target", "both", "--project", str(project / ".." / "project"), success=False)
        self.assertEqual(list(project.iterdir()), [])

    def test_source_file_symlink_is_rejected_before_writes(self):
        source = self.repo / "codex" / "skills" / "yb-second" / "SKILL.md"
        outside = self.root / "outside.md"
        outside.write_text("External content")
        source.unlink()
        source.symlink_to(outside)
        self.run_installer("--target", "codex", success=False)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_destination_folder_symlink_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        destination = self.skill()
        destination.parent.mkdir(parents=True)
        destination.symlink_to(outside, target_is_directory=True)
        self.run_installer("--target", "codex", "--update", success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_destination_extra_symlink_is_rejected(self):
        self.run_installer("--target", "codex")
        (self.skill() / "extra-link").symlink_to(self.root / "missing")
        result = self.run_installer("--target", "codex", success=False)
        self.assertIn("Symlinks", result.stderr)

    def test_project_ancestor_symlink_is_rejected(self):
        project = self.root / "actual-project"
        project.mkdir()
        linked = self.root / "linked-project"
        linked.symlink_to(project, target_is_directory=True)
        self.run_installer("--target", "codex", "--project", str(linked), success=False)
        self.assertEqual(list(project.iterdir()), [])

    def test_backup_symlink_is_rejected_before_overwrite(self):
        self.run_installer("--target", "codex")
        file = self.skill() / "SKILL.md"
        file.write_text("Local content")
        outside = self.root / "outside"
        outside.mkdir()
        (self.home / ".yb-engineering-skills-backups").symlink_to(outside, target_is_directory=True)
        self.run_installer("--target", "codex", "--update", success=False)
        self.assertEqual(file.read_text(), "Local content")
        self.assertEqual(list(outside.iterdir()), [])

    def test_file_directory_conflict_is_rejected_even_with_update(self):
        destination = self.skill()
        (destination / "SKILL.md").mkdir(parents=True)
        result = self.run_installer("--target", "codex", "--update", success=False)
        self.assertIn("File/directory conflict", result.stderr)
        self.assertFalse(self.skill(name="yb-second").exists())

    def add_migration_fixture(self):
        for target in ("codex", "claude-code"):
            source = self.repo / target / "skills" / "yb-code-reviewer"
            source.mkdir()
            (source / "SKILL.md").write_text("Unified code review")
        for platform in (".agents", ".claude"):
            for name in ("yb-code-correctness-reviewer", "yb-code-design-reviewer"):
                old = self.skill(platform, name)
                old.mkdir(parents=True)
                (old / "SKILL.md").write_text("Local old instructions")
                (old / "personal-notes.txt").write_text("Preserve in backup")

    def test_migration_backs_up_retired_skills_before_removing_them(self):
        self.add_migration_fixture()
        self.run_installer("--target", "both", "--update", "--migrate")
        backups = list((self.home / ".yb-engineering-skills-backups").iterdir())
        self.assertEqual(len(backups), 1)
        for target, platform in (("codex", ".agents"), ("claude-code", ".claude")):
            self.assertTrue(self.skill(platform, "yb-code-reviewer").exists())
            for name in ("yb-code-correctness-reviewer", "yb-code-design-reviewer"):
                self.assertFalse(self.skill(platform, name).exists())
                saved = backups[0] / target / name
                self.assertEqual((saved / "SKILL.md").read_text(), "Local old instructions")
                self.assertEqual((saved / "personal-notes.txt").read_text(), "Preserve in backup")

    def test_migration_is_explicit_and_dry_run_does_not_remove_anything(self):
        self.add_migration_fixture()
        self.run_installer("--target", "both", "--migrate", success=False)
        self.run_installer("--target", "both", "--update", "--migrate", "--dry-run")
        self.assertTrue(self.skill(name="yb-code-correctness-reviewer").exists())
        self.assertFalse((self.home / ".yb-engineering-skills-backups").exists())
        self.run_installer("--target", "both", "--update")
        self.assertTrue(self.skill(name="yb-code-correctness-reviewer").exists())

    def test_retired_skill_symlink_blocks_entire_migration_before_writes(self):
        self.add_migration_fixture()
        old = self.skill(name="yb-code-correctness-reviewer")
        shutil.rmtree(old)
        outside = self.root / "outside"
        outside.mkdir()
        old.symlink_to(outside, target_is_directory=True)
        self.run_installer("--target", "both", "--update", "--migrate", success=False)
        self.assertFalse(self.skill(name="yb-code-reviewer").exists())
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
