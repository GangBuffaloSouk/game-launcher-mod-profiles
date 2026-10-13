"""Default profile values and pipeline tuning constants."""
from __future__ import annotations

DEFAULT_PROFILE = {
    "schema_version": 2,
    "game": {"exe": "", "args": [], "working_dir": ""},
    "mods": [],
    "load_order": "declared",
    "inject": {"driver": "native", "delay_ms": 1500, "elevate": False},
    "verify_hashes": True,
}

# Pipeline tuning
MAX_PARALLEL_MOD_EXTRACTS = 4
MOD_EXTRACT_TIMEOUT_S = 90
INJECT_RETRY_ATTEMPTS = 3
INJECT_RETRY_BACKOFF_MS = 400