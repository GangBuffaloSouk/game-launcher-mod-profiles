"""Reject mod paths that try to escape their profile mod root."""
from __future__ import annotations

from pathlib import Path


class PathEscape(RuntimeError):
    pass


def assert_within(child: Path, root: Path) -> Path:
    c = child.resolve()
    r = root.resolve()
    if r != c and r not in c.parents:
        raise PathEscape(f"{child} escapes mod root {root}")
    return c