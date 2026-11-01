"""Validate and package portable editions into dist/ or an explicit output directory."""
import argparse
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ('START-HERE.md', 'SDLC-WORKFLOW.md', 'VALIDATION.md',
          'TOKEN-EFFICIENCY.md', 'PONYTAIL-COMPARISON.md')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist',
                        help='Archive directory (default: repository dist/)')
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    packaged_roots = ('codex', 'claude-code', 'docs/evidence', 'evals')
    if any(output.is_relative_to((ROOT / name).resolve()) for name in packaged_roots):
        parser.error('output directory must be outside packaged source trees')
    subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py')], check=True)
    output.mkdir(parents=True, exist_ok=True)
    for platform in ('codex', 'claude-code'):
        source = ROOT / platform
        prefix = Path(f'{platform}-engineering-skills')
        target = output / f'{platform}-engineering-skills.zip'
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(source.rglob('*')):
                if path.is_symlink():
                    raise RuntimeError(f'Refusing symlink in bundle: {path.relative_to(ROOT)}')
                if path.is_file() and '__pycache__' not in path.parts and path.name != '.DS_Store':
                    bundle.write(path, (prefix / path.relative_to(source)).as_posix())
            for name in GUIDES:
                content = (ROOT / name).read_text(encoding='utf-8')
                if name == 'START-HERE.md':
                    content = content.replace(
                        '[Claude Code](claude-code/README.md) and [Codex](codex/README.md) guides',
                        '[platform README](README.md)')
                    if platform == 'claude-code':
                        content = content.replace('](claude-code/HOOKS.md)', '](HOOKS.md)')
                    else:
                        content = content.replace(
                            'Optional hooks have a [separate setup](claude-code/HOOKS.md).',
                            'Optional Claude hooks are supplied in the Claude Code bundle.')
                bundle.writestr((prefix / name).as_posix(), content)
            for directory in ('docs/evidence', 'evals'):
                for path in sorted((ROOT / directory).rglob('*')):
                    if path.is_file() and '__pycache__' not in path.parts:
                        target_path = (prefix / path.relative_to(ROOT)).as_posix()
                        if path.suffix == '.md':
                            content = path.read_text(encoding='utf-8')
                            # Shared evidence links to a source edition; bundles expose skills/ directly.
                            for source_platform in ('codex', 'claude-code'):
                                content = content.replace(f'](../../{source_platform}/skills/', '](../../skills/')
                            bundle.writestr(target_path, content)
                        else:
                            bundle.write(path, target_path)
            helpers = ['summarize_evals.py']
            if platform == 'claude-code':
                helpers.append('install_hooks.py')
            for helper in helpers:
                bundle.write(ROOT / 'scripts' / helper,
                             (prefix / 'scripts' / helper).as_posix())
            if (ROOT / 'LICENSE').is_file():
                bundle.write(ROOT / 'LICENSE', (prefix / 'LICENSE').as_posix())
        with zipfile.ZipFile(target) as bundle:
            if bundle.testzip() is not None:
                raise RuntimeError(f'Corrupt archive: {target}')
            if sum(p.endswith('/SKILL.md') for p in bundle.namelist()) != 12:
                raise RuntimeError(f'Expected twelve skills in {target}')
        print(f'Created {target} ({target.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
