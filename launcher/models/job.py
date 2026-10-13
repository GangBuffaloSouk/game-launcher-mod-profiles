"""Job model — the unit of work the pipeline carries end to end."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class JobStage(str, Enum):
    INGEST = "ingest"
    PROCESS = "process"
    DRIVE = "drive"
    DONE = "done"
    FAILED = "failed"


@dataclass(slots=True)
class LaunchJob:
    profile_path: Path
    profile_name: str = ""
    stage: JobStage = JobStage.INGEST
    resolved_mods: list[Path] = field(default_factory=list)
    extracted_root: Path | None = None
    pid: int | None = None
    errors: list[str] = field(default_factory=list)

    def fail(self, reason: str) -> None:
        self.errors.append(reason)
        self.stage = JobStage.FAILED