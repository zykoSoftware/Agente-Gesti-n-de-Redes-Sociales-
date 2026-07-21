# Skills del Agente de Redes Sociales

Skills profesionales que especializan a cada subagente del sistema. Cada una da al
agente una **identidad** (quién es, su experiencia, su mentalidad), su **lugar en el
equipo**, una metodología detallada, estándares de calidad y errores a evitar.

Formato Anthropic Agent Skills: cada carpeta tiene un `SKILL.md` con frontmatter
(`name`, `description`) y las instrucciones.

| Skill | Subagente | Rol |
|-------|-----------|-----|
| `brand-analysis` | Analista de Marca | Web + logo → Brand Kit verificado |
| `content-strategy` | Estratega | Qué publicar cada día (calendario + Drive) |
| `carousel-copywriting` | Copywriter | Gancho, desarrollo, CTA, caption, hashtags |
| `carousel-design` | Director de Arte | Diseña el carrusel generándolo con IA |
| `image-prompting` | Director de Arte | Maestría de prompting de imagen (texto legible, serie coherente) |
| `quality-review` | Revisor de Calidad (QA) | Revisa ortografía, estética, marca y brief antes de publicar |
| `social-publishing` | Publicador | Publica en Instagram y TikTok con cola de aprobación |
| `community-management` | Community Manager | Responde DMs y comentarios; escala lo sensible |
| `growth-analytics` | Analista de Crecimiento | Lee métricas y ajusta la estrategia; informes |

## Cambio de enfoque: imágenes con IA
Las imágenes ya **no** se maquetan en HTML: se **generan con IA** (Ideogram,
GPT-Image, Flux…). Por eso el Diseñador es ahora un **Director de Arte maestro del
prompting**, y añadimos un **Revisor de Calidad (QA)** que verifica ortografía,
exactitud del texto generado, estética y coherencia con el brief antes de publicar.

## Skills oficiales de Anthropic que reutilizamos
Vienen incluidas con Claude (no hay que crearlas):
- `pdf` — leer guías de marca en PDF (Analista de Marca).
- `xlsx` — informes en Excel (Analista de Crecimiento).
- `dataviz` — gráficos de rendimiento (Analista de Crecimiento).
- `artifact-design` — fundamentos de diseño (Director de Arte).

## Cómo se usan
Con el Claude Agent SDK / Managed Agents, cada subagente se crea con su modelo y
sus skills. Las skills se cargan bajo demanda cuando la tarea las necesita.
