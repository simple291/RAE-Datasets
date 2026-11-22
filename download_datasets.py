#!/usr/bin/env python3
"""Download and verify the 21 paper evaluation scenes from GitHub Releases."""
from __future__ import annotations

import argparse
import hashlib
import re
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import stat
import tempfile
import zipfile
import time
from urllib.parse import quote

import requests


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_name(name):
    if not name or Path(name).name != name or "/" in name or "\\" in name or name in (".", ".."):
        raise ValueError(f"Invalid release asset name: {name!r}")
    return name


def safe_target(root, name):
    """Archive members are untrusted input: reject traversal, Windows streams and links."""
    pure = PurePosixPath(name)
    if (pure.is_absolute() or not pure.parts or ".." in pure.parts or "\\" in name
            or any(":" in part for part in pure.parts)):
        raise ValueError(f"Unsafe archive path: {name!r}")
    path = root.joinpath(*pure.parts)
    real_root = root.resolve()
    if not path.resolve().is_relative_to(real_root):
        raise ValueError(f"Archive path escapes output directory: {name!r}")
    for parent in [path, *path.parents]:
        if parent == root.parent:
            break
        if parent.is_symlink() or (hasattr(parent, "is_junction") and parent.is_junction()):
            raise ValueError(f"Output contains link/junction: {parent}")
    return path


def download(url, path, expected=None, retries=5):
    """Range-resume incomplete downloads; never trust a file solely by size."""
    if path.is_symlink():
        raise ValueError(f"Cache file is a symlink: {path}")
    if path.exists() and expected:
        if path.stat().st_size == expected["size"] and sha256_file(path) == expected["sha256"]:
            return path
        raise RuntimeError(f"Existing cache file fails validation: {path}; move it aside and retry.")
    partial = path.with_name(path.name + ".partial")
    if partial.is_symlink():
        raise ValueError(f"Cache partial is a symlink: {partial}")
    for attempt in range(retries):
        offset = partial.stat().st_size if partial.exists() else 0
        if expected and offset > expected["size"]:
            raise RuntimeError(f"Partial download is larger than expected: {partial}")
        if expected and offset == expected["size"]:
            if sha256_file(partial) == expected["sha256"]:
                os.replace(partial, path)
                return path
            partial.unlink()  # Only this script's incomplete cache artifact.
            offset = 0
        headers = {"User-Agent": "RAE-Datasets-Download/2"}
        if offset:
            headers["Range"] = f"bytes={offset}-"
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(30, 180)) as response:
                if response.status_code not in (200, 206):
                    raise RuntimeError(f"Download HTTP {response.status_code}: {path.name}")
                if response.status_code == 206:
                    prefix = f"bytes {offset}-"
                    if not response.headers.get("Content-Range", "").startswith(prefix):
                        raise RuntimeError(f"Unexpected range response for {path.name}")
                    mode = "ab"
                else:
                    mode = "wb"
                    offset = 0
                downloaded = offset
                last_print = time.monotonic()
                with open(partial, mode) as stream:
                    for block in response.iter_content(4 * 1024 * 1024):
                        if not block:
                            continue
                        downloaded += len(block)
                        if expected and downloaded > expected["size"]:
                            raise RuntimeError(f"Remote download exceeds expected size: {path.name}")
                        stream.write(block)
                        if time.monotonic() - last_print >= 30:
                            print(f"{path.name}: {downloaded / 2**30:.3f} GiB", flush=True)
                            last_print = time.monotonic()
            if expected and (partial.stat().st_size != expected["size"] or sha256_file(partial) != expected["sha256"]):
                raise RuntimeError(f"SHA256/size validation failed: {path.name}")
            os.replace(partial, path)
            return path
        except (requests.RequestException, RuntimeError) as exc:
            if attempt + 1 == retries:
                if isinstance(exc, requests.RequestException):
                    raise RuntimeError(f"Download failed: {path.name} ({type(exc).__name__})") from None
                raise
            print(f"Retrying {path.name} ({attempt + 1}/{retries})", flush=True)
            time.sleep(min(5 * 2**attempt, 60))
    raise AssertionError("unreachable")


