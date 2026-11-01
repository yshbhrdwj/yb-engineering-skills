"""Stop-hook configuration and Windows runner regressions, using local fixtures."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'claude-code/hooks/yb_stop_check.py'
SPEC = importlib.util.spec_from_file_location('stop_regressions', SOURCE)
STOP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STOP)


class StopConfigTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='yb-stop-config-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / 'repo'
        (self.repo / '.claude').mkdir(parents=True)
        self.installed = self.base / 'installation/.claude/hooks/yb_stop_check.py'
        self.installed.parent.mkdir(parents=True)
        self.install_config = self.installed.parents[1] / 'yb-hooks.json'
        self.project_config = self.repo / '.claude/yb-hooks.json'
        self.file_patch = mock.patch.object(STOP, '__file__', str(self.installed))
        self.file_patch.start()
        self.addCleanup(self.file_patch.stop)

    def test_install_defaults_and_project_timeout_override(self):
        self.assertEqual(STOP.check_timeout(self.repo), 120)
        self.install_config.write_text('{"check_timeout_seconds":7}')
        self.assertEqual(STOP.check_timeout(self.repo), 7)
        self.project_config.write_text('{"trusted_reviewers":["reviewer"]}')
        self.assertEqual(STOP.check_timeout(self.repo), 7)
        self.project_config.write_text('{"check_timeout_seconds":3}')
        self.assertEqual(STOP.check_timeout(self.repo), 3)

    def test_project_install_config_is_not_read_twice(self):
        self.installed = self.repo / '.claude/hooks/yb_stop_check.py'
        self.installed.parent.mkdir()
        self.project_config.write_text('{"check_timeout_seconds":4}')
        with mock.patch.object(STOP, '__file__', str(self.installed)):
            self.assertEqual(STOP.check_timeout(self.repo), 4)

    def test_invalid_or_nonfinite_timeout_and_nonobject_config_fail_clearly(self):
        for value in (None, True, '3', 0, 301, 10**400, float('nan'), float('inf')):
            with self.subTest(value=value):
                self.install_config.write_text(json.dumps({'check_timeout_seconds': value}))
                with self.assertRaises(STOP.CheckError):
                    STOP.check_timeout(self.repo)
        for text in ('[]', 'null', '{broken'):
            with self.subTest(text=text):
                self.install_config.write_text(text)
                with self.assertRaises(STOP.CheckError):
                    STOP.check_timeout(self.repo)

    @unittest.skipIf(os.name == 'nt', 'real POSIX check process; Windows command is tested separately')
    def test_installed_timeout_is_used_by_actual_hook_without_project_config(self):
        shutil.copy2(SOURCE, self.installed)
        self.install_config.write_text('{"check_timeout_seconds":1}')
        self.env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
                        GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
        def git(*args):
            subprocess.run(['git', *args], cwd=self.repo, env=self.env,
                           capture_output=True, check=True)
        git('init', '-q')
        (self.repo / 'source.txt').write_text('initial')
        git('add', 'source.txt')
        git('-c', 'commit.gpgsign=false', '-c', 'user.name=Fixture',
            '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
        check = self.repo / '.claude/yb-check.sh'
        check.write_text('#!/bin/sh\nsleep 20\n')
        check.chmod(0o755)
        started = time.monotonic()
        result = subprocess.run([sys.executable, str(self.installed)],
                                input=json.dumps({'cwd':str(self.repo)}),
                                text=True, capture_output=True, env=self.env, timeout=8)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('exceeded 1s', result.stderr)
        self.assertLess(time.monotonic() - started, 8)


class StopWindowsRunnerTests(unittest.TestCase):
    def test_windows_shell_check_uses_explicit_bash_not_direct_sh_file(self):
        check = Path('project/.claude/yb-check.sh')
        with mock.patch.dict(STOP.os.environ, {}, clear=True):
            with mock.patch.object(STOP.shutil, 'which', return_value=r'C:\Git\bin\bash.exe'):
                self.assertEqual(STOP.check_command(check, platform='nt'),
                                 [r'C:\Git\bin\bash.exe', str(check)])
            with mock.patch.object(STOP.shutil, 'which', return_value=None):
                with self.assertRaisesRegex(STOP.CheckError, 'requires Bash on Windows'):
                    STOP.check_command(check, platform='nt')
        self.assertEqual(STOP.check_command(check, platform='posix'), [str(check)])

    def test_windows_explicit_git_bash_path_has_precedence(self):
        check = Path('yb-check.sh')
        with mock.patch.dict(STOP.os.environ, {'CLAUDE_CODE_GIT_BASH_PATH':r'C:\Chosen Git\bash.exe'}, clear=True):
            with mock.patch.object(STOP.shutil, 'which') as find:
                self.assertEqual(STOP.check_command(check, platform='nt'),
                                 [r'C:\Chosen Git\bash.exe', str(check)])
                find.assert_not_called()

    def test_windows_timeout_terminates_process_tree_with_parent_fallback(self):
        process = mock.Mock(pid=42)
        process.poll.return_value = None
        with mock.patch.object(STOP.subprocess, 'run') as run:
            STOP.terminate_check(process, platform='nt')
            run.assert_called_once_with(['taskkill','/PID','42','/T','/F'],
                                        capture_output=True, timeout=5, check=False)
        process.kill.assert_called_once()
        process.wait.assert_called_once_with(timeout=5)

    def test_windows_missing_taskkill_still_stops_parent(self):
        process = mock.Mock(pid=43)
        process.poll.return_value = None
        with mock.patch.object(STOP.subprocess, 'run', side_effect=FileNotFoundError):
            STOP.terminate_check(process, platform='nt')
        process.kill.assert_called_once()
        process.wait.assert_called_once_with(timeout=5)


if __name__ == '__main__':
    unittest.main()
