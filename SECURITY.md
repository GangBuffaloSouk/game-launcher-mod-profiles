# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | yes       |
| < 0.5   | no        |

## What this launcher touches

`game-launcher-mod-profiles` reads and writes:

- `profiles/*.json` — user-authored mod profile definitions
- `mod_cache/` — extracted mod archives (DLLs, PAK files, loose scripts)
- `launcher_state.db` — SQLite index of installed mods and their hashes
- the target game process, via the injector driver, when a profile is launched

It does **not** phone home. There is no telemetry, no auto-update channel,
and no network listener. If a build you downloaded does any of those, it is
not ours.

## Threat model

The realistic risks are:

1. **Malicious mod archives.** A profile can point at a third-party mod
   archive. We hash every extracted artifact against the manifest and refuse
   to load mismatches unless `--allow-unverified-mod` is passed.
2. **DLL sideloading via mod paths.** Mod directories are added to the
   game's search order by some drivers. We sanitize mod paths and reject
   paths containing `..` or absolute roots outside the profile's mod root.
3. **Tampered profiles.** Profiles can be signed by the C# helper. The
   launcher verifies signatures when `profile.signature` is present.

## Reporting a vulnerability

Email `security@game-launcher-mod-profiles.dev` with a PoC. Do not open a
public issue for anything that lets a profile escape its mod root or run
unsigned code with launcher privileges. We'll acknowledge within 72h.

## Out of scope

- Anti-cheat detection of the injector itself. That's a cat-and-mouse game,
  not a vulnerability in this repo.
- Users running profiles from untrusted sources. Verify your mods.