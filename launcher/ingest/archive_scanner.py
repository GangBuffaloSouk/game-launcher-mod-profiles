"""Scan mod source directories/archives and enumerate candidate mod entries."""
from __future__ import annotations

import zipfile
from dataclasses import dataclass
from pathlib import Path

_MOD_EXTS = {".dll", ".asi", ".pak", ".esp", ".esm", ".bsa", ".lua", ".cs", ".json"}


@dataclass(slots=True)
class ScannedMod:
    name: str
    path: Path
    kind: str
    size_bytes: int


def _classify(suffix: str) -> str:
    s = suffix.lower()
    if s in {".dll", ".asi"}:
        return "dll"
    if s in {".pak", ".bsa"}:
        return "pak"
    if s in {".lua", ".cs"}:
        return "script"
    if s in {".esp", ".esm"}:
        return "plugin"
    return "mixed"


def scan_source(source: Path) -> list[ScannedMod]:
    if not source.exists():
        return []
    found: list[ScannedMod] = []
    if source.is_dir():
        for p in source.rglob("*"):
            if p.is_file() and p.suffix.lower() in _MOD_EXTS:
                found.append(ScannedMod(p.name, p, _classify(p.suffix), p.stat().st_size))
    elif zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                suffix = Path(info.filename).suffix
                if suffix.lower() in _MOD_EXTS:
                    found.append(ScannedMod(Path(info.filename).name, source, _classify(suffix), info.file_size))
    return found