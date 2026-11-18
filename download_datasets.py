#!/usr/bin/env python3
"""Download and restore RAE datasets from verified split TAR release assets.

Python 3.9+ and requests are required: python -m pip install requests
Example: python download_datasets.py --output Datasets
Example: python download_datasets.py --dataset CO3D --dataset 蜂蜜
Downloads resume automatically. TAR parts are retained in the cache.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tarfile
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
    """TAR is untrusted input: reject traversal, Windows streams and links."""
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
        headers = {"User-Agent": "RAE-Datasets-Download/1"}
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


class PartsReader(io.RawIOBase):
    """A seek-free byte stream spanning several individually verified TAR parts."""
    def __init__(self, paths):
        super().__init__()
        self.paths = iter(paths)
        self.current = None

    def readable(self):
        return True

    def readinto(self, buffer):
        while True:
            if self.current is None:
                try:
                    self.current = open(next(self.paths), "rb")
                except StopIteration:
                    return 0
            count = self.current.readinto(buffer)
            if count:
                return count
            self.current.close()
            self.current = None

    def close(self):
        if self.current is not None:
            self.current.close()
        super().close()


def extract_verified(parts, file_manifest, output, dataset):
    files = file_manifest["files"]
    expected = {item["path"]: item for item in files}
    if len(expected) != len(files):
        raise ValueError("Manifest contains duplicate file paths")
    for name in expected:
        if PurePosixPath(name).parts[0] != dataset:
            raise ValueError("Manifest path belongs to another dataset")
        safe_target(output, name)
    allowed_dirs = set(file_manifest.get("directories", []))
    found = set()
    with PartsReader(parts) as raw, io.BufferedReader(raw, buffer_size=4 * 1024 * 1024) as joined:
        with tarfile.open(fileobj=joined, mode="r|") as archive:
            for member in archive:
                name = member.name.rstrip("/")
                target = safe_target(output, name)
                if PurePosixPath(name).parts[0] != dataset:
                    raise ValueError(f"Unexpected archive dataset: {name}")
                if member.isdir():
                    if name not in allowed_dirs:
                        raise ValueError(f"Unexpected directory: {name}")
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile():
                    raise ValueError(f"Only ordinary files and directories are accepted: {name}")
                if name not in expected or name in found:
                    raise ValueError(f"Unexpected or duplicate archive file: {name}")
                item = expected[name]
                if member.size != item["size"]:
                    raise ValueError(f"TAR file size mismatch: {name}")
                found.add(name)
                if target.exists():
                    if target.is_file() and target.stat().st_size == item["size"] and sha256_file(target) == item["sha256"]:
                        continue
                    raise RuntimeError(f"Existing output differs; move it aside before retrying: {target}")
                target.parent.mkdir(parents=True, exist_ok=True)
                temp = target.with_name(target.name + ".rae-extract.partial")
                if temp.exists() or temp.is_symlink():
                    raise RuntimeError(f"Incomplete extraction exists; inspect and remove it before retrying: {temp}")
                digest = hashlib.sha256()
                count = 0
                source = archive.extractfile(member)
                try:
                    with open(temp, "xb") as destination:
                        for block in iter(lambda: source.read(4 * 1024 * 1024), b""):
                            destination.write(block)
                            digest.update(block)
                            count += len(block)
                    if count != item["size"] or digest.hexdigest() != item["sha256"]:
                        raise RuntimeError(f"Extracted SHA256 mismatch: {name}")
                    os.replace(temp, target)
                    if "mtime_ns" in item:
                        os.utime(target, ns=(item["mtime_ns"], item["mtime_ns"]))
                except Exception:
                    if temp.is_file() and not temp.is_symlink():
                        temp.unlink()
                    raise
                finally:
                    source.close()
    if found != set(expected):
        raise RuntimeError(f"Archive omitted {len(set(expected) - found)} expected files")
    for name in allowed_dirs:
        safe_target(output, name).mkdir(parents=True, exist_ok=True)
    print(f"Verified and restored {dataset}: {len(files):,} files", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="simple291/RAE-Datasets")
    parser.add_argument("--tag", default="datasets-2026-11-18")
    parser.add_argument("--output", type=Path, default=Path("Datasets"))
    parser.add_argument("--cache", type=Path, default=Path(".rae-datasets-cache"))
    parser.add_argument("--dataset", action="append", help="Dataset name or ASCII alias; repeat to select several. Default: all")
    parser.add_argument("--download-only", action="store_true")
    parser.add_argument("--list", action="store_true", help="Print datasets without downloading parts")
    parser.add_argument("--manifest", type=Path, help="Use an already downloaded packages.json")
    args = parser.parse_args(argv)
    args.cache.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    base = f"https://github.com/{args.repo}/releases/download/{quote(args.tag, safe='')}"
    if args.manifest:
        manifest_path = args.manifest
    else:
        # Refresh the small manifest from the selected immutable release tag.
        manifest_path = download(base + "/packages.json", args.cache / "packages.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if manifest.get("schema_version") != 1 or not manifest.get("complete"):
        raise ValueError("Unsupported or unfinished packages manifest")
    packages = manifest["packages"]
    if args.list:
        for package in packages:
            print(f"{package['dataset']} ({package['alias']}): {package['file_count']:,} files, {package['source_bytes'] / 2**30:.3f} GiB")
        return
    if args.dataset:
        wanted = set(args.dataset)
        selected = [p for p in packages if p["dataset"] in wanted or p["alias"] in wanted]
        known = {name for p in selected for name in (p["dataset"], p["alias"])}
        if wanted - known:
            raise ValueError(f"Unknown datasets: {', '.join(sorted(wanted - known))}")
        packages = selected
    for package in packages:
        print(f"Preparing {package['dataset']}", flush=True)
        metadata = package["file_manifest"]
        name = asset_name(metadata["name"])
        file_manifest_path = download(base + "/" + quote(name), args.cache / name, metadata)
        file_manifest = json.loads(file_manifest_path.read_text(encoding="utf-8-sig"))
        if file_manifest.get("dataset") != package["dataset"]:
            raise ValueError("File manifest dataset mismatch")
        paths = []
        for part in package["parts"]:
            name = asset_name(part["name"])
            paths.append(download(base + "/" + quote(name), args.cache / name, part))
        if not args.download_only:
            extract_verified(paths, file_manifest, args.output.resolve(), package["dataset"])
    print("All selected datasets completed.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr, flush=True)
        sys.exit(1)
