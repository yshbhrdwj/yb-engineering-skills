"""Verify extracted deliverables, including the optional hook install path."""
from pathlib import Path
import importlib.util
import shutil
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
    def test_output_cannot_contaminate_or_include_packaged_source(self):
        with tempfile.TemporaryDirectory(prefix='yb-package-source-') as temporary:
            root = Path(temporary).resolve()
            (root / 'scripts').mkdir()
            shutil.copy2(ROOT / 'scripts/package.py', root / 'scripts/package.py')
            for name in ('codex', 'claude-code', 'evals', 'docs/evidence'):
                source = root / name
                source.mkdir(parents=True)
                output = source / 'generated'
                result = subprocess.run([sys.executable, str(root / 'scripts/package.py'),
                                         '--output-dir', str(output)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn('outside packaged source trees', result.stderr)
                self.assertFalse(output.exists())

    def test_bundles_include_eleven_skills_and_working_hook_installer(self):
        with tempfile.TemporaryDirectory(prefix='yb-bundle-') as temporary:
            base = Path(temporary).resolve()
            output = base / 'archives'
            # Explicit output keeps ordinary test runs from changing ROOT/dist.
            before = {p.name: p.read_bytes() for p in (ROOT / 'dist').glob('*.zip')}
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/package.py'),
                                     '--output-dir', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in (ROOT / 'dist').glob('*.zip')})
            for platform in ('codex', 'claude-code'):
                with zipfile.ZipFile(output / f'{platform}-engineering-skills.zip') as bundle:
                    self.assertIsNone(bundle.testzip())
                    self.assertEqual(sum(x.endswith('/SKILL.md') for x in bundle.namelist()), 11)
                    bundle.extractall(base)
                extracted = base / f'{platform}-engineering-skills'
                self.assertTrue((extracted / 'evals/cases.json').is_file())
                self.assertNotIn('blob/main/claude-code/HOOKS.md',
                                 (extracted / 'START-HERE.md').read_text())
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