DEFAULT_TAG = "paper-test21-v1"


def restore(bundle, output, scene):
    """Install atomically, or verify an existing installation without replacing files."""
    output.mkdir(parents=True, exist_ok=True)
    final = safe_target(output, scene)
    existing = final.exists()
    with tempfile.TemporaryDirectory(prefix=".rae-restore-", dir=output) as scratch:
        root = output if existing else Path(scratch)
        seen = set()
        with zipfile.ZipFile(bundle) as archive:
            for info in archive.infolist():
                parts = PurePosixPath(info.filename).parts
                dest = safe_target(root, info.filename)
                if not parts or parts[0] != scene or info.filename.casefold() in seen:
                    raise ValueError(f"Unexpected or duplicate scene entry: {info.filename}")
                seen.add(info.filename.casefold())
                if stat.S_ISLNK(info.external_attr >> 16):
                    raise ValueError(f"Archive contains a link: {info.filename}")
                if info.is_dir():
                    if existing and not dest.is_dir():
                        raise ValueError(f"Missing directory in installed scene: {dest}")
                    dest.mkdir(parents=True, exist_ok=True)
                    continue
                with archive.open(info) as src:
                    if existing:
                        if not dest.is_file() or dest.stat().st_size != info.file_size:
                            raise ValueError(f"Installed scene is incomplete or changed: {dest}")
                        with dest.open("rb") as other:
                            for block in iter(lambda: src.read(1 << 20), b""):
                                if other.read(len(block)) != block:
                                    raise ValueError(f"Installed scene differs: {dest}")
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        with dest.open("xb") as out:
                            shutil.copyfileobj(src, out, 1 << 20)
        if not (root / scene / "adaptation_manifest.json").is_file():
            raise ValueError(f"Missing camera and frame manifest in {scene}")
        if not existing:
            (root / scene).rename(final)
    print(f"Verified {scene}: {final}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="simple291/RAE-Datasets")
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument("--output", type=Path, default=Path("Datasets"))
    parser.add_argument("--cache", type=Path, default=Path(".rae-datasets-cache"))
    parser.add_argument("--manifest", type=Path, help="Override datasets.json")
    parser.add_argument("--dataset", action="append", help="Scene ID, name or source family; repeat to select several")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--download-only", action="store_true")
    args = parser.parse_args(argv)
    manifest = args.manifest or Path(__file__).resolve().with_name("datasets.json")
    catalog = json.loads(manifest.read_text(encoding="utf-8-sig"))
    scenes = catalog["datasets"]
    if len(scenes) != 21 or len({s["id"] for s in scenes}) != 21:
        raise ValueError("Expected 21 unique paper evaluation scenes")
    wanted = {x.casefold() for x in args.dataset or []}
    selected, found = [], set()
    for row in scenes:
        if not re.fullmatch(r"[a-z0-9-]+", row["id"]) or row["archive"] != row["id"] + ".zip":
            raise ValueError("Invalid archive or scene name")
        if not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) or row["bytes"] <= 0:
            raise ValueError(f"Invalid archive checksum for {row['id']}")
        aliases = {row[k].casefold() for k in ("id", "name", "source_family")}
        if not wanted or wanted & aliases:
            selected.append(row)
            found.update(wanted & aliases)
    if wanted - found:
        raise ValueError("Unknown datasets: " + ", ".join(sorted(wanted - found)))
    if args.list:
        for row in selected:
            print(f"{row['id']:26} {row['name']}  ({row['bytes'] / 2**20:.1f} MiB)")
        return
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo):
        raise ValueError("Expected --repo owner/name")
    base = f"https://github.com/{args.repo}/releases/download/{quote(args.tag, safe='')}"
    args.cache.mkdir(parents=True, exist_ok=True)
    for row in selected:
        name = asset_name(row["archive"])
        bundle = download(base + "/" + quote(name), args.cache / name,
                          {"size": row["bytes"], "sha256": row["sha256"]})
        if not args.download_only:
            restore(bundle, args.output.resolve(), row["id"])


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        sys.exit(f"ERROR: {exc}")
