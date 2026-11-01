"""Verify extracted deliverables, including the optional hook install path."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bundle_validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PackageTests(unittest.TestCase):
    def test_bundles_include_ten_skills_and_working_hook_installer(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/package.py')],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with tempfile.TemporaryDirectory(prefix='yb-bundle-') as temporary:
            base = Path(temporary).resolve()
            for platform in ('codex', 'claude-code'):
                with zipfile.ZipFile(ROOT / 'dist' / f'{platform}-engineering-skills.zip') as bundle:
                    self.assertIsNone(bundle.testzip())
                    self.assertEqual(sum(x.endswith('/SKILL.md') for x in bundle.namelist()), 10)
                    bundle.extractall(base)
                extracted = base / f'{platform}-engineering-skills'
                self.assertTrue((extracted / 'evals/cases.json').is_file())
                self.assertTrue((extracted / 'docs/evidence/2026-11-01-eval-audit.md').is_file())
                links = validator.Validator(extracted)
                links.check_markdown()
                self.assertEqual(links.errors, [])
                if platform == 'claude-code':
                    project = base / 'isolated-project'
                    project.mkdir()
                    install = subprocess.run(
                        [sys.executable, str(extracted / 'scripts/install_hooks.py'),
                         '--project', str(project), '--trusted-reviewer', 'reviewer'],
                        capture_output=True, text=True)
                    self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
                    self.assertTrue((project / '.claude/hooks/yb_merge_gate.py').is_file())
                    self.assertTrue((project / '.claude/hooks/yb_stop_check.py').is_file())


if __name__ == '__main__':
    unittest.main()
