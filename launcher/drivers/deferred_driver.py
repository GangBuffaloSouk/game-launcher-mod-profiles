"""Deferred driver: queue injections and fire them after a delay on a worker thread."""
from __future__ import annotations

import threading
import time
from pathlib import Path

from launcher.models.job import LaunchJob
from launcher.models.profile import ModProfile
from launcher.utils.log import get_logger

log = get_logger("launcher.drivers.deferred")


class DeferredDriver:
    name = "deferred"

    def __init__(self, inner: object) -> None:
        self._inner = inner

    def capabilities(self) -> dict[str, bool]:
        return {"dll_inject": True, "elevate": False, "deferred": True}

    def launch(self, profile: ModProfile, job: LaunchJob) -> int:
        return self._inner.launch(profile, job)  # type: ignore[attr-defined]

    def inject(self, pid: int, artifacts: list[Path], job: LaunchJob) -> None:
        delay = job.__dict__.get("delay_ms", 1500) / 1000

        def _run() -> None:
            time.sleep(delay)
            self._inner.inject(pid, artifacts, job)  # type: ignore[attr-defined]

        threading.Thread(target=_run, name="deferred-inject", daemon=True).start()