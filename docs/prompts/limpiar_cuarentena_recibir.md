# Prompt — Limpiar cuarentena (formato de recepción)

Formato que debe devolver el agente externo. El operador guarda la respuesta en `docs/sesiones/buffer-NN.md` (sección RESOLUCIÓN) y convierte ítems SOLIDIFICAR a `data/buffers/MCS-N-entrada.json` o buffer siguiente (p. ej. MCS-3).

---

## Plantilla de respuesta del agente

```markdown
## RESOLUCIÓN CUARENTENA {{buffer_id}}

### Q1 [id-item]
ESTADO: SOLIDIFICAR | DESCARTADO: id-item
CAPA: L0 | L1 | L2
RANURA: [ranura_mcs]
DATOS:
- procedimiento: …
- fecha: …
- juzgado: …
- fuente: …
EVIDENCIA: [cita ≤25 palabras | URL | BOE/TEDH/CGPJ]

### Q2 [id-item]
…

## RESUMEN
- Solidificados: N/M
- Descartados: N/M
- L0: N | L1: N | L2: N
```

---

## Reglas de conversión (operador / LLM interno)

1. **DESCARTADO** → no incluir en JSON de buffer; opcional: nota en `buffer-NN.md`.
2. **SOLIDIFICAR L0/L1** → un ítem por hecho en `buffer_entrada.items[]`:
   ```json
   {
     "texto": "Hecho con fecha y fuente embebida en una frase",
     "ranura_sugerida": "ventanas_temporales",
     "bloque": "solidificacion_cuarentena",
     "ref_cuarentena": "id-item"
   }
   ```
3. **SOLIDIFICAR L2** → texto con conector inferencial (“por tanto”, “indica que”) + hechos L0/L1 en el mismo ítem o ítems enlazados.
4. Evitar frases que disparen L3 en el cribador (`mecánica estructural`, `pena de telediario`, `dejó de ser`, etc.).
5. Tras JSON: `medidor cribar` → revisar capas → `medidor commit` → `pytest` → `medidor catalog sync` → `medidor build --target all`.

---

## Validación mínima antes de commit

- [ ] Cada SOLIDIFICAR tiene fecha + fuente verificable
- [ ] No duplica ítems ya en buffers inmutables sin dato nuevo
- [ ] `caso_foco` en JSON coincide con `estado.json`
- [ ] `buffer_entrada.id` es el siguiente MCS-N (append-only)

---

## FIN
