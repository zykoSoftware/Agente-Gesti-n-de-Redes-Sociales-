"""Copywriter: genera el texto de cada carrusel según el pilar de contenido.

Cada pilar devuelve una estructura de slides (gancho → desarrollo → CTA) lista
para volcarse en las plantillas de diseño. Los textos usan el nombre y el sector
de la empresa. Es un primer generador por plantilla; más adelante este módulo
puede delegar en un modelo de lenguaje para redactar copy a medida (ver
`generate` y el hook `_llm_copy`).
"""
from __future__ import annotations

# Pilares de contenido disponibles y su etiqueta visible.
PILLARS = {
    "problema_solucion": "Problema vs Solución",
    "nosotros_competencia": "Nosotros vs Competencia",
    "por_que_elegirnos": "Por qué elegirnos",
    "dato_sector": "Dato del sector",
}


def _problema_solucion(name: str, sector: str, handle: str) -> dict:
    en_sector = f"en {sector} " if sector else ""
    return {
        "eyebrow": "Problema vs Solución",
        "slides": [
            {"type": "hook",
             "pre": "El problema no", "hl": "eres tú.",
             "sub": f"Es cómo te lo han vendido {en_sector}hasta ahora.".replace("  ", " "),
             "foot": "Desliza y lo ves claro"},
            {"type": "list", "variant": "bad",
             "eyebrow": "El problema", "title_pre": "Lo de siempre", "title_hl": "no funciona.",
             "points": ["Pagas de más por lo mismo",
                        "Nadie te explica nada claro",
                        "Y al final pierdes tiempo"],
             "foot": "Hay una forma mejor"},
            {"type": "list", "variant": "good",
             "eyebrow": "La solución", "title_pre": f"Con {name}", "title_hl": "lo tienes fácil.",
             "points": ["Atención personalizada de verdad",
                        "Todo claro desde el primer día",
                        "Un equipo que responde cuando lo necesitas"],
             "foot": "Empieza hoy mismo"},
            {"type": "cta",
             "eyebrow": "Da el primer paso", "pre": "Hablemos", "hl": "hoy.",
             "sub": "Sin compromiso. Te contamos cómo podemos ayudarte.",
             "button": "Escríbenos por DM", "handle": handle},
        ],
    }


def _nosotros_competencia(name: str, sector: str, handle: str) -> dict:
    return {
        "eyebrow": "Nosotros vs Competencia",
        "slides": [
            {"type": "hook",
             "pre": "No todos", "hl": "somos iguales.",
             "sub": f"Te enseñamos la diferencia con {name}.",
             "foot": "Desliza y compara"},
            {"type": "list", "variant": "bad",
             "eyebrow": "Lo habitual", "title_pre": "La competencia", "title_hl": "se queda corta.",
             "points": ["Trato impersonal",
                        "Precios poco claros",
                        "Te dejan solo tras la venta"],
             "foot": "Nosotros lo hacemos distinto"},
            {"type": "list", "variant": "good",
             "eyebrow": "Con nosotros", "title_pre": f"En {name}", "title_hl": "vas de la mano.",
             "points": ["Trato cercano y directo",
                        "Precios transparentes",
                        "Acompañamiento de principio a fin"],
             "foot": "Así trabajamos"},
            {"type": "cta",
             "eyebrow": "Elige mejor", "pre": "Da el salto", "hl": "con nosotros.",
             "sub": "Descubre por qué cada vez más gente nos elige.",
             "button": "Escríbenos por DM", "handle": handle},
        ],
    }


def _por_que_elegirnos(name: str, sector: str, handle: str) -> dict:
    return {
        "eyebrow": "Por qué elegirnos",
        "slides": [
            {"type": "hook",
             "pre": "Por qué elegir", "hl": name + ".",
             "sub": "3 razones que marcan la diferencia.",
             "foot": "Desliza para verlas"},
            {"type": "list", "variant": "good",
             "eyebrow": "Razón 1 y 2", "title_pre": "Lo que", "title_hl": "nos hace únicos.",
             "points": ["Experiencia real en el sector",
                        "Resultados que puedes comprobar"],
             "foot": "Y hay más"},
            {"type": "list", "variant": "good",
             "eyebrow": "Razón 3", "title_pre": "Lo que más", "title_hl": "valoran de nosotros.",
             "points": ["Un trato que no encontrarás en otro sitio",
                        "Siempre a tu lado, antes y después"],
             "foot": "Compruébalo tú mismo"},
            {"type": "cta",
             "eyebrow": "Decídete", "pre": "Empieza", "hl": "con nosotros.",
             "sub": "Da el primer paso, nosotros nos encargamos del resto.",
             "button": "Escríbenos por DM", "handle": handle},
        ],
    }


def _dato_sector(name: str, sector: str, handle: str) -> dict:
    sec = sector or "el sector"
    return {
        "eyebrow": "Dato del sector",
        "slides": [
            {"type": "hook",
             "pre": "Un dato que", "hl": "deberías saber.",
             "sub": f"Sobre {sec} y lo que casi nadie te cuenta.",
             "foot": "Desliza para descubrirlo"},
            {"type": "list", "variant": "bad",
             "eyebrow": "La realidad", "title_pre": "Lo que", "title_hl": "casi nadie sabe.",
             "points": ["La mayoría elige sin comparar",
                        "Y acaba pagando el doble",
                        "Por no informarse antes"],
             "foot": "Aquí entramos nosotros"},
            {"type": "list", "variant": "good",
             "eyebrow": "La ventaja", "title_pre": f"Con {name}", "title_hl": "juegas con ventaja.",
             "points": ["Te asesoramos antes de decidir",
                        "Comparas de verdad",
                        "Y ahorras desde el primer día"],
             "foot": "Aprovéchalo"},
            {"type": "cta",
             "eyebrow": "No te quedes fuera", "pre": "Infórmate", "hl": "con nosotros.",
             "sub": "Te contamos lo que el sector no suele contar.",
             "button": "Escríbenos por DM", "handle": handle},
        ],
    }


_GENERATORS = {
    "problema_solucion": _problema_solucion,
    "nosotros_competencia": _nosotros_competencia,
    "por_que_elegirnos": _por_que_elegirnos,
    "dato_sector": _dato_sector,
}


def generate(pillar: str, name: str, sector: str = "", handle: str = "") -> dict:
    """Genera el guion de un carrusel para el pilar indicado."""
    handle = handle or name.lower().replace(" ", "")
    gen = _GENERATORS.get(pillar, _problema_solucion)
    return gen(name, sector, handle)


# Punto de extensión: redacción con modelo de lenguaje (Claude) cuando haya
# clave de API disponible. De momento el generador por plantilla es la vía por
# defecto, determinista y sin coste.
def _llm_copy(pillar: str, brand_tone: str, name: str, sector: str) -> dict | None:  # noqa: ARG001
    return None
