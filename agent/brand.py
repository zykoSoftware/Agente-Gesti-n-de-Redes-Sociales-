"""Analizador de marca: convierte la web + el logo en un Brand Kit.

Descarga el HTML de la web de la empresa, extrae señales de identidad
(nombre, descripción, tipografías, colores) y las combina con los colores del
logo para construir la paleta y el tono que usarán todos los diseños.
"""
from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from . import palette

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SocialAgent/1.0; +https://example.com/bot)"
}

# Tipografías web habituales que podemos mapear a stacks seguros del sistema.
_FONT_HINTS = {
    "poppins": "'Poppins', system-ui, sans-serif",
    "montserrat": "'Montserrat', system-ui, sans-serif",
    "inter": "'Inter', system-ui, sans-serif",
    "roboto": "'Roboto', system-ui, sans-serif",
    "lato": "'Lato', system-ui, sans-serif",
    "open sans": "'Open Sans', system-ui, sans-serif",
    "raleway": "'Raleway', system-ui, sans-serif",
    "playfair": "'Playfair Display', Georgia, serif",
    "merriweather": "Merriweather, Georgia, serif",
    "oswald": "Oswald, 'Arial Narrow', sans-serif",
}
_DEFAULT_FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"


def _fetch(url: str) -> tuple[str, str | None]:
    """Descarga el HTML de la web. Devuelve (html, error)."""
    if not url:
        return "", "sin URL"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=12)
        resp.raise_for_status()
        return resp.text, None
    except requests.RequestException as exc:
        return "", f"no se pudo acceder a la web ({exc.__class__.__name__})"


def _detect_font(html: str, soup: BeautifulSoup) -> str:
    text = html.lower()
    # Fuentes de Google Fonts declaradas en la web.
    for link in soup.find_all("link", href=True):
        href = link["href"].lower()
        if "fonts.googleapis" in href:
            for name, stack in _FONT_HINTS.items():
                if name.replace(" ", "+") in href or name.replace(" ", "") in href:
                    return stack
    # font-family en el CSS embebido.
    for name, stack in _FONT_HINTS.items():
        if name in text:
            return stack
    return _DEFAULT_FONT


def _tone(soup: BeautifulSoup, sector: str) -> str:
    """Resumen breve del tono/temática a partir de meta y titulares."""
    bits = []
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        bits.append(desc["content"].strip())
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        bits.append(og["content"].strip())
    if not bits:
        h1 = soup.find(["h1", "h2"])
        if h1:
            bits.append(h1.get_text(strip=True))
    tone = " ".join(bits)[:280]
    if not tone and sector:
        tone = f"Empresa del sector {sector}."
    return tone


def analyze(name: str, website: str, logo_path: str | None, sector: str = "") -> dict:
    """Analiza la marca y devuelve el Brand Kit (colores, fuente, tono, meta)."""
    html, error = _fetch(website)
    soup = BeautifulSoup(html, "html.parser") if html else BeautifulSoup("", "html.parser")

    theme_color = None
    tc = soup.find("meta", attrs={"name": "theme-color"})
    if tc and tc.get("content"):
        theme_color = tc["content"].strip()

    site_name = None
    og_name = soup.find("meta", property="og:site_name")
    if og_name and og_name.get("content"):
        site_name = og_name["content"].strip()

    colors = palette.build_color_kit(logo_path, html, theme_color)
    font = _detect_font(html, soup) if html else _DEFAULT_FONT
    tone = _tone(soup, sector)

    return {
        "colors": colors,
        "font": font,
        "tone": tone,
        "site_name": site_name or name,
        "source": "web+logo" if html else ("logo" if logo_path else "por defecto"),
        "error": error,
    }


def brand_or_default(name: str, sector: str = "") -> dict:
    """Brand Kit neutro por si aún no se ha analizado nada."""
    return {
        "colors": palette.build_color_kit(None, None, None),
        "font": _DEFAULT_FONT,
        "tone": f"Empresa del sector {sector}." if sector else "",
        "site_name": name,
        "source": "por defecto",
        "error": None,
    }
