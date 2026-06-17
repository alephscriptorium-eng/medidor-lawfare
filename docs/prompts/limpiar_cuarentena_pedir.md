# Prompt — Limpiar cuarentena (pedir datos)

Plantilla para solicitar **solidificación o descarte explícito** de ítems en cuarentena L3. Sustituir `{{…}}`.

**Entrada:** lista de ítems desde `data/casos/{{caso_id}}/cribados/cribado-MCS-N.json` → array `cuarentena[]`.

---

## Variables

| Variable | Ejemplo |
|----------|---------|
| `{{caso_id}}` | `zapatero-plus-ultra` |
| `{{caso_foco_id}}` | `ZAP-PU-2026-06-17` |
| `{{caso_etiqueta}}` | Zapatero / Plus Ultra |
| `{{buffer_id}}` | MCS-2 |
| `{{medicion_activa}}` | M2 |
| `{{intensidad_activa}}` | 6.5 |

---

## BLOQUE PARA EL AGENTE

El buffer `{{buffer_id}}` fue cribado por el MCN. Parte de los ítems quedó en **cuarentena (L3)** por falta de ancla verificable. Necesito resolver **cada ítem** del listado inferior.

**Caso foco (inmutable):** `{{caso_etiqueta}}` — `{{caso_foco_id}}`  
**Medición actual:** `{{medicion_activa}}` = {{intensidad_activa}}/10

---

### Regla binaria (sin tercera vía)

| Salida | Condición |
|--------|-----------|
| **SOLIDIFICAR** | Aportas datos L0/L1/L2 según criterios → entra al cálculo en buffer posterior |
| **DESCARTADO: [id]** | No hay datos públicos verificables → el ítem se elimina del buffer |

**No acepto:** parafraseos interpretativos, “optimización asimétrica”, “umbrales internos”, ni rechazos sin investigar.

**Sí acepto:** fechas, números, autos/sentencias, BOE/CENDOC/TEDH, URLs, nº de pieza.

---

### Criterios MCN

| Capa | Mínimo |
|------|--------|
| **L0** | ≥2 señales: fecha + documento/sentencia/cita/URL |
| **L1** | Hecho o estadística con fuente explícita |
| **L2** | Inferencia + ≥1 evidencia L0/L1 en el mismo mensaje |
| **L3** | Cuarentena — no válido como respuesta final |

---

### Ítems en cuarentena (pegar desde cribado-*.json)

```
{{cuarentena_listado}}
```

Formato sugerido por ítem:

```
#### Qn — `[id]` | ranura: `[ranura]`
Texto original: …
Qué solidificar: [checklist concreto del operador]
```

---

### Formato de respuesta obligatorio

Ver plantilla en `docs/prompts/limpiar_cuarentena_recibir.md`. Responder **ítem por ítem** en ese formato.

---

### Contexto ya cargado (no contar como novedad)

```
{{items_ya_cargados}}
```

---

### Prioridad

Si existe evidencia pública del **caso foco**, incluirla en Q4 (ventanas) o Q3 (acusación). Si no existe, declararlo y no inventar.

---

## FIN DEL PROMPT
