"""Driver registry — maps profile.inject.driver to a concrete OutputDriver."""
from __future__ import annotations

from pathlib import Path

from launcher.config.paths import APP_ROOT
from launcher.drivers.base import OutputDriver
from launcher.drivers.deferred_driver import DeferredDriver
from launcher.drivers.native_injector import NativeInjector
from launcher.utils.log import get_logger

log = get_logger("launcher.core.registry")

_HELPER = APP_ROOT / "bin" / "glmp_injector.exe"


def build_driver(kind: str) -> OutputDriver:
    native = NativeInjector(helper_exe=_HELPER if _HELPER.exists() else None)
    if kind == "native":
        return native
    if kind == "deferred":
        return DeferredDriver(native)
    if kind == "manual":
        log.info("manual driver selected: injections must be applied by the user")
        return native
    raise ValueError(f"unknown driver: {kind}")