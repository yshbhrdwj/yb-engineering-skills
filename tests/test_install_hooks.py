"""Opt-in hook installation and migration in disposable homes/projects."""
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install_hooks.py"
SPEC = importlib.util.spec_from_file_location("hook_installer", SCRIPT)
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class HookInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="yb-hook-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "home with spaces"
        self.home.mkdir()

    def run_installer(self, *args, code=0):
        env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, str(SCRIPT), *args], env=env,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def settings(self, base=None):
        return json.loads(((base or self.home) / ".claude/settings.json").read_text())

    def test_explicit_target_is_required(self):
        self.run_installer(code=2)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_dry_run_writes_nothing(self):
        self.run_installer("--user", "--home", str(self.home), "--dry-run")
        self.assertEqual(list(self.home.iterdir()), [])

    def test_user_install_without_reviewers_fails_closed_at_runtime(self):
        self.run_installer("--user", "--home", str(self.home))
        settings = self.settings()
        self.assertEqual(settings["hooks"]["PreToolUse"][0]["matcher"], "Bash")
        for event, name in (("PreToolUse", "yb_merge_gate.py"), ("Stop", "yb_stop_check.py")):
            hook = settings["hooks"][event][0]["hooks"][0]
            self.assertEqual(hook["command"], sys.executable)
            self.assertEqual(hook["args"], [str(self.home / ".claude/hooks" / name)])
            self.assertEqual(hook["onFailure"], "block")
        config = json.loads((self.home / ".claude/yb-hooks.json").read_text())
        self.assertEqual(config["trusted_reviewers"], [])
        for name in ("yb_merge_gate.py", "yb_stop_check.py"):
            installed = self.home / ".claude/hooks" / name
            self.assertEqual(installed.read_bytes(), (ROOT / "claude-code/hooks" / name).read_bytes())

    def test_extracted_bundle_installer_finds_sibling_hooks(self):
        bundle = self.root / "extracted-bundle"
        (bundle / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, bundle / "scripts/install_hooks.py")
        shutil.copytree(ROOT / "claude-code/hooks", bundle / "hooks")
        result = subprocess.run([sys.executable, str(bundle / "scripts/install_hooks.py"),
                                 "--user", "--home", str(self.home)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".claude/hooks/yb_merge_gate.py").is_file())

    def test_project_reviewers_only_has_no_global_allowlist(self):
        self.run_installer("--user", "--home", str(self.home), "--project-reviewers-only")
        path = self.home / ".claude/yb-hooks.json"
        config = json.loads(path.read_text())
        self.assertIs(config["project_reviewers_only"], True)
        self.assertNotIn("trusted_reviewers", config)
        self.run_installer("--user", "--home", str(self.home), "--project-reviewers-only")
        self.run_installer("--user", "--home", str(self.home), "--project-reviewers-only",
                           "--trusted-reviewer", "reviewer", "--update", code=1)
        self.assertNotIn("trusted_reviewers", json.loads(path.read_text()))

    def test_identical_reinstall_is_no_op(self):
        self.run_installer("--user", "--home", str(self.home), "--trusted-reviewer", "trusted[bot]")
        path = self.home / ".claude/settings.json"
        before = path.stat().st_mtime_ns
        self.run_installer("--user", "--home", str(self.home))
        self.assertEqual(path.stat().st_mtime_ns, before)
        self.assertFalse((self.home / ".yb-engineering-skills-backups").exists())
        self.assertEqual(len(self.settings()["hooks"]["Stop"]), 1)

    def test_settings_conflict_requires_update_before_any_write(self):
        (self.home / ".claude").mkdir()
        path = self.home / ".claude/settings.json"
        path.write_text('{"permissions":{"allow":["Read"]}}')
        original = path.read_bytes()
        self.run_installer("--user", "--home", str(self.home), code=1)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse((self.home / ".claude/hooks").exists())

    def test_legacy_migration_preserves_unrelated_entries_and_backs_up(self):
        hooks = self.home / ".claude/hooks"
        hooks.mkdir(parents=True)
        for name in ("yb-merge-gate.sh", "yb-stop-check.sh"):
            (hooks / name).write_text("old unsafe hook")
        unrelated = {"type": "command", "command": "my-security-hook", "timeout": 4}
        original = {"model": "keep", "permissions": {"allow": ["Read"]}, "hooks": {
            "PreToolUse": [{"matcher": "Bash", "hooks": [
                {"type": "command", "command": "$HOME/.claude/hooks/yb-merge-gate.sh"}, unrelated]}],
            "Stop": [{"hooks": [{"type": "command", "command": "$HOME/.claude/hooks/yb-stop-check.sh"}]}],
            "SessionStart": [{"hooks": [{"type": "command", "command": "other"}]}]}}
        settings = self.home / ".claude/settings.json"
        settings.write_text(json.dumps(original))
        self.run_installer("--user", "--home", str(self.home), "--update", "--trusted-reviewer", "trusted[bot]")
        updated = self.settings()
        self.assertEqual(updated["model"], original["model"])
        self.assertEqual(updated["permissions"], original["permissions"])
        self.assertEqual(updated["hooks"]["SessionStart"], original["hooks"]["SessionStart"])
        self.assertEqual(updated["hooks"]["PreToolUse"][0]["hooks"], [unrelated])
        self.assertFalse((hooks / "yb-merge-gate.sh").exists())
        self.assertFalse((hooks / "yb-stop-check.sh").exists())
        backup = next((self.home / ".yb-engineering-skills-backups").iterdir())
        self.assertEqual(json.loads((backup / ".claude/settings.json").read_text()), original)
        self.assertEqual((backup / ".claude/hooks/yb-merge-gate.sh").read_text(), "old unsafe hook")

    def test_windows_managed_python_paths_support_both_quote_conventions_on_every_host(self):
        import shlex
        home = PureWindowsPath(r"C:\Users\Example User")
        folder = home / ".claude" / "hooks"
        for interpreter in (r"C:\Old Python\python3.10.exe", "/old/python3.10"):
            for name in ("yb_merge_gate.py", "yb_stop_check.py"):
                arguments = [interpreter, str(folder / name)]
                for command in (subprocess.list2cmdline(arguments), shlex.join(arguments)):
                    with self.subTest(command=command):
                        self.assertTrue(INSTALLER.owned(command, folder, home))

    def test_exec_form_ownership_is_exact_across_platform_path_representations(self):
        home = PureWindowsPath(r"C:\Users\Example User")
        folder = home / ".claude" / "hooks"
        script = str(folder / "yb_merge_gate.py")
        self.assertTrue(INSTALLER.owned(r"C:\Old Python\python.exe", folder, home, [script]))
        self.assertFalse(INSTALLER.owned(r"C:\Old Python\other.exe", folder, home, [script]))
        self.assertFalse(INSTALLER.owned("python.exe", folder, home, [script, "--extra"]))
        self.assertFalse(INSTALLER.owned("python.exe", folder, home, [script + ".bak"]))
        self.assertFalse(INSTALLER.owned("python.exe", folder, home, []))

    def test_python_ownership_requires_exact_script_and_no_extra_commands(self):
        import shlex
        home = PureWindowsPath(r"C:\Users\Example User")
        folder = home / ".claude" / "hooks"
        good = subprocess.list2cmdline([r"C:\Old Python\python.exe", str(folder / "yb_merge_gate.py")])
        invalid = [good + " --extra", good + " && other-command", good + "; other-command",
                   subprocess.list2cmdline(["other.exe", str(folder / "yb_merge_gate.py")]),
                   subprocess.list2cmdline(["python.exe", str(home / "other/yb_merge_gate.py")]),
                   shlex.join(["python3", str(folder / "yb_merge_gate.py") + ".bak"]),
                   "command " + good]
        for command in invalid:
            with self.subTest(command=command):
                self.assertFalse(INSTALLER.owned(command, folder, home))

    def test_reinstall_retires_managed_python_command_after_interpreter_changes(self):
        self.run_installer("--user", "--home", str(self.home))
        settings = self.settings()
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]
        import shlex
        command["command"] = shlex.join(["/old/python3.10", str(self.home / ".claude/hooks/yb_merge_gate.py")])
        command.pop("args")
        path = self.home / ".claude/settings.json"
        path.write_text(json.dumps(settings))
        self.run_installer("--user", "--home", str(self.home), "--update")
        hooks = self.settings()["hooks"]["PreToolUse"]
        self.assertEqual(len(hooks), 1)
        self.assertNotIn("/old/python", hooks[0]["hooks"][0]["command"])
        # An exec-form entry from an older Python installation is also ours.
        settings = self.settings()
        settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"] = "/old/python3.10"
        path.write_text(json.dumps(settings))
        self.run_installer("--user", "--home", str(self.home), "--update")
        hooks = self.settings()["hooks"]["PreToolUse"]
        self.assertEqual(len(hooks), 1)
        self.assertEqual(hooks[0]["hooks"][0]["command"], sys.executable)
        self.assertEqual(hooks[0]["hooks"][0]["args"], [str(self.home / ".claude/hooks/yb_merge_gate.py")])

    def test_project_install_does_not_touch_home(self):
        project = self.root / "project"
        project.mkdir()
        self.run_installer("--project", str(project), "--trusted-reviewer", "reviewer")
        self.assertTrue((project / ".claude/settings.json").is_file())
        self.assertEqual(list(self.home.iterdir()), [])
        self.run_installer("--project", str(project), "--home", str(self.home), code=2)

    def test_dry_run_update_does_not_create_backup_or_mutate(self):
        self.run_installer("--user", "--home", str(self.home))
        path = self.home / ".claude/hooks/yb_merge_gate.py"
        path.write_text("locally changed")
        self.run_installer("--user", "--home", str(self.home), "--update", "--dry-run")
        self.assertEqual(path.read_text(), "locally changed")
        self.assertFalse((self.home / ".yb-engineering-skills-backups").exists())

    def test_malformed_settings_and_reviewers_fail_before_writes(self):
        self.run_installer("--user", "--home", str(self.home), "--trusted-reviewer", "anyone/*", code=1)
        (self.home / ".claude").mkdir()
        (self.home / ".claude/settings.json").write_text("[]")
        self.run_installer("--user", "--home", str(self.home), "--update", code=1)
        self.assertFalse((self.home / ".claude/hooks").exists())

    def test_symlinks_and_directory_conflicts_are_rejected(self):
        if os.name == "nt":
            self.skipTest("symlink privileges vary")
        outside = self.root / "outside"
        outside.mkdir()
        (self.home / ".claude").symlink_to(outside, target_is_directory=True)
        self.run_installer("--user", "--home", str(self.home), "--update", code=1)
        self.assertEqual(list(outside.iterdir()), [])
        (self.home / ".claude").unlink()
        (self.home / ".claude/hooks/yb_merge_gate.py").mkdir(parents=True)
        self.run_installer("--user", "--home", str(self.home), "--update", code=1)

    def test_backup_symlink_rejected_before_overwrite(self):
        if os.name == "nt":
            self.skipTest("symlink privileges vary")
        self.run_installer("--user", "--home", str(self.home))
        file = self.home / ".claude/hooks/yb_merge_gate.py"
        file.write_text("local")
        outside = self.root / "outside"
        outside.mkdir()
        (self.home / ".yb-engineering-skills-backups").symlink_to(outside, target_is_directory=True)
        self.run_installer("--user", "--home", str(self.home), "--update", code=1)
        self.assertEqual(file.read_text(), "local")
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
