#!/usr/bin/env python3
"""Export bilingual Markdown and build both PDFs, with optional page previews."""

import argparse
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "ja": "dimensional_shift",
    "en": "dimensional_shift_en",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path, help="Write page PNGs to ja/ and en/ subdirectories")
    args = parser.parse_args()
    try:
        from export_markdown import export_all

        export_all(ROOT)
        print("Exported Japanese and English Markdown from the current Typst sources")
    except Exception as error:
        print(f"Markdown export failed: {error}", file=sys.stderr)
        return 1
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

    try:
        current = ROOT / "output/current"
        # Complete both compilations before replacing either published PDF.
        compiled = {}
        previews = {}
        for language, stem in PAPERS.items():
            source = current / f"{stem}.typ"
            compiled[language] = typst.compile(str(source), root=str(ROOT), format="pdf")
            if args.preview_dir:
                rendered = typst.compile(str(source), root=str(ROOT), format="png", ppi=120)
                previews[language] = [rendered] if isinstance(rendered, bytes) else rendered
        with tempfile.TemporaryDirectory(prefix=".build-", dir=current) as pending_dir:
            for language, stem in PAPERS.items():
                pending = Path(pending_dir) / f"{stem}.pdf"
                pending.write_bytes(compiled[language])
            for language, stem in PAPERS.items():
                output = current / f"{stem}.pdf"
                (Path(pending_dir) / output.name).replace(output)
                print(f"Built {output.relative_to(ROOT)} ({len(compiled[language]):,} bytes)")
        for language, pages in previews.items():
            preview_dir = args.preview_dir.resolve() / language
            preview_dir.mkdir(parents=True, exist_ok=True)
            for stale in preview_dir.glob("page-*.png"):
                stale.unlink()
            for index, png in enumerate(pages, start=1):
                (preview_dir / f"page-{index:02d}.png").write_bytes(png)
            print(f"Rendered {language}: {len(pages)} pages to {preview_dir}")
    except Exception as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
