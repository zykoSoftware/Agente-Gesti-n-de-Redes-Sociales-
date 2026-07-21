"""Configuración y utilidades de entorno del agente."""
from __future__ import annotations

import glob
import os
import shutil
from pathlib import Path

# Raíz del proyecto y carpeta de datos (perfiles, logos, posts generados).
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("AGENT_DATA_DIR", ROOT / "data"))
PROFILES_FILE = DATA_DIR / "profiles.json"

# Dimensiones de cada slide del carrusel (formato vertical recomendado de Instagram).
SLIDE_WIDTH = 1080
SLIDE_HEIGHT = 1350
# Factor de escala para render nítido (2 = calidad retina).
RENDER_SCALE = int(os.environ.get("AGENT_RENDER_SCALE", "2"))


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "profiles").mkdir(parents=True, exist_ok=True)


def find_chrome() -> str | None:
    """Localiza un binario de Chrome/Chromium para renderizar HTML a PNG."""
    if os.environ.get("CHROME_BIN") and Path(os.environ["CHROME_BIN"]).exists():
        return os.environ["CHROME_BIN"]

    # Chromium instalado por Playwright (entornos de desarrollo/CI).
    for pattern in (
        "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
        "/opt/pw-browsers/chromium-*/chrome-linux/headless_shell",
    ):
        matches = sorted(glob.glob(pattern))
        if matches:
            return matches[-1]

    # Binarios habituales del sistema (Linux / macOS).
    candidates = [
        "chromium", "chromium-browser", "google-chrome",
        "google-chrome-stable", "chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for c in candidates:
        found = shutil.which(c) if "/" not in c else (c if Path(c).exists() else None)
        if found:
            return found
    return None
