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
PAPER_FILES = ("dimensional_shift.typ", "dimensional_shift.pdf")


def file_info(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def save_snapshot(version, summary):
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?", version):
        raise ValueError("Version must look like v0.1.0 or v0.1.0-draft.1")
    if not summary.strip():
        raise ValueError("Summary must not be empty")

    current = ROOT / "output" / "current"
    history = ROOT / "output" / "history"
    original = ROOT / "origin" / "dimensional_shift_01.txt"
    reference = ROOT / "output" / "reference" / "dimensional_shift_01_original.txt"
    for path in [*(current / name for name in PAPER_FILES), original, reference]:
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"Required nonempty file is missing: {path}")
    with (current / "dimensional_shift.pdf").open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ValueError("The current PDF does not have a PDF header")
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
        for name in PAPER_FILES:
            source = current / name
            destination = staging / name
            before = file_info(source)
            shutil.copy2(source, destination)
            copied = file_info(destination)
            if copied != before or file_info(source) != before:
                raise RuntimeError(f"Source changed during snapshot creation: {source}")
            entries.append({"path": name, **copied})
        metadata = {
            "schema_version": 1,
            "version": version,
            "created_at": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"),
            "timezone": "Asia/Tokyo",
            "summary": summary.strip(),
            "authors": ["木村祐太", "GPT-6 Astra（AI）"],
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
    parser.add_argument("--version", required=True, help="New version, for example v0.1.0")
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
