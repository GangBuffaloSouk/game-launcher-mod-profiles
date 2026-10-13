"""Canonical filesystem locations. Every path in the launcher routes through here."""
from __future__ import annotations

import os
from pathlib import Path


def _app_root() -> Path:
    override = os.environ.get("GLMP_HOME")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".glmp"


APP_ROOT: Path = _app_root()
MOD_CACHE_DIR: Path = APP_ROOT / "mod_cache"
LOG_DIR: Path = APP_ROOT / "logs"
STATE_DB: Path = APP_ROOT / "launcher_state.db"
INJECTOR_TRACE_DIR: Path = APP_ROOT / "injector_traces"


def default_profile_dir() -> Path:
    return APP_ROOT / "profiles"


def ensure_runtime_dirs() -> None:
    for d in (APP_ROOT, MOD_CACHE_DIR, LOG_DIR, INJECTOR_TRACE_DIR, default_profile_dir()):
        d.mkdir(parents=True, exist_ok=True)