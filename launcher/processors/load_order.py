"""Resolve mod load order. Declared order or topological sort on load_after."""
from __future__ import annotations

from launcher.models.profile import ModEntry


class LoadOrderCycle(RuntimeError):
    pass


def resolve(entries: list[ModEntry], mode: str) -> list[ModEntry]:
    enabled = [m for m in entries if m.enabled]
    if mode == "declared":
        return enabled

    by_name = {m.name: m for m in enabled}
    ordered: list[ModEntry] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            raise LoadOrderCycle(f"cycle detected at mod: {name}")
        visiting.add(name)
        mod = by_name.get(name)
        if mod is None:
            visiting.discard(name)
            return
        for dep in mod.load_after:
            visit(dep)
        visiting.discard(name)
        visited.add(name)
        ordered.append(mod)

    for m in enabled:
        visit(m.name)
    return ordered