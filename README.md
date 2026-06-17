# Medidor de Lawfare

**Artefacto** FOSS (GPL-3.0) para cuantificar indicios de lawfare en casos concretos, y **centro de datos** donde se publican las mediciones que produce.

Web: https://alephscriptorium-eng.github.io/medidor-lawfare

**Versión:** 1.0.0

## El artefacto

Herramienta reproducible con:

- 5 ejes observables + intensidad global (0–10)
- Buffers de contexto cribados epistemológicamente (L0–L3)
- Registro de deltas entre mediciones

Documentación técnica: `public/foss/` · Metodología: `docs/metodologia/`

## Centro de datos

El catálogo de mediciones publicadas vive en `data/catalog.json` y se expone en `public/prensa/`. Cada entrada es un resultado del artefacto aplicado a un caso — no el objeto del repositorio en sí.

| Portal | URL generada | Audiencia |
|--------|--------------|-----------|
| Índice | `public/index.html` | Entrada a prensa y FOSS |
| Prensa | `public/prensa/` | Catálogo de mediciones |
| FOSS | `public/foss/` | Artefacto, operación, esquemas |

### Primera medición en el catálogo

La medición inaugural (*Zapatero / Plus Ultra*, M0→M2) ilustra el funcionamiento del artefacto. Sus fichas están en el centro de datos; ver [ficha del registro](public/prensa/caso/zapatero-plus-ultra.html).

## Requisitos

- Python 3.9+
- pip

## Instalación

```bash
pip install -e ".[dev]"
```

## Comandos CLI

```bash
# Cribar buffer entrante
medidor cribar data/buffers/MI-BUFFER.json --caso <caso-id>

# Confirmar buffer y recalcular
medidor commit data/buffers/MI-BUFFER.json --caso <caso-id>

# Sincronizar catálogo desde estados
medidor catalog sync

# Regenerar sitios (no editar public/ a mano)
medidor build --target all
```

## Estructura

```
data/              # Catálogo, casos medidos, buffers, esquemas
medidor_lawfare/   # Paquete Python (MCN, motor, RDB, CLI)
docs/              # Metodología
site/              # Plantillas
public/            # Salida publicada (GitHub Pages)
```

## GitHub Pages

1. [Settings → Pages](https://github.com/alephscriptorium-eng/medidor-lawfare/settings/pages) → **GitHub Actions**
2. El workflow `.github/workflows/pages.yml` publica `public/` en cada push a `main`

## Tests

```bash
pytest
```

## Licencia y citación

GPL-3.0 — [LICENSE](LICENSE) · [CITATION.cff](CITATION.cff)
