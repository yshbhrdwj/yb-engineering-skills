"""Validate and package both portable platform editions into dist/."""
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ('SDLC-WORKFLOW.md', 'VALIDATION.md', 'TOKEN-EFFICIENCY.md',
          'PONYTAIL-COMPARISON.md')


def main():
    subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py')], check=True)
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    for platform in ('codex', 'claude-code'):
        source = ROOT / platform
        prefix = Path(f'{platform}-engineering-skills')
        target = output / f'{platform}-engineering-skills.zip'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(source.rglob('*')):
                if path.is_file():
                    bundle.write(path, (prefix / path.relative_to(source)).as_posix())
            for name in GUIDES:
                bundle.write(ROOT / name, (prefix / name).as_posix())
            if (ROOT / 'LICENSE').is_file():
                bundle.write(ROOT / 'LICENSE', (prefix / 'LICENSE').as_posix())
        with zipfile.ZipFile(target) as bundle:
            if bundle.testzip() is not None:
                raise RuntimeError(f'Corrupt archive: {target}')
            if sum(p.endswith('/SKILL.md') for p in bundle.namelist()) != 10:
                raise RuntimeError(f'Expected ten skills in {target}')
        print(f'Created {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
