# llms.md — Contexto para agentes LLM

Documento de onboarding para cualquier LLM que trabaje en este repositorio. **Leer antes de tocar código o datos.**

Repositorio: https://github.com/alephscriptorium-eng/medidor-lawfare  
Web (cuando Pages esté activo): https://alephscriptorium-eng.github.io/medidor-lawfare

---

## Qué es este proyecto

**Medidor de Lawfare** (`medidor-lawfare` v1.0.0) — **artefacto** FOSS (GPL-3.0) + **centro de datos** donde se publican sus mediciones.

- El **artefacto** cuantifica indicios de lawfare en un caso concreto (foco inmutable por medición).
- El **centro de datos** (`public/prensa/`, `data/catalog.json`) es el registro de resultados; no confundir un caso publicado con el objeto del repositorio.

Módulos: 5 ejes + intensidad, buffers MCS, MCN (L0–L3), RDB (deltas/branching).

**Presentación pública:** README, webs e índices deben enfatizar artefacto + catálogo. Zapatero/Plus Ultra es solo la **primera medición publicada** (ilustrativa), con ficha propia en prensa — no el tema del proyecto.

---

## Rama de trabajo

| Rama | Estado |
|------|--------|
| **`main`** | **Activa.** Todo el desarrollo va aquí. |
| `artefacto` | Referencia histórica (commit del motor). Mergeada a `main`. |
| `prensa` | Referencia histórica (catálogo + `public/`). Mergeada a `main`. |

No crear ramas de feature salvo petición explícita. No depender de rutas del prototipo `sls/` — ya no existe en `main`.

Push de las tres ramas (si hace falta sincronizar remotas):

```bash
git push -u origin main artefacto prensa
```

---

## CI / GitHub Actions

| Workflow | Archivo | Trigger | Estado |
|----------|---------|---------|--------|
| Deploy GitHub Pages | `.github/workflows/pages.yml` | push a `main` | **Requiere activación manual** |

El último run falló con `HttpError: Not Found` al crear el deployment — **GitHub Pages no está habilitado** en el repo. Para arreglarlo:

