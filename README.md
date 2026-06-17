# Medidor de Lawfare

**Artefacto** FOSS (GPL-3.0) para cuantificar indicios de lawfare en casos concretos, y **centro de datos** donde se publican las mediciones que produce.

**Web:** https://alephscriptorium-eng.github.io/medidor-lawfare · **Versión:** 1.0.0

---

## Qué es esto

El repositorio tiene dos caras que comparten el mismo motor Python:

| Cara | Qué es | Dónde vive |
|------|--------|------------|
| **Artefacto** | Herramienta reproducible de medición (ejes, intensidad, cribado MCN, deltas) | `medidor_lawfare/`, `data/`, CLI `medidor` |
| **Centro de datos** | Registro público de resultados del artefacto aplicado a casos concretos | `data/catalog.json`, `public/prensa/` |

Un caso publicado (p. ej. *Zapatero / Plus Ultra*) es una **medición ilustrativa** en el catálogo, no el objeto del repositorio. El proyecto es el artefacto y el flujo que genera esas mediciones.

### El artefacto incluye

- **5 ejes observables** + intensidad global (0–10)
- **Buffers de contexto** (MCS-N) cribados epistemológicamente (capas L0–L3)
- **Registro de deltas** entre mediciones consecutivas (RDB)

Metodología: `docs/metodologia/` · Documentación técnica publicada: `public/foss/`

---

## La web: `site/` → `public/`

La web es estática y se **genera**, no se edita a mano en `public/`.

```
data/ (JSON)  +  site/ (plantillas Jinja2 + CSS)
        ↓
   medidor build
        ↓
     public/  →  GitHub Pages
```

| Carpeta | Rol | ¿Editar? |
|---------|-----|----------|
| `site/` | Plantillas y assets fuente | Sí |
| `public/` | HTML generado listo para publicar | No — regenerar con `medidor build` |

Los paquetes de datos se generan con `medidor build` en `public/prensa/downloads/`.

Los paquetes ZIP de datos (por medición y por caso) se generan en `public/prensa/downloads/` con `medidor build`.

### Tres portales en `public/`

| Portal | Ruta | Contenido |
|--------|------|-----------|
| **Índice** | `public/index.html` | Puerta de entrada a prensa y FOSS |
| **Centro de datos** | `public/prensa/` | Catálogo, fichas de caso, mediciones M0…MN |
| **Artefacto (FOSS)** | `public/foss/` | Operación, esquemas, devops, licencia |

El catálogo prensa se alimenta de `data/catalog.json`, sincronizado desde los estados de cada caso.

### Primera medición en el catálogo

La entrada inaugural (*Zapatero / Plus Ultra*, M0→M4, activa **M4** = 6.68/10) ilustra el funcionamiento del artefacto. Ficha: [zapatero-plus-ultra](public/prensa/caso/zapatero-plus-ultra.html).

---

## Ciclo operativo

Flujo estándar para cualquier `caso_id`:

```
1. docs/sesiones/buffer-NN.md       ← conversación con agente u operador
2. data/buffers/MCS-N-entrada.json  ← conversión estructurada
3. medidor cribar … --caso <id>     ← preview MCN + cribado-*.json
4. medidor commit … --caso <id>     ← estado.json + nueva medición + delta
5. pytest
6. medidor catalog sync             ← data/catalog.json
7. medidor build --target all       ← public/
8. git push main                    ← GitHub Pages (si activo)
```

Los buffers ya confirmados son **inmutables** (append-only). La cuarentena L3 no se reescribe: se resuelve con buffers posteriores.

### Capas del flujo

| Capa | Carpeta | Función |
|------|---------|---------|
| Prompts reutilizables | `docs/prompts/` | Plantillas para agentes externos (`{{variables}}`) |
| Sesiones | `docs/sesiones/` | Bitácora conversacional por buffer (`buffer-NN.md`) |
| Entrada machine | `data/buffers/` | JSON que consume el motor |
| Estado del caso | `data/casos/<id>/` | `caso.json`, `estado.json`, `cribados/` |
| Catálogo | `data/catalog.json` | Índice prensa (generado) |
| Web | `public/` | Salida renderizada |

### Prompts (`docs/prompts/`)

| Archivo | Uso |
|---------|-----|
| `llenar_buffer.md` | Pedir un **nuevo buffer** MCS-N a un agente externo |
| `limpiar_cuarentena_pedir.md` | Solicitar datos para ítems en cuarentena L3 |
| `limpiar_cuarentena_recibir.md` | Formato de respuesta + reglas de conversión a JSON |

### Sesiones (`docs/sesiones/`)

Cada `buffer-NN.md` documenta el origen conversacional de un MCS-N. Correspondencia en el caso inaugural:

| Sesión | Buffer | Medición |
|--------|--------|----------|
| `buffer-01.md` | MCS-1 | M1 (5.0 → 6.4) |
| `buffer-02.md` | MCS-2 | M2 (6.4 → 6.5) |
| `buffer-03.md` | MCS-3 | M3 (+0.06, solidificación parcial cuarentena) |
| `buffer-04.md` | MCS-4 | M4 (+0.12, investigación ampliada) |

`sesion-01.md` es archivo histórico del diseño inicial del sensor; no forma parte del pipeline operativo.

---

## Instalación

**Requisitos:** Python 3.9+, pip

```bash
pip install -e ".[dev]"
```

## Comandos CLI

```bash
# Cribar buffer entrante (preview + guarda cribado-*.json)
medidor cribar data/buffers/MI-BUFFER.json --caso <caso-id>

# Confirmar buffer y recalcular medición
medidor commit data/buffers/MI-BUFFER.json --caso <caso-id>

# Sincronizar catálogo desde estados
medidor catalog sync

# Regenerar sitios (no editar public/ a mano)
medidor build --target all
```

## Estructura del repositorio

```
data/                          # Fuente de verdad (casos, buffers, esquemas, catálogo)
medidor_lawfare/               # Paquete Python
├── mcn/                       # Cribado epistemológico L0–L3
├── motor/                     # Ejes e intensidad
├── rdb/                       # Estado y deltas
├── catalog/                   # Sincronización del catálogo
├── cli/                       # cribar, commit, build, catalog sync
└── site/                      # Contexto Jinja (prensa, foss)

docs/
├── metodologia/               # Marco, ejes, L0–L3, limitaciones
├── prompts/                   # Plantillas para agentes externos
└── sesiones/                  # Origen conversacional por buffer

site/                          # Plantillas Jinja2 + CSS (fuente de la web)
public/                        # Salida generada (GitHub Pages)
tests/                         # Regresión M0–M4
```

## GitHub Pages

El workflow `.github/workflows/pages.yml` publica el contenido de `public/` en cada push a `main` (sin build en CI — el HTML debe estar generado y commiteado).

1. [Settings → Pages](https://github.com/alephscriptorium-eng/medidor-lawfare/settings/pages) → **GitHub Actions**
2. Tras activar, cada push a `main` despliega `public/`

## Tests

```bash
pytest
```

## Para agentes LLM

Contexto operativo detallado (reglas epistemológicas, correspondencias, convenciones de commit): [`llms.md`](llms.md).

## Licencia y citación

GPL-3.0 — [LICENSE](LICENSE) · [CITATION.cff](CITATION.cff)
