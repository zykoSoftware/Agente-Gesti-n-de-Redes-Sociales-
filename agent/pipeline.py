"""Orquestador: del perfil de empresa a un carrusel en PNG, listo para revisar."""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from . import brand as brand_mod
from . import copywriter, designer, renderer, store


def analyze_profile(profile_id: str) -> dict:
    """Analiza la web + logo de un perfil y guarda su Brand Kit."""
    profile = store.get_profile(profile_id)
    if not profile:
        raise ValueError("Perfil no encontrado")

    logo_path = None
    if profile.get("logo"):
        logo_path = str(store.profile_dir(profile_id) / profile["logo"])

    kit = brand_mod.analyze(
        name=profile["name"],
        website=profile.get("website", ""),
        logo_path=logo_path,
        sector=profile.get("sector", ""),
    )
    store.update_profile(profile_id, brand=kit)
    return kit


def generate_carousel(profile_id: str, pillar: str = "problema_solucion") -> dict:
    """Genera un carrusel completo (copy + diseño + render) para un perfil."""
    profile = store.get_profile(profile_id)
    if not profile:
        raise ValueError("Perfil no encontrado")

    brand = profile.get("brand") or brand_mod.brand_or_default(
        profile["name"], profile.get("sector", "")
    )

    logo_uri = None
    if profile.get("logo"):
        logo_uri = renderer.logo_data_uri(
            store.profile_dir(profile_id) / profile["logo"]
        )

    script = copywriter.generate(
        pillar, profile["name"], profile.get("sector", ""), profile.get("handle", "")
    )
    slides_html = designer.build_carousel(script, profile["name"], brand, logo_uri)

    post_id = f"{pillar}-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"
    out_dir = store.profile_dir(profile_id) / "posts" / post_id
    out_dir.mkdir(parents=True, exist_ok=True)

    slide_files = []
    for i, html in enumerate(slides_html, start=1):
        out = out_dir / f"slide{i}.png"
        renderer.render_html_to_png(html, out)
        slide_files.append(f"slide{i}.png")

    post = {
        "id": post_id,
        "pillar": pillar,
        "pillar_label": copywriter.PILLARS.get(pillar, pillar),
        "slides": slide_files,
        "created": time.time(),
    }
    (out_dir / "post.json").write_text(
        json.dumps(post, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return post


def list_posts(profile_id: str) -> list[dict]:
    """Lista los carruseles generados de un perfil (más recientes primero)."""
    posts_dir = store.profile_dir(profile_id) / "posts"
    posts = []
    for meta in posts_dir.glob("*/post.json"):
        try:
            posts.append(json.loads(meta.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return sorted(posts, key=lambda p: p.get("created", 0), reverse=True)
