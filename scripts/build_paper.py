#!/usr/bin/env python3
"""Build the current Typst paper; optionally render every page for visual review."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, help="Write page PNGs here for visual review")
    args = parser.parse_args()
    try:
        import typst
    except ImportError:
        print(
            "Install build dependencies first:\n"
            "  python3 -m pip install -r requirements-build.txt\n"
            "Japanese fonts: Hiragino Mincho ProN (macOS), or Noto Serif CJK JP.\n"
            "Heading fonts: Hiragino Sans (macOS), or Noto Sans CJK JP.",
            file=sys.stderr,
        )
        return 1

    source = ROOT / "output/current/dimensional_shift.typ"
    output = source.with_suffix(".pdf")
    try:
        pdf = typst.compile(str(source), root=str(ROOT), format="pdf")
        pending = output.with_suffix(".pdf.tmp")
        pending.write_bytes(pdf)
        pending.replace(output)
        print(f"Built {output.relative_to(ROOT)} ({len(pdf):,} bytes)")
        if args.preview_dir:
            preview_dir = args.preview_dir.resolve()
            preview_dir.mkdir(parents=True, exist_ok=True)
            rendered = typst.compile(str(source), root=str(ROOT), format="png", ppi=120)
            pages = [rendered] if isinstance(rendered, bytes) else rendered
            for index, png in enumerate(pages, start=1):
                (preview_dir / f"page-{index:02d}.png").write_bytes(png)
            print(f"Rendered {len(pages)} pages to {preview_dir}")
    except Exception as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
