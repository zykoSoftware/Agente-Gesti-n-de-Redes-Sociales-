# Agente de Gestión de Redes Sociales

Agente que diseña y genera **carruseles de imágenes** para redes sociales con la
identidad de cada empresa. Esta primera versión incluye:

- 🏢 **Interfaz visual** para gestionar perfiles de varias empresas.
- 🎨 **Análisis de marca**: a partir de la **web** y el **logo** de cada empresa,
  extrae colores, tipografía y tono → *Brand Kit*.
- 🖼️ **Motor de diseño HTML → PNG**: genera carruseles profesionales (1080×1350)
  con los colores y el logo de la empresa. El texto se compone por CSS (siempre
  nítido y on-brand); la IA de imágenes se reservará solo para fondos.
- 🧠 **Copywriter por pilares**: *Problema vs Solución*, *Nosotros vs Competencia*,
  *Por qué elegirnos*, *Dato del sector*.

> Estado: MVP del motor de contenido. La **publicación automática** en Instagram
> y TikTok y el **asistente de DMs/comentarios** son los siguientes módulos
> (ver la propuesta del proyecto).

## Requisitos

- Python 3.10+
- **Google Chrome o Chromium** instalado (se usa para renderizar HTML a PNG).
  Si no está en el PATH, define la ruta con la variable `CHROME_BIN`.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
python run.py
```

Abre **http://127.0.0.1:5000** y:

1. Crea una empresa con su **nombre**, **web** y **logo**.
2. El agente analiza la marca y muestra el **Brand Kit** (paleta, fuente, tono).
3. Elige un **pilar de contenido** y pulsa **Generar carrusel**.
4. Se generan 4 slides en PNG listos para revisar.

Los datos (perfiles, logos y carruseles) se guardan en la carpeta `data/`
(ignorada por git).

## Estructura

```
agent/
  config.py       Config y localización de Chrome
  store.py        Persistencia de perfiles (JSON)
  palette.py      Extracción de color y construcción de paleta
  brand.py        Análisis de marca (web + logo) → Brand Kit
  copywriter.py   Guion de cada carrusel por pilar
  designer.py     Plantillas HTML de los slides
  renderer.py     Render HTML → PNG con Chromium
  pipeline.py     Orquestación completa
web/
  app.py          Rutas Flask
  templates/      Interfaz (empresas y perfil)
run.py            Arranque
```

## Configuración

| Variable          | Descripción                                             |
|-------------------|---------------------------------------------------------|
| `CHROME_BIN`      | Ruta al binario de Chrome/Chromium.                     |
| `AGENT_DATA_DIR`  | Carpeta de datos (por defecto `./data`).                |
| `AGENT_RENDER_SCALE` | Escala de render (2 = retina, por defecto).          |
