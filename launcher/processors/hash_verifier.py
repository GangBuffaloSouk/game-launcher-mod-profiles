"""SHA-256 verification of extracted mod artifacts against profile manifests."""
from __future__ import annotations

import hashlib
from pathlib import Path

_CHUNK = 1 << 20  # 1 MiB


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def verify(path: Path, expected: str | None, *, allow_unverified: bool) -> bool:
    if not expected:
        return allow_unverified
    actual = sha256_file(path)
    return actual.lower() == expected.lower()