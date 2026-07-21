# Skills del Agente de Redes Sociales

Skills personalizadas que especializan a cada subagente del sistema. Cada carpeta
contiene un `SKILL.md` (formato Anthropic Agent Skills: frontmatter `name` +
`description`, y las instrucciones).

| Skill | Subagente | Qué hace |
|-------|-----------|----------|
| `brand-analysis` | Analista de Marca | Web + logo → Brand Kit (color, tipografía, tono) |
| `content-strategy` | Estratega | Decide qué publicar cada día (calendario + Drive) |
| `carousel-copywriting` | Copywriter | Gancho, desarrollo, CTA, caption y hashtags |
| `carousel-design` | Diseñador | Slides HTML→PNG on-brand (1080×1350) |
| `background-prompting` | Ilustrador | Prompts de fondos para IA de imágenes (sin texto) |
| `social-publishing` | Publicador | Publica en Instagram y TikTok con cola de aprobación |
| `community-management` | Community Manager | Responde DMs y comentarios; escala lo sensible |
| `growth-analytics` | Analista de Crecimiento | Lee métricas y ajusta la estrategia; informes |

## Skills oficiales de Anthropic que reutilizamos
Estas vienen incluidas con Claude (no hay que crearlas):
- `pdf` — leer guías de marca en PDF (Analista de Marca).
- `xlsx` — informes en Excel (Analista de Crecimiento).
- `dataviz` — gráficos de rendimiento (Analista de Crecimiento).
- `artifact-design` — fundamentos de diseño (Diseñador).

## Cómo se usan
Con el Claude Agent SDK / Managed Agents, cada subagente se crea con su modelo y
sus skills. Las skills se cargan bajo demanda cuando la tarea las necesita.