1. Ir a [Settings → Pages](https://github.com/alephscriptorium-eng/medidor-lawfare/settings/pages)
2. **Build and deployment → Source:** elegir **GitHub Actions** (no “Deploy from branch”)
3. Re-ejecutar el workflow fallido o hacer un push vacío a `main`

El workflow sube el contenido de `public/` tal cual (índice raíz + `prensa/` + `foss/`). No hay workflow de `pytest` aún; ejecutar tests en local antes de push.

**Nota git en este entorno:** si `git commit` falla con `opción trailer desconocida`, usar `/usr/bin/git` en lugar del wrapper de Homebrew.

---

## Estructura del repositorio

```
data/                          # Fuente de verdad
├── casos/
│   └── zapatero-plus-ultra/
│       ├── caso.json          # Metadatos del caso (inmutable)
│       ├── estado.json        # Mediciones, buffers, deltas, branches
│       └── cribados/
│           └── cribado-MCS-2.json
├── buffers/
│   └── MCS-2-entrada.json     # Buffer original del agente externo
├── schema/                    # JSON Schemas (estado, buffer, cribado, catalog, caso)
└── catalog.json               # Catálogo prensa (generado/sincronizado)

medidor_lawfare/               # Paquete Python instalable
├── mcn/cribador.py            # Cribado L0–L3, ranuras, parser de buffers
├── motor/
│   ├── ejes.py                # RANURA_EJES, redundancia, caps, pesos intensidad
│   └── intensidad.py          # lectura_intensidad()
├── rdb/
│   ├── estado.py              # cargar/guardar estado, commit_buffer()
│   └── deltas.py              # clasificar_delta()
├── catalog/sync.py            # sync_catalog() / sincronizar_catalog() → catalog.json
├── cli/
│   ├── main.py                # medidor cribar | commit | build | catalog sync
│   ├── cribar.py
│   ├── commit.py
│   └── build.py               # Jinja2 → public/index + public/prensa + public/foss
└── paths.py                   # Rutas centralizadas

docs/
├── metodologia/               # Marco, ejes, L0–L3, limitaciones, extension-mcn-rdb
└── sesiones/                  # sesion-01.md, buffer-01.md, buffer-02.md (origen conversacional)

site/                          # Plantillas Jinja2 + CSS (no editar public/ a mano)
public/                        # Salida generada (GitHub Pages despliega esto)

tests/test_regression.py       # M0=5.0, M1=6.4, M2=6.5, schema, cribado MCS-2
```

---

## Primera medición en catálogo (regresión / referencia)

`zapatero-plus-ultra` es la entrada **inaugural** del centro de datos (`caso.json` → `inaugural: true`). Se usa en tests y como ilustración; **no** define el alcance del codebase.

| Campo | Valor |
|-------|-------|
| `caso_id` | `zapatero-plus-ultra` |
| `caso_foco.id` | `ZAP-PU-2026-06-17` |
| Etiqueta pública | Zapatero / Plus Ultra |
| Inmutable (por medición) | sí |

### Mediciones de esa entrada

| ID | Intensidad | Lectura | Buffers activos |
|----|------------|---------|-----------------|
| **M0** | 5.0 | sospechas fundadas | — |
| **M1** | 6.4 | alta probabilidad de lawfare | MCS-1 |
| **M2** | 6.5 | alta probabilidad de lawfare | MCS-1, MCS-2 |

### Deltas registrados

| Delta | Δ intensidad | Dirección | Buffer |
|-------|--------------|-----------|--------|
| D0→1 | +1.4 | UP | MCS-1 — directorio histórico España 1978–2026 |
| D1→2 | +0.1 | NEUTRAL | MCS-2 — verificación empírica (mixto) |

**Por qué D1→2 es tan pequeño:** MCS-2 confirma MCS-1; descuento de redundancia (`REDUNDANCIA_MCS1 = 0.55`); 56% del buffer en cuarentena L3.

---

## Cuarentena MCS-2 (estado congelado, no es un bug)

Los 10 ítems L3 en cuarentena son **correctos por diseño**: el bloque interpretativo de `docs/sesiones/buffer-02.md` no tenía ancla verificable suficiente. Están registrados en `data/casos/zapatero-plus-ultra/cribados/cribado-MCS-2.json` y **no afectan M2**.

| Métrica | Valor |
|---------|-------|
| Ítems cargados | 8 (L0: 2, L1: 6) |
| Ítems en cuarentena | **10 (L3)** |
| pct_l3 | 0.56 |

### Ítems en cuarentena (IDs)

| ID | Ranura | Resumen |
|----|--------|---------|
| `5ae098d6` | meta_patrones_sistemicos | Dosieres prospectivos sin mandato (Kitchen/PISA) |
| `ad9fe6cf` | cobertura_mediatica | Filtración a medios en momento político |
| `afaf2846` | patrones_acusacion | Querella basada en recorte + alarma social |
| `4efd030c` | ventanas_temporales | Hitos 15–30 días antes de comicios |
| `e951031d` | ventanas_temporales | Archivo tardío post-objetivo político |
| `3d0a0138` | precedentes_judiciales | Tipificación para subir a AN/TS |
| `1171a6d9` | precedentes_judiciales | Forum shopping / juez natural |
| `98840122` | patrones_acusacion | Acusación popular vs archivo fiscal |
| `481c5cb8` | meta_patrones_sistemicos | “Pena de telediario” |
| `ea902be9` | meta_patrones_sistemicos | “Mecánica estructural” |

### Ya cargado (no repetir como novedad)

- Salvador Alba / Victoria Rosell (TSJC 2019, TS 2021)
- TEDH Bateragune / Otegi (6-nov-2018)
- Operación Cataluña: borrador UDEF 16-nov-2012, elecciones 25-nov-2012
- >20 querellas Podemos archivadas en ~6 años

---

## Próximo trabajo posible (cuarentena → solidificación)

Si el usuario aporta **datos verificables** del agente externo para ítems en cuarentena:

1. Recibir output (formato: SOLIDIFICAR con L0/L1/L2 por ítem, o DESCARTADO).
2. Convertir a buffer nuevo (`MCS-3` o patch documentado).
3. `medidor cribar … --caso zapatero-plus-ultra` — previsualizar.
4. `medidor commit …` — recalcula medición (probablemente **M3**, no M2').
5. `pytest` — no romper M0/M1/M2 **a menos que el usuario acepte recálculo**.
6. `medidor catalog sync` + `medidor build --target all`.

**Limitación del motor actual:** `commit_buffer()` solo **appendea** buffers nuevos (MCS-3, MCS-4…). No existe flujo de patch in-place sobre MCS-2. Opciones:

- **Opción A (recomendada):** Nuevo buffer `MCS-3` solo con ítems solidificados → M3 + delta D2→3
- **Opción B:** Extender MCN/commit para mergear cuarentena resuelta sin duplicar ranuras

Comparar IDs de cuarentena antes/después; no inventar L0.

## CLI — comandos esenciales

```bash
pip install -e ".[dev]"

# Cribar sin commit (preview + guarda cribado-*.json)
medidor cribar data/buffers/MI-BUFFER.json --caso <caso-id>
medidor commit data/buffers/MI-BUFFER.json --caso <caso-id>

# Sincronizar catálogo prensa
medidor catalog sync

# Regenerar sitios estáticos (NO editar public/ manualmente)
medidor build --target all

# Tests
pytest
```

---

## Reglas epistemológicas (MCN)

| Capa | Entra al cálculo | Criterio heurístico |
|------|------------------|---------------------|
| L0 | sí (peso 1.0) | ≥2 señales: fecha + sentencia/documento/URL/cita |
| L1 | sí (peso 1.0) | Dato con fuente explícita |
| L2 | sí (peso 0.7) | Inferencia con conectores (“por tanto”, “indica que”) |
| L3 | **cuarentena** | Patrones interpretativos (“mecánica estructural”, “pena de telediario”, etc.) |
| Lx | conflicto | Contradicción interna — no carga |

Solo ítems con `accion: "cargar"` y ranura válida alteran ejes. Cuarentena aparece en informes pero **Δ = 0**.

Ranuras válidas: `historico_imputaciones`, `patrones_acusacion`, `cobertura_mediatica`, `ventanas_temporales`, `actores_recurrentes`, `precedentes_judiciales`, `vectores_politicos`, `intensidad_historica_comparable`, `meta_patrones_sistemicos`.

---

## Motor — constantes que no cambiar sin motivo

```python
REDUNDANCIA_MCS1 = 0.55   # buffers posteriores confirman MCS-1
CAP_DELTA_EJE = 0.55
CAP_DELTA_INTENSIDAD = 0.50
# Dirección delta: |Δ| > 0.3 → UP/DOWN; ≤ 0.3 → NEUTRAL
```

Tests de regresión fijan M0=5.0, M1=6.4, M2=6.5. Cualquier recálculo post-cuarentena debe documentar si cambia M2 o crea M3.

---

## Sitios generados

| Target | Rol | Destino |
|--------|-----|---------|
| Raíz | Índice artefacto + centro de datos | `public/index.html` |
| Prensa | Catálogo de mediciones | `public/prensa/` (`artefacto.html`, no `que-es`) |
| FOSS | Documentación del artefacto | `public/foss/` (`datos-publicados.html`, no `ejemplo-zapatero`) |

`medidor build --target all` regenera los tres targets. GitHub Actions (`.github/workflows/pages.yml`) despliega `public/` en cada push a `main` **una vez Pages esté activado**.

---

## Documentación de referencia

| Archivo | Contenido |
|---------|-----------|
| `docs/metodologia/marco.md` | Marco conceptual |
| `docs/metodologia/ejes.md` | Definición de ejes |
| `docs/metodologia/epistemologia-L0-L3.md` | Capas epistemológicas |
| `docs/metodologia/extension-mcn-rdb.md` | Especificación MCN + RDB |
| `docs/metodologia/limitaciones.md` | Limitaciones conocidas |
| `docs/sesiones/buffer-01.md` | Origen MCS-1 (directorio Gemini) |
| `docs/sesiones/buffer-02.md` | Origen MCS-2 (interpretación + datos duros) |
| `docs/sesiones/sesion-01.md` | Log conversacional sesión 1 |
| `CHANGELOG.md` | Historial de releases |
| `README.md` | Instalación y uso humano |

---

## Qué NO hacer

- **No presentar el proyecto como “el caso Zapatero”** en README, webs ni docs de interfaz — es una medición del catálogo.
- **No editar `public/` a mano** — regenerar con `medidor build`.
- **No sobrescribir buffers inmutables** en `estado.json` — son append-only.
- **No cambiar `caso_foco`** — es inmutable por diseño.
- **No asumir rutas `sls/`** — migradas a `medidor_lawfare/` + `data/`.
- **No commitear sin que el usuario lo pida.**
- **No inventar datos L0** para sacar ítems de cuarentena — el usuario provee output del agente externo verificable.

---

## Migración desde prototipo

El prototipo inicial vivía en `sls/` (rama `artefacto`). En `main`:

| Antes (`sls/`) | Ahora |
|----------------|-------|
| `sls/estado.json` | `data/casos/zapatero-plus-ultra/estado.json` |
| `sls/parser.py` | `medidor_lawfare/mcn/cribador.py` |
| `sls/commit.py` | `medidor_lawfare/rdb/estado.py` + `cli/commit.py` |
| `sls/extension-mcn-rdb.md` | `docs/metodologia/extension-mcn-rdb.md` |
| `buffer-01/02.md` (raíz) | `docs/sesiones/` |
| — | `medidor_lawfare/cli/build.py`, `catalog/`, tests, schemas, sitios |

Funcionalidad preservada; añadidos empaquetado pip, schemas, tests, sitios prensa/foss, CI Pages.

---

## Checklist antes de cerrar una tarea

- [ ] `pytest` pasa
- [ ] `estado.json` valida contra `data/schema/estado.schema.json`
- [ ] Si hay cambio de medición: `medidor catalog sync`
- [ ] Si hay cambio publicable: `medidor build --target all`
- [ ] Documentar en CHANGELOG si es release-worthy
- [ ] Caso foco intacto; buffers previos intactos
- [ ] Si tocaste plantillas o datos: verificar que `public/` se regeneró con build

---

*Última actualización: 2026-06-17 — branch `main`, motor 1.0.0, Pages workflow pendiente de activación en repo.*
