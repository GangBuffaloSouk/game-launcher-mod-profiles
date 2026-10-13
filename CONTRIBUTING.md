# Contributing to game-launcher-mod-profiles

Thanks for wanting to push patches. This is a hobbyist launcher that manages
per-game mod profiles and drives the inject/launch pipeline. PRs welcome from
the modding community.

## Ground rules

- One feature per PR. No drive-by refactors.
- Every new handler goes in `launcher/ingest/` and must have a matching test in `tests/`.
- Every new output driver goes in `launcher/drivers/` and must declare its `capabilities()`.
- No hardcoded absolute paths. Use `launcher/config/paths.py`.
- No new third-party dependency without a note in the PR description explaining why stdlib won't do.

## Dev setup

```bash
python -m venv .venv
. .venv/Scripts/activate      # Windows
pip install -e ".[dev]"
pytest -q
python -m launcher --dry-run --profile profiles/example.json
```

## Native helpers

C++ injector helpers live under `native/injector/` and are built with CMake.
C# profile-signing helper lives under `native/signer/`. Java mod-metadata
reader lives under `native/metadata_reader/`. All three are optional — the
Python launcher falls back to pure-Python paths when they're absent.

## Style

- `ruff` + `black`, line length 100.
- Type hints required on public functions.
- Logging via `launcher.utils.log` only. No bare `print` outside CLI entry.

## Reporting

Open an issue with: game title, launcher version (`python -m launcher --version`),
profile JSON, and the tail of `logs/launcher.log`.

## Code of conduct

Be normal. Modding is a shared hobby. Don't be a cunt to people shipping
free code on their weekend.