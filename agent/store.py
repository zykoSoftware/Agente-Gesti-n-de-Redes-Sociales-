"""Persistencia sencilla de perfiles de empresa en JSON."""
from __future__ import annotations

import json
import re
import time
import uuid
from pathlib import Path

from . import config


def _load() -> list[dict]:
    if not config.PROFILES_FILE.exists():
        return []
    try:
        return json.loads(config.PROFILES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _save(profiles: list[dict]) -> None:
    config.ensure_dirs()
    config.PROFILES_FILE.write_text(
        json.dumps(profiles, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "empresa"


def list_profiles() -> list[dict]:
    return sorted(_load(), key=lambda p: p.get("created", 0), reverse=True)


def get_profile(profile_id: str) -> dict | None:
    return next((p for p in _load() if p["id"] == profile_id), None)


def profile_dir(profile_id: str) -> Path:
    d = config.DATA_DIR / "profiles" / profile_id
    (d / "posts").mkdir(parents=True, exist_ok=True)
    return d


def create_profile(name: str, website: str = "", sector: str = "",
                   handle: str = "") -> dict:
    profiles = _load()
    profile = {
        "id": f"{slugify(name)}-{uuid.uuid4().hex[:6]}",
        "name": name.strip(),
        "website": website.strip(),
        "sector": sector.strip(),
        "handle": handle.strip().lstrip("@"),
        "logo": None,          # ruta relativa al directorio del perfil
        "brand": None,         # Brand Kit resultante del análisis
        "created": time.time(),
    }
    profiles.append(profile)
    _save(profiles)
    profile_dir(profile["id"])
    return profile


def update_profile(profile_id: str, **fields) -> dict | None:
    profiles = _load()
    for p in profiles:
        if p["id"] == profile_id:
            p.update(fields)
            _save(profiles)
            return p
    return None


def delete_profile(profile_id: str) -> None:
    _save([p for p in _load() if p["id"] != profile_id])
