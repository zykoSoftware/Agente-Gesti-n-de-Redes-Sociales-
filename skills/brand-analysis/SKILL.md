---
name: brand-analysis
description: Analiza la identidad visual y verbal de una empresa a partir de su web y su logo para construir un Brand Kit (paleta de color, tipografía, tono y valores). Úsalo al dar de alta una empresa nueva o al re-analizar su marca antes de generar contenido.
---

# Análisis de marca (Brand Kit)

Convierte la web y el logo de una empresa en un **Brand Kit** reutilizable que
todos los demás agentes aplicarán a cada publicación.

## Cuándo usar esta skill
- Al crear el perfil de una empresa nueva.
- Cuando cambie el logo, la web o el posicionamiento.
- Antes de la primera tanda de contenido de una marca.

## Entradas
- URL de la web de la empresa.
- Logo en alta calidad (PNG/SVG preferible).
- Sector y, si existe, guía de marca (PDF).

## Proceso
1. **Color**: extrae la paleta del logo (color de marca = señal más fuerte) y de
   la web (CSS + `theme-color`). Elige un **acento** vivo, un **fondo** oscuro
   tintado hacia el acento, y colores de texto con contraste AA (ratio ≥ 4.5).
2. **Tipografía**: detecta la fuente de la web y mapéala a un stack seguro; si no
   hay señal, usa un sans neutro de sistema.
3. **Tono de voz**: describe en 1–2 frases cómo habla la marca (cercano, técnico,
   premium, divertido…) a partir de los textos de la web.
4. **Valores y diferenciadores**: lista 3–5 cosas que hacen única a la empresa
   (se usarán en los pilares "Por qué elegirnos" y "Nosotros vs competencia").
5. **Público objetivo**: define a quién le habla la marca.

## Salida (Brand Kit)
```json
{
  "colors": {"accent": "#..", "bg": "#..", "text": "#..", "muted": "#.."},
  "font": "stack tipográfico",
  "tone": "descripción del tono",
  "values": ["...", "...", "..."],
  "audience": "descripción del público",
  "handle": "@usuario"
}
```

## Reglas
- Prioriza SIEMPRE los colores del logo sobre los de la web.
- Garantiza contraste legible; nunca texto de bajo contraste sobre el fondo.
- Si la web no es accesible, construye el kit solo con el logo y avísalo.
- No inventes valores de marca: extráelos de lo que dice realmente la empresa.
