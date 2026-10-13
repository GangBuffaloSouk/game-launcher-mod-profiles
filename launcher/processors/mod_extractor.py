"""Extract mod archives into the mod cache and return the artifact root."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from launcher.config.defaults import MOD_EXTRACT_TIMEOUT_S
from launcher.config.paths import MOD_CACHE_DIR
from launcher.utils.log import get_logger

log = get_logger("launcher.processors.extractor")


class ExtractionError(RuntimeError):
    pass


def _safe_join(root: Path, member: str) -> Path:
    target = (root / member).resolve()
    root_resolved = root.resolve()
    if root_resolved not in target.parents and target != root_resolved:
        raise ExtractionError(f"archive member escapes root: {member}")
    return target


def extract_archive(archive: Path, mod_name: str) -> Path:
    dest = MOD_CACHE_DIR / mod_name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    if not zipfile.is_zipfile(archive):
        # Loose directory or unsupported archive: copy through.
        if archive.is_dir():
            shutil.copytree(archive, dest, dirs_exist_ok=True)
            return dest
        raise ExtractionError(f"unsupported mod source: {archive}")
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            _safe_join(dest, info.filename).parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, _safe_join(dest, info.filename).open("wb") as out:
                shutil.copyfileobj(src, out, length=1 << 16)
    log.info("extracted %s -> %s", archive.name, dest)
    return dest