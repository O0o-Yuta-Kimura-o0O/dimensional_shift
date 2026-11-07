#!/usr/bin/env python3
"""Export the existing inline visualizer as a standalone public page."""

import argparse
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renderer", required=True, type=Path,
                        help="Path to visualize/scripts/render.py")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().with_name("coordinate-lift.html")
    fragment = source.read_text(encoding="utf-8")
    calls = set(re.findall(r"window\.openai(?:\?\.)?\.?([A-Za-z_$][\w$]*)", fragment))
    if calls - {"widgetState", "setWidgetState"}:
        raise SystemExit(f"Host-only API requires replacement: {sorted(calls)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(args.renderer.resolve()), str(source),
                    str(args.output.resolve()), "--force", "--title",
                    "Dimensional Shift | 独立座標生成 v0.1.1"], check=True)
    document = args.output.read_text(encoding="utf-8")
    document = document.replace('<html lang="en"', '<html lang="ja"')
    document = document.replace('&lt;html lang=&quot;en&quot;', '&lt;html lang=&quot;ja&quot;')
    metadata = '\n'.join([
        '<meta name="description" content="Lを適用するたびに独立座標を生成し、実数空間と離散格子を切り替えるビジュアライザー。対応論文 v0.2.0。">',
        '<meta name="visualizer-version" content="visualizer-v0.1.1">',
        '<meta name="paper-version" content="v0.2.0">',
        '<meta name="author" content="木村祐太・GPT-6 Astra（AI）">',
    ])
    document = document.replace('</head>', metadata + '\n</head>', 1)
    args.output.write_text(document, encoding="utf-8")
    data = args.output.read_bytes()
    print(f"Standalone export: {args.output.resolve()}")
    print(f"Bytes: {len(data)}; SHA-256: {sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
