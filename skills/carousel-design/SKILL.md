---
name: carousel-design
description: Compone slides de carrusel (1080x1350) en HTML/CSS aplicando el Brand Kit y el logo, listos para exportar a PNG con Chromium. Úsalo para diseñar cada carrusel de forma profesional y on-brand.
---

# Diseño de carruseles (HTML → PNG)

Convierte el guion del copywriter en slides visuales perfectos, aplicando los
colores, la tipografía y el logo del Brand Kit. El texto se compone por CSS
(siempre nítido); la IA de imágenes solo aporta fondos.

## Cuándo usar esta skill
- Al maquetar cualquier carrusel antes de publicarlo.

## Especificaciones
- Tamaño: **1080 × 1350 px** (feed vertical de Instagram / carrusel de TikTok).
- Render a **2× (retina)** con Chromium headless.
- Una plantilla por tipo de slide: `hook`, `list`, `cta`.

## Sistema visual (del Brand Kit)
- **Fondo**: color oscuro tintado hacia el acento de la marca.
- **Acento**: color de marca para destacar palabras clave, iconos y CTA.
- **Logo**: arriba a la izquierda; si no hay, wordmark del nombre.
- **Paginador**: `01 / 04` arriba a la derecha.
- **Jerarquía**: titular enorme (peso 900), subtítulo medio, bullets legibles.

## Reglas de calidad
- Contraste AA en todo el texto; nunca texto ilegible sobre el fondo.
- `text-wrap: balance` en titulares; evita viudas y desbordes.
- Un mensaje por slide; no saturar.
- Coherencia entre todos los slides del mismo carrusel y entre pilares.
- Iconos ✓ para lo positivo, ✕ para lo negativo (rojo de aviso).

## Flujo
1. Recibe `slides` (del copywriter) + `brand` (del Brand Kit) + `logo`.
2. Rellena la plantilla HTML de cada slide con colores, fuente y logo.
3. Renderiza cada HTML a PNG con Chromium (`--screenshot`, `--window-size`).
4. Devuelve la lista de PNGs en orden.

## Fondos con IA (opcional)
Si se usa un modelo de imágenes, genera SOLO el fondo (ilustración/gradiente
acorde a la estética), difumínalo y colócalo detrás; el texto SIEMPRE por CSS.
