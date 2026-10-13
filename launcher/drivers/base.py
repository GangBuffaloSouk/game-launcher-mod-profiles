"""Driver protocol. Every output driver implements launch() and inject()."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from launcher.models.job import LaunchJob
from launcher.models.profile import ModProfile


@runtime_checkable
class OutputDriver(Protocol):
    name: str

    def capabilities(self) -> dict[str, bool]: ...

    def launch(self, profile: ModProfile, job: LaunchJob) -> int: ...

    def inject(self, pid: int, artifacts: list[Path], job: LaunchJob) -> None: ...