#!/usr/bin/env python3
"""Archive a visualizer release locally, never overwriting an earlier release."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = ('coordinate-lift.html', 'export_site.py', 'test-model.cjs',
                'test-browser.cjs', 'test-public.cjs', 'README.md', 'CHANGELOG.md', 'version.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--site-index', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'visualizer-v\d+\.\d+\.\d+', args.version):
        parser.error('Use visualizer-vMAJOR.MINOR.PATCH')
    current = ROOT / 'visualizer'
    history = current / 'history'
    history.mkdir(parents=True, exist_ok=True)
    target = history / args.version
    if target.exists():
        parser.error('Existing release cannot be overwritten: ' + str(target))
    config = json.loads((current / 'version.json').read_text())
    if config['version'] != args.version:
        parser.error('Version must match visualizer/version.json')
    sources = [(current / name, name) for name in SOURCE_FILES if (current / name).exists()]
    if not (current / 'coordinate-lift.html').is_file() or not args.site_index.is_file():
        parser.error('Both the inline source and standalone index must exist')
    sources.append((args.site_index, 'site/index.html'))
    staging = Path(tempfile.mkdtemp(prefix='.snapshot-', dir=history))
    try:
        entries = []
        for source, name in sources:
            data = source.read_bytes()
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            entries.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        metadata = {'version': args.version, 'paper_version': config['paper_version'],
                    'created_at': datetime.now(ZoneInfo('Asia/Tokyo')).isoformat(timespec='seconds'),
                    'scope': 'local archive; do not publish', 'files': entries}
        (staging / 'metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
        if target.exists():
            raise FileExistsError(target)
        staging.rename(target)
        print(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


if __name__ == '__main__':
    main()
