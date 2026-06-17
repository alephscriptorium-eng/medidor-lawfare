# Prompt — Llenar buffer (agente externo)

Plantilla para pedir a un agente externo un **nuevo buffer de contexto** (MCS-N). Sustituir variables entre `{{…}}`.

---

## Variables

| Variable | Ejemplo (caso inaugural) |
|----------|--------------------------|
| `{{caso_id}}` | `zapatero-plus-ultra` |
| `{{caso_foco_id}}` | `ZAP-PU-2026-06-17` |
| `{{caso_etiqueta}}` | Zapatero / Plus Ultra |
| `{{medicion_activa}}` | M2 |
| `{{intensidad_activa}}` | 6.5 |
| `{{buffers_activos}}` | MCS-1, MCS-2 |
| `{{proposito_buffer}}` | Verificar delta 5→6.4 / ampliar ventanas temporales / etc. |

---

## BLOQUE PARA EL AGENTE

Estoy alimentando el **Medidor de Lawfare** (artefacto FOSS con cribado MCN L0–L3). Necesito un **nuevo buffer de contexto** para el caso:

- **Caso:** `{{caso_etiqueta}}` — `{{caso_foco_id}}` (`{{caso_id}}`)
- **Medición actual:** `{{medicion_activa}}` = **{{intensidad_activa}}/10**
- **Buffers ya cargados (inmutables):** {{buffers_activos}}

**Propósito de este buffer:** {{proposito_buffer}}

---

### Qué debe contener tu respuesta

1. **Bloque interpretativo** (opcional): mecanismos, hipótesis — se marcará probablemente L3.
2. **Bloque de datos duros** (obligatorio): fechas, procedimientos, sentencias, URLs, citas ≤25 palabras.

Prioriza datos **anclados al caso foco** cuando existan en fuentes públicas. Si no existen, dilo; no inventes.

---

### Formato de entrega (markdown)

Guardar como `docs/sesiones/buffer-NN.md`:

```markdown
# Buffer MCS-N — {{caso_etiqueta}}

## Origen
Agente: [nombre/modelo] | Fecha: [YYYY-MM-DD]

## Bloque interpretativo
[ párrafos opcionales ]

## Bloque datos verificables

### [Título hecho 1]
- Fecha:
- Procedimiento / juzgado:
- Fuente:
- Cita o URL:

### [Título hecho 2]
...
```

---

### Ranuras MCS (asignar cuando sea obvio)

`historico_imputaciones` | `patrones_acusacion` | `cobertura_mediatica` | `ventanas_temporales` | `actores_recurrentes` | `precedentes_judiciales` | `vectores_politicos` | `intensidad_historica_comparable` | `meta_patrones_sistemicos`

---

### Reglas

- No repitas hechos ya en buffers anteriores salvo que añadas dato nuevo verificable.
- No sustituyas fuentes por opinión (“es conocido que…”, “sin duda…”).
- El usuario convertirá este markdown a `data/buffers/MCS-N-entrada.json` y ejecutará `medidor cribar` / `medidor commit`.

---

## FIN DEL PROMPT
