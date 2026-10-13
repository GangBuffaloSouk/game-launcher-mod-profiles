"""Mod profile schema. Validated with pydantic; this is the on-disk contract."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class GameTarget(BaseModel):
    exe: str
    args: list[str] = Field(default_factory=list)
    working_dir: str = ""

    @field_validator("exe")
    @classmethod
    def _exe_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("game.exe must be set")
        return v


class ModEntry(BaseModel):
    name: str
    source: str  # path to archive or loose dir
    kind: Literal["dll", "pak", "script", "asi", "mixed"] = "mixed"
    enabled: bool = True
    load_after: list[str] = Field(default_factory=list)
    sha256: str | None = None
    notes: str = ""


class InjectConfig(BaseModel):
    driver: Literal["native", "manual", "deferred"] = "native"
    delay_ms: int = 1500
    elevate: bool = False


class ModProfile(BaseModel):
    schema_version: int = 2
    name: str
    game: GameTarget
    mods: list[ModEntry] = Field(default_factory=list)
    load_order: Literal["declared", "topological"] = "declared"
    inject: InjectConfig = Field(default_factory=InjectConfig)
    verify_hashes: bool = True
    signature: str | None = None