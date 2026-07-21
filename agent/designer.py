"""Motor de diseño: convierte el guion del carrusel en HTML por slide.

Aplica el Brand Kit (colores, tipografía, logo) a plantillas profesionales.
El texto y la composición se controlan por CSS para que salgan perfectos; la IA
de imágenes queda reservada para fondos (punto de extensión futuro).
"""
from __future__ import annotations

import html as html_lib

from . import config


def _esc(text: str) -> str:
    return html_lib.escape(text or "")


def _base_css(c: dict, font: str) -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{config.SLIDE_WIDTH}px; height:{config.SLIDE_HEIGHT}px; overflow:hidden; }}
body {{ background:{c['bg']}; color:{c['text']}; font-family:{font}; position:relative; }}
.slide {{ width:{config.SLIDE_WIDTH}px; height:{config.SLIDE_HEIGHT}px;
  padding:84px 80px; display:flex; flex-direction:column; position:relative; }}
.top {{ display:flex; justify-content:space-between; align-items:center; z-index:3; }}
.brand {{ font-weight:900; font-size:34px; letter-spacing:.14em; color:{c['text']}; }}
.brand .dot {{ color:{c['accent']}; }}
.logo {{ height:64px; max-width:360px; object-fit:contain; }}
.pager {{ font-family:ui-monospace,Menlo,monospace; font-size:24px; color:{c['muted']};
  letter-spacing:.1em; font-weight:600; }}
.pager b {{ color:{c['accent']}; }}
.eyebrow {{ display:inline-block; align-self:flex-start; font-family:ui-monospace,Menlo,monospace;
  font-size:23px; letter-spacing:.26em; text-transform:uppercase; font-weight:700;
  color:{c['accent_text']}; background:{c['accent']}; padding:12px 20px; border-radius:8px; }}
.eyebrow.danger {{ background:{c['danger']}; color:#fff; }}
.mid {{ flex:1; display:flex; flex-direction:column; justify-content:center; z-index:3; gap:34px; }}
h1 {{ font-size:100px; line-height:.99; font-weight:900; letter-spacing:-.03em; color:{c['text']}; }}
h1 .hl {{ color:{c['accent']}; }}
h1 .hl.danger {{ color:{c['danger']}; }}
.sub {{ font-size:41px; line-height:1.3; color:{c['muted']}; font-weight:500; max-width:20ch; }}
.list {{ display:flex; flex-direction:column; gap:26px; }}
.item {{ display:flex; align-items:center; gap:26px; font-size:43px; font-weight:600;
  line-height:1.2; color:{c['text']}; }}
.item .ic {{ width:64px; height:64px; border-radius:16px; flex:none; display:flex;
  align-items:center; justify-content:center; font-size:38px; font-weight:900; }}
.bad .ic {{ background:{c['danger']}22; color:{c['danger']}; }}
.good .ic {{ background:{c['accent']}22; color:{c['accent']}; }}
.bottom {{ display:flex; align-items:center; gap:16px; font-size:30px; color:{c['muted']};
  font-weight:600; z-index:3; }}
.bottom .arrow {{ color:{c['accent']}; font-size:38px; }}
.handle {{ font-weight:800; color:{c['text']}; }}
.ghost {{ position:absolute; right:-40px; bottom:-120px; font-size:620px; font-weight:900;
  color:{c['text']}; opacity:.035; letter-spacing:-.05em; z-index:1; line-height:1; }}
.cta-btn {{ display:inline-flex; align-items:center; gap:18px; background:{c['accent']};
  color:{c['accent_text']}; font-size:44px; font-weight:900; padding:28px 44px;
  border-radius:20px; align-self:flex-start; letter-spacing:-.01em; }}
.glow {{ position:absolute; width:900px; height:900px; border-radius:50%;
  background:radial-gradient(circle,{c['accent']}22 0%,transparent 60%);
  top:-200px; right:-200px; z-index:0; }}
"""


def _brand_mark(name: str, logo_uri: str | None) -> str:
    if logo_uri:
        return f'<img class="logo" src="{logo_uri}" alt="{_esc(name)}">'
    return f'<div class="brand">{_esc(name.upper())}<span class="dot">.</span></div>'


def _header(name: str, logo_uri: str | None, idx: int, total: int) -> str:
    return (f'<div class="top">{_brand_mark(name, logo_uri)}'
            f'<div class="pager"><b>{idx:02d}</b> / {total:02d}</div></div>')


def _footer_hint(text: str) -> str:
    return f'<div class="bottom"><span class="arrow">&#8594;</span> {_esc(text)}</div>'


def _slide_html(slide: dict, ctx: dict, idx: int, total: int) -> str:
    c, font = ctx["colors"], ctx["font"]
    name, logo_uri = ctx["name"], ctx["logo_uri"]
    header = _header(name, logo_uri, idx, total)
    body = ""

    if slide["type"] == "hook":
        body = f"""
          <div class="glow"></div>{header}
          <div class="mid">
            <span class="eyebrow">{_esc(ctx['eyebrow'])}</span>
            <h1>{_esc(slide['pre'])} <span class="hl">{_esc(slide['hl'])}</span></h1>
            <div class="sub">{_esc(slide['sub'])}</div>
          </div>
          {_footer_hint(slide['foot'])}"""

    elif slide["type"] == "list":
        variant = slide.get("variant", "good")
        eyebrow_cls = "eyebrow danger" if variant == "bad" else "eyebrow"
        hl_cls = "hl danger" if variant == "bad" else "hl"
        icon = "&#10005;" if variant == "bad" else "&#10003;"
        items = "".join(
            f'<div class="item {variant}"><span class="ic">{icon}</span> {_esc(p)}</div>'
            for p in slide["points"]
        )
        ghost = f'<div class="ghost">{idx - 1:02d}</div>'
        body = f"""
          {ghost}{header}
          <div class="mid">
            <span class="{eyebrow_cls}">{_esc(slide['eyebrow'])}</span>
            <h1>{_esc(slide['title_pre'])} <span class="{hl_cls}">{_esc(slide['title_hl'])}</span></h1>
            <div class="list">{items}</div>
          </div>
          {_footer_hint(slide['foot'])}"""

    elif slide["type"] == "cta":
        handle = slide.get("handle") or ctx["name"].lower().replace(" ", "")
        body = f"""
          <div class="glow"></div>{header}
          <div class="mid">
            <span class="eyebrow">{_esc(slide['eyebrow'])}</span>
            <h1>{_esc(slide['pre'])} <span class="hl">{_esc(slide['hl'])}</span></h1>
            <div class="sub">{_esc(slide['sub'])}</div>
            <div class="cta-btn">{_esc(slide['button'])}</div>
          </div>
          <div class="bottom">Síguenos en <span class="handle">@{_esc(handle)}</span></div>"""

    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<style>{_base_css(c, font)}</style></head>'
            f'<body><div class="slide">{body}</div></body></html>')


def build_carousel(script: dict, name: str, brand: dict,
                   logo_uri: str | None = None) -> list[str]:
    """Devuelve la lista de HTML (uno por slide) de un carrusel completo."""
    ctx = {
        "colors": brand["colors"],
        "font": brand.get("font", "system-ui, sans-serif"),
        "name": name,
        "logo_uri": logo_uri,
        "eyebrow": script["eyebrow"],
    }
    slides = script["slides"]
    total = len(slides)
    return [_slide_html(s, ctx, i + 1, total) for i, s in enumerate(slides)]
