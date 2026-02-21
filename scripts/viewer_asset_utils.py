#!/usr/bin/env python3
"""Helpers for managing repository-local viewer renderer assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Dict, List

ASSET_ARCHIVE_DIR = Path(__file__).resolve().parent / "viewer_asset_archive"
MANIFEST_NAME = "manifest.json"
MANIFEST_VERSION = 1


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def iter_archive_files(archive_dir: Path) -> List[Path]:
    files: List[Path] = []
    for path in archive_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name == MANIFEST_NAME:
            continue
        files.append(path.relative_to(archive_dir))
    files.sort(key=lambda p: p.as_posix())
    return files


def build_manifest(archive_dir: Path = ASSET_ARCHIVE_DIR) -> Dict[str, object]:
    files = []
    for rel_path in iter_archive_files(archive_dir):
        files.append(
            {
                "path": rel_path.as_posix(),
                "sha256": _sha256_file(archive_dir / rel_path),
            }
        )
    return {
        "version": MANIFEST_VERSION,
        "files": files,
    }


def write_manifest(archive_dir: Path = ASSET_ARCHIVE_DIR) -> Path:
    archive_dir = archive_dir.resolve()
    if not archive_dir.exists():
        raise RuntimeError(f"Asset archive directory not found: {archive_dir}")
    manifest = build_manifest(archive_dir)
    manifest_path = archive_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=True, separators=(",", ":"), indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def load_manifest(archive_dir: Path = ASSET_ARCHIVE_DIR) -> Dict[str, object]:
    archive_dir = archive_dir.resolve()
    manifest_path = archive_dir / MANIFEST_NAME
    if not manifest_path.exists():
        raise RuntimeError(f"Missing asset manifest: {manifest_path}")
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise RuntimeError(f"Invalid JSON manifest: {manifest_path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Asset manifest must be a JSON object.")
    if payload.get("version") != MANIFEST_VERSION:
        raise RuntimeError(
            f"Unsupported asset manifest version: {payload.get('version')}. "
            f"Expected {MANIFEST_VERSION}."
        )
    files = payload.get("files")
    if not isinstance(files, list):
        raise RuntimeError("Asset manifest must include a 'files' list.")
    for entry in files:
        if not isinstance(entry, dict):
            raise RuntimeError("Asset manifest entries must be objects.")
        rel_path = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(rel_path, str) or not rel_path:
            raise RuntimeError("Asset manifest entry path must be a non-empty string.")
        if not isinstance(digest, str) or len(digest) != 64:
            raise RuntimeError(f"Asset manifest entry has invalid sha256: {rel_path}")
    return payload


def verify_archive(archive_dir: Path = ASSET_ARCHIVE_DIR) -> Dict[str, object]:
    archive_dir = archive_dir.resolve()
    if not archive_dir.exists():
        raise RuntimeError(f"Asset archive directory not found: {archive_dir}")
    manifest = load_manifest(archive_dir)
    errors: List[str] = []
    for entry in manifest["files"]:
        rel_path = Path(entry["path"])
        full_path = archive_dir / rel_path
        if not full_path.exists():
            errors.append(f"Missing file: {entry['path']}")
            continue
        actual = _sha256_file(full_path)
        expected = entry["sha256"]
        if actual != expected:
            errors.append(
                f"Checksum mismatch for {entry['path']}: expected {expected}, got {actual}"
            )
    if errors:
        detail = "\n".join(f"- {line}" for line in errors)
        raise RuntimeError(f"Asset archive verification failed:\n{detail}")
    return manifest


def copy_archive_to(destination_dir: Path, archive_dir: Path = ASSET_ARCHIVE_DIR) -> None:
    archive_dir = archive_dir.resolve()
    destination_dir = destination_dir.resolve()
    verify_archive(archive_dir)
    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(archive_dir, destination_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage local viewer asset archive metadata.")
    parser.add_argument(
        "--archive-dir",
        default=str(ASSET_ARCHIVE_DIR),
        help=f"Path to archive folder (default: {ASSET_ARCHIVE_DIR})",
    )
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="Recompute and write manifest.json for the archive.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify archive integrity against manifest.json.",
    )
    args = parser.parse_args()

    archive_dir = Path(args.archive_dir).expanduser().resolve()
    if args.write_manifest:
        path = write_manifest(archive_dir)
        print(f"Wrote manifest: {path}")
    if args.verify:
        verify_archive(archive_dir)
        print(f"Verified: {archive_dir}")
    if not args.write_manifest and not args.verify:
        parser.error("No action selected. Use --write-manifest and/or --verify.")


if __name__ == "__main__":
    main()
