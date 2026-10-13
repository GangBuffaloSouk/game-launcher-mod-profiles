"""Launcher pipeline: ingest -> process -> drive. The whole launcher is this."""
from __future__ import annotations

from pathlib import Path

from launcher.config.paths import ensure_runtime_dirs
from launcher.core.registry import build_driver
from launcher.ingest.archive_scanner import scan_source
from launcher.ingest.profile_loader import ProfileLoadError, load_profile
from launcher.models.job import JobStage, LaunchJob
from launcher.processors.load_order import LoadOrderCycle, resolve
from launcher.processors.mod_extractor import extract_archive
from launcher.utils.log import get_logger

log = get_logger("launcher.core.pipeline")


class LauncherPipeline:
    def __init__(self, profile_path: Path, *, dry_run: bool = False, allow_unverified: bool = False) -> None:
        self.profile_path = profile_path
        self.dry_run = dry_run
        self.allow_unverified = allow_unverified

    def run(self) -> int:
        ensure_runtime_dirs()
        job = LaunchJob(profile_path=self.profile_path)
        try:
            profile = load_profile(self.profile_path)
        except ProfileLoadError as exc:
            log.error("%s", exc)
            return 2
        job.profile_name = profile.name

        try:
            ordered = resolve(profile.mods, profile.load_order)
        except LoadOrderCycle as exc:
            log.error("load order failed: %s", exc)
            job.fail(str(exc))
            return 3

        artifacts: list[Path] = []
        for mod in ordered:
            src = Path(mod.source)
            for scanned in scan_source(src):
                if scanned.kind in {"dll", "script"}:
                    artifacts.append(scanned.path)
            if not self.dry_run and src.is_file():
                try:
                    extract_archive(src, mod.name)
                except Exception as exc:  # noqa: BLE001
                    job.fail(f"extract failed for {mod.name}: {exc}")

        if self.dry_run:
            log.info("dry-run: %d artifacts resolved for %s", len(artifacts), profile.name)
            return 0

        driver = build_driver(profile.inject.driver)
        pid = driver.launch(profile, job)
        job.stage = JobStage.DRIVE
        driver.inject(pid, artifacts, job)
        job.stage = JobStage.DONE if not job.errors else JobStage.FAILED
        return 0 if job.stage == JobStage.DONE else 1