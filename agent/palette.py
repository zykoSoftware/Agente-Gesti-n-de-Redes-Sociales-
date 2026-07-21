"""Extracción y construcción de paletas de color para el Brand Kit.

Convierte los colores del logo y de la web en una paleta lista para diseñar:
color de acento, fondo, texto y tonos de apoyo, con contraste garantizado.
"""
from __future__ import annotations

import colorsys
import re
from typing import Iterable

from PIL import Image

RGB = tuple[int, int, int]


# ---------- Conversión y métricas de color ----------

def hex_to_rgb(value: str) -> RGB | None:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        return None
    try:
        return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))
    except ValueError:
        return None


def rgb_to_hex(rgb: RGB) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(c))) for c in rgb)


def _rel_luminance(rgb: RGB) -> float:
    """Luminancia relativa (WCAG), 0 = negro, 1 = blanco."""
    def chan(c: float) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: RGB, b: RGB) -> float:
    la, lb = _rel_luminance(a), _rel_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _saturation(rgb: RGB) -> float:
    r, g, b = (c / 255.0 for c in rgb)
    _, _, s = colorsys.rgb_to_hsv(r, g, b)
    return s


def _hsl(rgb: RGB) -> tuple[float, float, float]:
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def _from_hsl(h: float, s: float, l: float) -> RGB:
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (round(r * 255), round(g * 255), round(b * 255))


# ---------- Extracción desde imágenes y CSS ----------

def colors_from_image(path: str, sample: int = 120) -> list[tuple[RGB, int]]:
    """Devuelve los colores dominantes de una imagen (ignora transparencias)."""
    try:
        im = Image.open(path).convert("RGBA")
    except Exception:
        return []
    im.thumbnail((sample, sample))
    counts: dict[RGB, int] = {}
    for r, g, b, a in im.getdata():
        if a < 128:
            continue
        key = (r // 16 * 16, g // 16 * 16, b // 16 * 16)  # cuantización suave
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
_RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")


def colors_from_css(text: str) -> list[tuple[RGB, int]]:
    """Extrae y cuenta colores presentes en CSS/HTML en bruto."""
    counts: dict[RGB, int] = {}
    for m in _HEX_RE.findall(text or ""):
        rgb = hex_to_rgb(m)
        if rgb:
            counts[rgb] = counts.get(rgb, 0) + 1
    for r, g, b in _RGB_RE.findall(text or ""):
        rgb = (int(r), int(g), int(b))
        if all(0 <= c <= 255 for c in rgb):
            counts[rgb] = counts.get(rgb, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def _is_neutral(rgb: RGB) -> bool:
    """True si el color es casi blanco, casi negro o gris (mal candidato a acento)."""
    lum = _rel_luminance(rgb)
    return _saturation(rgb) < 0.18 or lum < 0.04 or lum > 0.95


def pick_accent(candidates: Iterable[tuple[RGB, float]], fallback: RGB = (79, 124, 255)) -> RGB:
    """Elige el color de marca más vivo entre los candidatos ponderados.

    `candidates` es una lista de (rgb, peso). Se prioriza saturación y un brillo
    intermedio (ni demasiado oscuro ni lavado), multiplicado por el peso.
    """
    best, best_score = None, 0.0
    for rgb, weight in candidates:
        if _is_neutral(rgb):
            continue
        _, s, l = _hsl(rgb)
        mid = 1.0 - abs(l - 0.5) * 1.4          # premia luminosidad media
        score = weight * (0.5 + s) * max(0.2, mid)
        if score > best_score:
            best, best_score = rgb, score
    return best or fallback


# ---------- Construcción del Brand Kit de color ----------

def build_color_kit(logo_path: str | None, web_text: str | None,
                    theme_color: str | None = None) -> dict:
    """Genera la paleta final para los diseños a partir del logo y la web."""
    candidates: list[tuple[RGB, float]] = []

    # El logo es la señal más fuerte de color de marca.
    if logo_path:
        for i, (rgb, cnt) in enumerate(colors_from_image(logo_path)[:6]):
            candidates.append((rgb, cnt * (3.0 if i < 3 else 1.5)))

    # theme-color declarado en la web es intención explícita de marca.
    if theme_color:
        tc = hex_to_rgb(theme_color)
        if tc:
            candidates.append((tc, 400))

    # Colores del CSS de la web, ponderados por frecuencia (señal más débil).
    if web_text:
        for rgb, cnt in colors_from_css(web_text)[:20]:
            candidates.append((rgb, cnt * 0.4))

    accent = pick_accent(candidates)
    h, s, _ = _hsl(accent)

    # Fondo oscuro tintado ligeramente hacia el color de marca (look premium).
    bg = _from_hsl(h, min(0.35, s * 0.4 + 0.05), 0.055)
    surface = _from_hsl(h, min(0.30, s * 0.35 + 0.05), 0.11)

    text = (255, 255, 255)
    muted = _from_hsl(h, 0.10, 0.66)
    # Color de texto que va SOBRE el acento (para botones): negro o blanco según contraste.
    accent_text = (14, 17, 22) if contrast_ratio(accent, (14, 17, 22)) >= 4.5 else (255, 255, 255)

    return {
        "accent": rgb_to_hex(accent),
        "accent_text": rgb_to_hex(accent_text),
        "bg": rgb_to_hex(bg),
        "surface": rgb_to_hex(surface),
        "text": rgb_to_hex(text),
        "muted": rgb_to_hex(muted),
        "danger": "#FF5A4D",
    }
