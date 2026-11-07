#!/usr/bin/env python3
"""Save a reviewed paper version without overwriting an existing snapshot."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
PAPER_FILES = (
    "dimensional_shift.typ", "dimensional_shift.pdf", "dimensional_shift.md",
    "dimensional_shift_en.typ", "dimensional_shift_en.pdf", "dimensional_shift_en.md",
    "paper_config.json", "equations.json",
)


def file_info(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def describe_file(name):
    """Describe language and format without relying on translated content."""
    path = Path(name)
    language = None
    if path.name.startswith("dimensional_shift"):
        language = "en" if path.stem.endswith("_en") else "ja"
    formats = {".typ": "typst", ".pdf": "pdf", ".md": "markdown", ".json": "json"}
    return {"language": language, "format": formats[path.suffix]}


def save_snapshot(version, summary):
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?", version):
        raise ValueError("Version must look like v0.2.0 or v0.2.0-draft.1")
    if not summary.strip():
        raise ValueError("Summary must not be empty")

    current = ROOT / "output" / "current"
    history = ROOT / "output" / "history"
    original = ROOT / "origin" / "dimensional_shift_01.txt"
    reference = ROOT / "output" / "reference" / "dimensional_shift_01_original.txt"
    discussion_map = ROOT / "output" / "discussion" / "version_map.json"
    for path in [*(current / name for name in PAPER_FILES), original, reference]:
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Required nonempty file is missing: {path}")
    config = json.loads((current / "paper_config.json").read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("paper_config.json must contain an object")
    if config.get("version") != version:
        raise ValueError(f"Requested version {version} does not match paper_config.json")
    json.loads((current / "equations.json").read_text(encoding="utf-8"))
    for name in PAPER_FILES:
        if name.endswith(".pdf"):
            with (current / name).open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    raise ValueError(f"The current PDF does not have a PDF header: {name}")
    sources = [(current / name, name) for name in PAPER_FILES]
    if discussion_map.exists():
        json.loads(discussion_map.read_text(encoding="utf-8"))
        sources.append((discussion_map, "discussion/version_map.json"))
    original_info = file_info(original)
    if file_info(reference) != original_info:
        raise ValueError("The original memo and its reference copy differ")

    history.mkdir(parents=True, exist_ok=True)
    target = history / version
    if target.exists():
        raise FileExistsError(f"Snapshot already exists; choose a new version: {target}")
    lock = history / f".{version}.lock"
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    staging = None
    try:
        os.close(lock_fd)
        if target.exists():
            raise FileExistsError(f"Snapshot already exists: {target}")
        staging = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=history))
        entries = []
        source_info = {str(source): file_info(source) for source, _ in sources}
        for source, name in sources:
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            before = source_info[str(source)]
            shutil.copy2(source, destination)
            copied = file_info(destination)
            if copied != before or file_info(source) != before:
                raise RuntimeError(f"Source changed during snapshot creation: {source}")
            entries.append({"path": name, **describe_file(name), **copied})
        for source, _ in sources:
            if file_info(source) != source_info[str(source)]:
                raise RuntimeError(f"Source changed during snapshot creation: {source}")
        metadata = {
            "schema_version": 2,
            "version": version,
            "git_tag": version,
            "paper_date": config.get("date"),
            "created_at": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"),
            "timezone": "Asia/Tokyo",
            "summary": summary.strip(),
            "authors": config.get("authors", ["木村祐太", "GPT-6 Astra（AI）"]),
            "languages": ["ja", "en"],
            "reader_formats": ["pdf", "markdown"],
            "rebuild": "Check out the corresponding Git tag to restore shared build scripts and styles.",
            "files": entries,
            "original_memo": {
                "path": "origin/dimensional_shift_01.txt",
                "reference_copy": "output/reference/dimensional_shift_01_original.txt",
                **original_info,
            },
        }
        (staging / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        if target.exists():
            raise FileExistsError(f"Snapshot already exists: {target}")
        staging.rename(target)
        staging = None
        return target
    finally:
        if staging is not None:
            shutil.rmtree(staging)
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="New version, for example v0.2.0")
    parser.add_argument("--summary", required=True, help="Brief description of the change")
    args = parser.parse_args()
    try:
        result = save_snapshot(args.version, args.summary)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Snapshot failed: {error}", file=sys.stderr)
        return 1
    print(f"Saved {result.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
