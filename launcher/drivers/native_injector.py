"""Native driver: spawn the game, then inject DLL/ASI artifacts via the C++ helper."""
from __future__ import annotations

import ctypes
import subprocess
import time
from pathlib import Path

from launcher.config.defaults import INJECT_RETRY_ATTEMPTS, INJECT_RETRY_BACKOFF_MS
from launcher.models.job import LaunchJob
from launcher.models.profile import ModProfile
from launcher.utils.log import get_logger

log = get_logger("launcher.drivers.native")


class NativeInjector:
    name = "native"

    def __init__(self, helper_exe: Path | None = None) -> None:
        self.helper_exe = helper_exe

    def capabilities(self) -> dict[str, bool]:
        return {"dll_inject": True, "elevate": True, "deferred": False}

    def launch(self, profile: ModProfile, job: LaunchJob) -> int:
        exe = Path(profile.game.exe)
        cwd = profile.game.working_dir or str(exe.parent)
        log.info("spawning game: %s", exe)
        proc = subprocess.Popen([str(exe), *profile.game.args], cwd=cwd)
        job.pid = proc.pid
        return proc.pid

    def inject(self, pid: int, artifacts: list[Path], job: LaunchJob) -> None:
        if self.helper_exe is None or not self.helper_exe.exists():
            log.warning("native injector helper missing; skipping injection")
            return
        for artifact in artifacts:
            self._inject_one(pid, artifact, job)

    def _inject_one(self, pid: int, artifact: Path, job: LaunchJob) -> None:
        last_err: str | None = None
        for attempt in range(1, INJECT_RETRY_ATTEMPTS + 1):
            proc = subprocess.run(
                [str(self.helper_exe), "--pid", str(pid), "--dll", str(artifact)],
                capture_output=True, text=True,
            )
            if proc.returncode == 0:
                log.info("injected %s into pid %d", artifact.name, pid)
                return
            last_err = proc.stderr.strip() or f"exit {proc.returncode}"
            log.warning("inject attempt %d failed for %s: %s", attempt, artifact.name, last_err)
            time.sleep(INJECT_RETRY_BACKOFF_MS / 1000)
        job.fail(f"injection failed for {artifact.name}: {last_err}")