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
│           ├── cribado-MCS-1.json
│           ├── cribado-MCS-2.json
│           ├── cribado-MCS-3.json
│           ├── cribado-MCS-4.json
│           └── cribado-MCS-5.json
├── buffers/
│   ├── MCS-1-entrada.json
│   ├── MCS-2-entrada.json
│   ├── MCS-3-entrada.json
│   ├── MCS-4-entrada.json
│   └── MCS-5-entrada.json
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
│   ├── main.py                # medidor cribar | commit | build | pack | catalog sync
│   ├── cribar.py
│   ├── commit.py
│   ├── pack.py                # ZIP por medición o caso → public/prensa/downloads/
│   └── build.py               # Jinja2 → public/index + public/prensa + public/foss
├── site/
│   └── packs.py               # Lógica de empaquetado (usada por build y pack)
└── paths.py                   # Rutas centralizadas

docs/
├── metodologia/               # Marco, ejes, L0–L3, limitaciones, extension-mcn-rdb
├── prompts/                   # Plantillas para agentes externos ({{variables}})
└── sesiones/                  # buffer-NN.md — origen conversacional por MCS-N

site/                          # Plantillas Jinja2 + CSS (no editar public/ a mano)
public/                        # Salida generada (GitHub Pages despliega esto)

tests/test_regression.py       # M0–M5, schema, cribado MCS-2
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
| **M3** | 6.56 | alta probabilidad de lawfare | MCS-1, MCS-2, MCS-3 |
| **M4** | 6.68 | alta probabilidad de lawfare | MCS-1, MCS-2, MCS-3, MCS-4 |
| **M5** | 6.79 | alta probabilidad de lawfare | MCS-1, MCS-2, MCS-3, MCS-4, MCS-5 |
| **M6** | 6.88 | alta probabilidad de lawfare | MCS-1, MCS-2, MCS-3, MCS-4, MCS-5, MCS-6 |

### Correspondencia sesión → buffer → medición (armónica)

| Sesión | MCS | Medición | Entrada JSON | Cribado |
|--------|-----|----------|--------------|---------|
| buffer-01.md | MCS-1 | **M1** | `MCS-1-entrada.json` | `cribado-MCS-1.json` (retroactivo) |
| buffer-02.md | MCS-2 | **M2** | `MCS-2-entrada.json` | `cribado-MCS-2.json` |
| buffer-03.md | MCS-3 | **M3** | `MCS-3-entrada.json` | `cribado-MCS-3.json` |
| buffer-04.md | MCS-4 | **M4** | `MCS-4-entrada.json` | `cribado-MCS-4.json` |
| buffer-05.md | MCS-5 | **M5** | `MCS-5-entrada.json` | `cribado-MCS-5.json` |
| buffer-06.md | MCS-6 | **M6** | `MCS-6-entrada.json` | `cribado-MCS-6.json` |

`buffer-03.md` incluye prompt + respuesta agente; solo la parte SOLIDIFICAR entra en MCS-3.

### Deltas registrados

| Delta | Δ intensidad | Dirección | Buffer |
|-------|--------------|-----------|--------|
| D0→1 | +1.4 | UP | MCS-1 |
| D1→2 | +0.1 | NEUTRAL | MCS-2 (56% L3 cuarentena) |
| D2→3 | +0.06 | NEUTRAL | MCS-3 — respuesta agente buffer-03 |
| D3→4 | +0.12 | NEUTRAL | MCS-4 — investigación buffer-04 |
| D4→5 | +0.11 | MIXED | MCS-5 — calendario electoral, PSOE, tensiones Sánchez–Trump/Musk (14% L3 cuarentena) |
| D5→6 | +0.09 | MIXED | MCS-6 — acusación Plus Ultra vista 17-jun-2026 y posiciones públicas |

**Medición activa en catálogo:** **M6** (6.88/10).

---

## Cuarentena MCS-2 (resuelta en M3 + M4)

La cuarentena original (10 L3 en `cribado-MCS-2.json`) se solidificó en **dos buffers**:

- **MCS-3** (buffer-03): 5 ítems del agente → M3 (+0.06)
- **MCS-4** (buffer-04): 9 ítems investigación ampliada → M4 (+0.12)

Cuarentena MCS-2 permanece como histórico; no se reescribe MCS-2 (inmutable).

