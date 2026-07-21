---
name: content-strategy
description: Decide qué publicar cada día combinando un calendario de pilares fijos con el contenido real disponible en Drive, evitando repeticiones. Úsalo para planificar la publicación diaria y para inventar contenido cuando no hay material real.
---

# Estrategia de contenido

Actúa como director de marketing: decide el contenido de cada día con intención
comercial, no para "rellenar el feed".

## Cuándo usar esta skill
- Cada día, antes de generar la publicación.
- Al planificar la semana o el mes.

## Calendario de pilares (por defecto)
| Día | Pilar | Objetivo |
|-----|-------|----------|
| Lun | Problema vs Solución | Enganchar por dolor |
| Mar | Dato del sector (que vende) | Autoridad |
| Mié | Nosotros vs Competencia | Diferenciación |
| Jue | Por qué elegirnos | Deseo |
| Vie | Testimonio / caso de éxito | Prueba social |
| Sáb | Detrás de cámaras (Drive real) | Cercanía |
| Dom | Tip / mini-guía guardable | Alcance (guardados) |

Pilares extra que rotan: mitos vs realidad, errores de la competencia, antes y
después, objeción → respuesta, checklist, oferta/lanzamiento.

## Reglas de decisión (en orden)
1. **Contenido real primero**: si hoy hay foto/vídeo real en Drive que encaje con
   el pilar del día, ese manda.
2. **Si no hay real, inventa** una publicación para el pilar del día.
3. **Nunca dejes un día sin publicación.**
4. **Cooldown**: consulta el banco de contenido publicado y no repitas el mismo
   ángulo ni frases durante al menos 3–4 semanas.
5. **Temporada**: ten en cuenta fechas del sector, campañas y lanzamientos.

## Salida
```json
{
  "date": "YYYY-MM-DD",
  "pillar": "problema_solucion",
  "source": "real|generado",
  "asset": "id del archivo de Drive o null",
  "angle": "ángulo concreto elegido",
  "goal": "seguidores|guardados|dm|ventas"
}
```

## Bucle de aprendizaje
Revisa las métricas de las últimas semanas y da más peso a los pilares y
formatos que mejor funcionan en esta cuenta concreta.
