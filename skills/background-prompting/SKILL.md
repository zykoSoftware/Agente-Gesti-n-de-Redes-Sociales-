---
name: background-prompting
description: Escribe prompts para modelos de generación de imágenes (DALL·E, Flux, Stable Diffusion) que producen FONDOS on-brand para los slides, nunca texto. Úsalo cuando un slide necesite una imagen de fondo generada por IA.
---

# Prompts de fondos con IA

Genera prompts para modelos de imágenes que produzcan **fondos** coherentes con
la marca. Nunca se genera texto con la IA (sale deforme); el texto va por CSS.

## Cuándo usar esta skill
- Cuando un slide requiera un fondo generado (ilustración, textura, escena).

## Reglas de oro
- **Solo fondos.** Prohibido pedir texto, logos o marcas de agua a la IA.
- El fondo debe dejar **zona limpia** para el texto (composición con espacio
  negativo o desenfoque en la zona de la copy).
- Respeta la **paleta del Brand Kit**: incluye los colores de marca en el prompt.
- Evita elementos que choquen con el acento o compliquen la legibilidad.

## Estructura del prompt
```
[sujeto/escena], [estilo visual], paleta [colores del Brand Kit],
composición con amplio espacio negativo en [zona], iluminación [x],
sin texto, sin logos, sin marcas de agua, formato vertical 4:5
```

## Ejemplos
- *Fitness*: "gimnasio moderno desenfocado al fondo, tonos oscuros con acento
  lima, mucho espacio negativo arriba, cinemático, sin texto ni logos, 4:5".
- *Legal*: "despacho elegante con luz suave, tonos grafito y coral, minimalista,
  espacio negativo a la izquierda, sin texto, 4:5".

## Postproceso
Tras generar, difumina o oscurece la zona donde irá la copy para garantizar
contraste antes de componer el slide con la skill `carousel-design`.
