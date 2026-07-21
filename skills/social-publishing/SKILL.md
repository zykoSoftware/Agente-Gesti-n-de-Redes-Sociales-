---
name: social-publishing
description: Publica carruseles y vídeos en Instagram y TikTok adaptando cada pieza a su formato, con cola de aprobación humana previa. Úsalo para programar y publicar el contenido en las redes.
---

# Publicación multiplataforma

Publica cada pieza en la plataforma y el formato correctos, con revisión humana
antes de salir a las cuentas reales.

## Cuándo usar esta skill
- Al programar o publicar cualquier contenido aprobado.

## Mapa de formatos
| Contenido | Instagram | TikTok |
|-----------|-----------|--------|
| Carrusel de imágenes | Post de feed (varias imágenes) | Modo foto |
| Vídeo real (Drive) | Reel | Vídeo |

> Un carrusel es un post de feed, NO un Reel. Los vídeos van a Reels/TikTok vídeo.

## Vías de publicación (módulo intercambiable)
1. **API agregadora** (Ayrshare, Blotato, upload-post): una sola API para todas
   las redes, sin esperar aprobaciones de Meta/TikTok. Recomendada para el MVP.
2. **Automatización** (Make, n8n): webhook → publica.
3. **APIs oficiales** (Meta Graph, TikTok Content Posting): sin cuota, pero
   requieren revisión/auditoría.

El agente llama a UNA interfaz interna `publicar(carrusel, texto, plataformas)`;
el backend concreto se puede cambiar sin tocar el resto.

## Reglas
- **Cola de aprobación por defecto**: nada se publica sin visto bueno humano.
- Publica en el **mejor horario** calculado para cada cuenta.
- Adjunta caption + hashtags generados por el copywriter.
- Registra cada publicación en el banco de contenido (para el cooldown y la
  analítica).

## Requisitos de acceso
- Instagram: cuenta Business/Creator + página de Facebook + app de Meta.
- TikTok: app de desarrollador + auditoría para publicación directa.
Mientras llegan, opera en modo cola de aprobación (publicación manual con 1 clic).
