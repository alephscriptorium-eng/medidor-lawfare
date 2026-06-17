# Extensión SLS v1.1 — MCN + PBM + RDB

Extensión del artefacto **SLS + MCS** para soportar buffers sucesivos sin perder el foco del caso ni sobrescribir buffers anteriores.

## Problema que resuelve

A partir del buffer 2, el agente puede aportar datos **no asépticos** (interpretación, inferencias, juicios). Hay que:

1. **Cribar y normalizar** antes de cargar.
2. **Conservar** el buffer 1 (`MCS-1`) intacto.
3. **Mantener el foco** en el caso medido (`ZAP-PU-2026-06-17`).
4. **Registrar deltas** por buffer para branching (subir / bajar / mixto).

---

## Módulos nuevos

### 1. MCN — Módulo de Cribado y Normalización

Clasifica cada ítem del buffer entrante en una capa epistemológica:

| Capa | Código | Descripción | Acción |
|------|--------|-------------|--------|
| Bruto verificable | `L0` | Fecha, cita textual, documento, sentencia, URL | Carga directa a ranura |
| Agregado con fuente | `L1` | Estadística o resumen con fuente explícita | Carga con peso 1.0 |
| Inferencia evidenciada | `L2` | Conclusión con ≥1 evidencia `L0`/`L1` enlazada | Carga con peso 0.7 |
| Interpretación agente | `L3` | Opinión, valoración, narrativa sin ancla | **Cuarentena** — no altera ejes |
| Contradicción interna | `Lx` | Ítem que contradice otro del mismo buffer | Marca conflicto; no carga hasta resolución |

**Regla de oro:** solo `L0`–`L2` entran al MCS. `L3` va a `cuarentena[]` y aparece en el informe pero **no mueve la aguja**.

**Salida del cribado** (por ítem):

```json
{
  "id": "item-uuid",
  "texto_original": "...",
  "capa": "L2",
  "ranura_destino": "patrones_acusacion",
  "evidencias": ["item-uuid-2"],
  "peso": 0.7,
  "accion": "cargar"
}
```

---

### 2. PBM — Parser de Buffers Múltiples

Los buffers son **apéndices**, no reemplazos. Estructura:

```json
{
  "buffer_entrada": {
    "id": "MCS-2",
    "tipo": "contexto_fino | contexto_historico | contexto_comparativo",
    "etiqueta": "descripción corta",
    "caso_foco": "ZAP-PU-2026-06-17",
    "fuente": "agente | usuario | documento",
    "items": [
      {
        "texto": "...",
        "ranura_sugerida": "cobertura_mediatica",
        "fuente": "opcional",
        "fecha": "opcional"
      }
    ]
  }
}
```

**Flujo del parser:**

```
buffer_entrada
    → MCN (cribado por ítem)
    → items_normalizados[] + cuarentena[]
    → validación caso_foco == estado.caso_foco.id
    → append a estado.buffers[] (inmutable tras commit)
    → recálculo SLS con buffers_activos del branch
    → registro delta en RDB
```

**Ranuras MCS** (heredadas del diseño original):

1. `historico_imputaciones`
2. `patrones_acusacion`
3. `cobertura_mediatica`
4. `ventanas_temporales`
5. `actores_recurrentes`
6. `precedentes_judiciales`
7. `vectores_politicos`
8. `intensidad_historica_comparable`
9. `meta_patrones_sistemicos`

---

### 3. RDB — Registro de Deltas y Branching

Cada buffer nuevo genera un nodo de medición y un delta respecto al anterior **en el mismo branch**.

```json
{
  "id": "D1→2",
  "desde": "M1",
  "hasta": "M2",
  "buffer_aplicado": "MCS-2",
  "delta_ejes": { "integridad": 0.0, "sincronia": 0.0, "ventana": 0.0, "impacto": 0.0, "vector": 0.0 },
  "delta_intensidad": 0.0,
  "direccion": "UP | DOWN | MIXED | NEUTRAL",
  "clasificacion_impacto": "eleva_lawfare | reduce_lawfare | ambiguo"
}
```

**Dirección del delta:**

| Condición | `direccion` |
|-----------|-------------|
| `delta_intensidad` > +0.3 | `UP` |
| `delta_intensidad` < −0.3 | `DOWN` |
| Ejes suben y bajan a la vez | `MIXED` |
| \|delta\| ≤ 0.3 | `NEUTRAL` |

**Branching:** si un buffer futuro contradice evidencialmente a `MCS-2`, se puede abrir branch:

```json
{
  "branch_id": "alt-mcs2-rechazado",
  "padre": "main",
  "buffers_activos": ["MCS-1"],
  "motivo": "MCS-2 en cuarentena por >40% L3"
}
```

El caso foco **nunca cambia** entre branches; solo cambia el contexto acumulado.

---

## Estado congelado (sesión 01)

| Medición | Buffers | Intensidad |
|----------|---------|------------|
| M0 (baseline) | ninguno | **5.0** |
| M1 (post MCS-1) | MCS-1 | **6.4** |
| Δ D0→1 | +1.4 | dirección **UP** |

`MCS-1` permanece en `estado.json` como inmutable.

---

## Formato para pegar el buffer 2

Puedes pegar texto libre o JSON. Si es texto libre, el parser intentará segmentar por párrafos/bloques y asignar ranuras. Si prefieres control fino, usa el JSON de arriba.

**Mínimo requerido:**

```
--- BUFFER MCS-2 ---
etiqueta: [nombre corto del buffer]
tipo: [contexto_fino | contexto_historico | contexto_comparativo]
items:
- [texto del ítem 1] → ranura: [nombre ranura opcional]
- [texto del ítem 2]
...
--- FIN BUFFER ---
```

El MCN cribará cada ítem, reportará cuántos quedan en L0/L1/L2 vs cuarentena L3, y recalculará **M2** mostrando el delta respecto a **M1**.

---

## Panel de salida esperado (tras buffer 2)

```
CASO FOCO: Zapatero / Plus Ultra (sin cambio)
BRANCH: main
BUFFERS ACTIVOS: MCS-1 + MCS-2

CRIBADO MCS-2:
  L0: n | L1: n | L2: n | L3 (cuarentena): n | Lx: n

MEDICIÓN M2:
  Integridad / Sincronía / Ventana / Impacto / Vector / Intensidad

DELTA D1→2:
  Δ por eje + dirección + clasificación_impacto
```