Ítems originales en cuarentena (referencia): ver `cribado-MCS-2.json` o tabla en commits anteriores a MCS-3.

### Ya cargado en MCS-1/MCS-2 (no repetir como novedad)

- Salvador Alba / Victoria Rosell (TSJC 2019, TS 2021)
- TEDH Bateragune / Otegi (6-nov-2018)
- Operación Cataluña: borrador UDEF 16-nov-2012, elecciones 25-nov-2012
- >20 querellas Podemos archivadas en ~6 años

---

## Ciclo operativo completo (artefacto → prensa)

Flujo estándar para **cualquier** `caso_id` (Zapatero es el primer caso de uso, no un modo especial):

```
1. docs/sesiones/buffer-NN.md     ← agente externo o operador (markdown)
2. data/buffers/MCS-N-entrada.json ← conversión estructurada
3. medidor cribar … --caso <id>   ← preview MCN + cribado-*.json
4. medidor commit … --caso <id>   ← estado.json + M(N+1) + delta
5. pytest                         ← regresión
6. medidor catalog sync           ← data/catalog.json
7. medidor build --target all     ← public/ (prensa + foss + índice)
8. git push main                  ← GitHub Pages (si activo)
```

**Archivos tocados por medición nueva:**

| Artefacto | Ruta |
|-----------|------|
| Entrada conversacional | `docs/sesiones/buffer-NN.md` |
| Entrada machine | `data/buffers/MCS-N-entrada.json` |
| Estado | `data/casos/<caso-id>/estado.json` |
| Cribado | `data/casos/<caso-id>/cribados/cribado-MCS-N.json` |
| Catálogo | `data/catalog.json` |
| Prensa | `public/prensa/medicion/MN.html`, caso, índice |
| Paquetes ZIP | `public/prensa/downloads/<caso-id>.zip`, `<caso-id>-MN.zip` |

Los paquetes ZIP se generan en el paso 7 (`medidor build`) **o** bajo demanda con `medidor pack` (sin rebuild del sitio). Ver sección CLI.

**Solo generar un ZIP (agente / operador):** no hace falta levantar web ni `medidor build` completo si los datos en `data/` ya están actualizados:

```bash
pip install -e .
medidor pack --caso zapatero-plus-ultra              # caso completo
medidor pack --caso zapatero-plus-ultra --med M3   # una medición
# Salida por defecto: public/prensa/downloads/
```

Si el repo ya tiene `public/prensa/downloads/` commiteado, el archivo puede existir sin ejecutar nada.

---

## Prompts reutilizables (agentes externos)

Plantillas en `docs/prompts/` — sustituir `{{variables}}`; no acoplar al caso inaugural salvo en ejemplos.

| Archivo | Uso |
|---------|-----|
| `llenar_buffer.md` | Pedir un **nuevo buffer** MCS-N al agente |
| `limpiar_cuarentena_pedir.md` | Pedir datos para ítems L3 en cuarentena |
| `limpiar_cuarentena_recibir.md` | Formato de respuesta + reglas de conversión a JSON |

**Convención sesiones:** ver tabla «Correspondencia sesión → buffer → medición» arriba.

---

## Próximo trabajo posible

- Añadir otro `caso_id` bajo `data/casos/` (mismo flujo; tests nuevos).
- Workflow CI con `pytest` (aún no existe).
- Patch in-place de cuarentena (Opción B en metodología) — hoy solo append MCS-N.

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

# Paquetes ZIP de datos (medición o caso) sin rebuild completo
medidor pack --caso <caso-id> [--med M3] [--output dir]

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

Tests de regresión fijan M0=5.0 … M5=6.79.

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
| `docs/sesiones/buffer-04.md` | Origen MCS-3 (solidificación cuarentena) |
| `docs/prompts/` | Plantillas llenar_buffer / limpiar_cuarentena |
| `docs/sesiones/sesion-01.md` | Log conversacional sesión 1 |
| `CHANGELOG.md` | Historial de releases |
| `README.md` | Instalación y uso humano |

---

## Qué NO hacer

- **No presentar el proyecto como “el caso Zapatero”** en README, webs ni docs de interfaz — es una medición del catálogo.
- **No editar `public/` a mano** — regenerar con `medidor build`.
- Paquetes ZIP: `public/prensa/downloads/` — `medidor build` o `medidor pack --caso <id>`
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
