"""Filesystem watcher that emits ingest events when mod sources change."""
from __future__ import annotations

import queue
import threading
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from launcher.utils.log import get_logger

log = get_logger("launcher.ingest.watch")


class _ModSourceHandler(FileSystemEventHandler):
    def __init__(self, sink: "queue.Queue[Path]") -> None:
        self._sink = sink

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        self._sink.put(Path(event.src_path))


class ModSourceWatcher:
    """Watches a mod source directory. Call .start() and drain .events."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.events: queue.Queue[Path] = queue.Queue()
        self._observer = Observer()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._observer.schedule(_ModSourceHandler(self.events), str(self.root), recursive=True)
        self._observer.start()
        log.info("watching mod source %s", self.root)

    def stop(self) -> None:
        self._observer.stop()
        self._observer.join(timeout=5)