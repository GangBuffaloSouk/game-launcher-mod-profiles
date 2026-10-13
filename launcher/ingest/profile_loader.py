"""Load and validate a mod profile JSON from disk."""
from __future__ import annotations

import json
from pathlib import Path

from launcher.models.profile import ModProfile


class ProfileLoadError(RuntimeError):
    pass


def load_profile(path: Path) -> ModProfile:
    if not path.is_file():
        raise ProfileLoadError(f"profile not found: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProfileLoadError(f"profile {path.name} is not valid JSON: {exc}") from exc
    try:
        return ModProfile.model_validate(raw)
    except Exception as exc:  # pydantic ValidationError
        raise ProfileLoadError(f"profile {path.name} failed schema validation: {exc}") from exc