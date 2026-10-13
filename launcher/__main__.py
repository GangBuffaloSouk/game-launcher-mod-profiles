"""CLI bootstrap. Parses args, wires the pipeline, hands off to the runner."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from launcher import __version__
from launcher.config.paths import default_profile_dir
from launcher.core.pipeline import LauncherPipeline
from launcher.utils.log import get_logger

log = get_logger("launcher.cli")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="glmp",
        description="Launch a game with a mod profile applied.",
    )
    p.add_argument("--profile", type=Path, help="Path to a mod profile JSON.")
    p.add_argument("--profile-dir", type=Path, default=default_profile_dir())
    p.add_argument("--list", action="store_true", help="List known profiles and exit.")
    p.add_argument("--dry-run", action="store_true", help="Resolve and validate only.")
    p.add_argument("--allow-unverified-mod", action="store_true",
                   help="Skip hash verification of mod artifacts.")
    p.add_argument("--verbose", "-v", action="count", default=0)
    p.add_argument("--version", action="version", version=f"glmp {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.list:
        for profile in sorted(args.profile_dir.glob("*.json")):
            print(profile.stem)
        return 0
    if not args.profile:
        log.error("no --profile given; use --list to see available profiles")
        return 2
    pipeline = LauncherPipeline(
        profile_path=args.profile,
        dry_run=args.dry_run,
        allow_unverified=args.allow_unverified_mod,
    )
    return pipeline.run()


if __name__ == "__main__":
    sys.exit(main())