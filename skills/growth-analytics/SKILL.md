---
name: growth-analytics
description: Lee las métricas de las publicaciones (alcance, guardados, DMs, conversiones) y ajusta la estrategia futura, generando informes. Úsalo para el bucle de aprendizaje y los reportes de rendimiento.
---

# Analítica y crecimiento

Cierra el bucle: aprende de lo que funciona y hace que el agente publique mejor
cada semana.

## Cuándo usar esta skill
- Semanalmente (o tras cada campaña) para revisar rendimiento y ajustar.
- Al generar informes para el cliente/jefe.

## Métricas clave
- **Alcance / impresiones**: cuánta gente lo ve.
- **Guardados y compartidos**: mejor señal de contenido valioso (amplían alcance).
- **Interacción** (likes, comentarios): resonancia.
- **DMs generados**: intención comercial.
- **Clics / conversiones**: resultado de negocio.

## Proceso
1. Recoge métricas por publicación y por pilar.
2. Identifica qué **pilares, formatos y horarios** rinden mejor en esta cuenta.
3. Envía recomendaciones al estratega (`content-strategy`) para dar más peso a
   lo que funciona y jubilar lo que no.
4. Detecta ganadores para reutilizar el ángulo (respetando el cooldown).

## Informes
- Tabla de rendimiento por pilar (usa la skill `xlsx` para el Excel).
- Gráficos de evolución (usa la skill `dataviz` para las visualizaciones).
- Resumen ejecutivo: qué funcionó, qué no, y qué haremos distinto.

## Salida
```json
{
  "period": "YYYY-Www",
  "top_pillars": ["...", "..."],
  "best_time": "hora óptima",
  "recommendations": ["...", "..."]
}
```
