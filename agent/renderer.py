"""Renderizado de HTML a PNG usando Chrome/Chromium en modo headless."""
from __future__ import annotations

import base64
import subprocess
import tempfile
from pathlib import Path

from . import config


class RenderError(RuntimeError):
    pass


def logo_data_uri(logo_path: str | Path) -> str | None:
    """Convierte un logo en data URI para incrustarlo en el HTML del slide."""
    path = Path(logo_path)
    if not path.exists():
        return None
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "svg": "image/svg+xml", "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/png")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def render_html_to_png(html: str, out_path: str | Path,
                       width: int = config.SLIDE_WIDTH,
                       height: int = config.SLIDE_HEIGHT,
                       scale: int = config.RENDER_SCALE) -> Path:
    """Renderiza una cadena HTML a un PNG de tamaño exacto width x height."""
    chrome = config.find_chrome()
    if not chrome:
        raise RenderError(
            "No se encontró Chrome/Chromium. Instala Google Chrome o define "
            "la variable CHROME_BIN con la ruta al binario."
        )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_path = Path(tmp.name)

    try:
        cmd = [
            chrome, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--disable-dev-shm-usage",
            f"--force-device-scale-factor={scale}",
            f"--window-size={width},{height}",
            f"--screenshot={out_path}",
            tmp_path.as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if not out_path.exists():
            raise RenderError(f"Chrome no generó la imagen. {proc.stderr[-400:]}")
        return out_path
    except subprocess.TimeoutExpired as exc:
        raise RenderError("El render superó el tiempo límite.") from exc
    finally:
        tmp_path.unlink(missing_ok=True)
