# Medidor de Lawfare

Web: https://alephscriptorium-eng.github.io/medidor-lawfare

Herramienta FOSS (GPL-3.0) para **cuantificar indicios de lawfare** en un caso concreto, usando ejes observables, buffers de contexto cribados epistemológicamente (L0–L3) y registro de deltas entre mediciones.

**Versión:** 1.0.0

## Requisitos

- Python 3.9+
- pip

## Instalación

```bash
pip install -e ".[dev]"
```

## Comandos CLI

```bash
# Cribar un buffer entrante (MCN)
medidor cribar data/buffers/MCS-2-entrada.json --caso zapatero-plus-ultra

# Confirmar buffer y recalcular medición
medidor commit data/buffers/MCS-2-entrada.json --caso zapatero-plus-ultra

# Sincronizar catálogo prensa desde estados
medidor catalog sync

# Generar sitios estáticos
medidor build --target all    # prensa + foss
medidor build --target prensa
medidor build --target foss
```

## Estructura

```
data/           # Fuente de verdad: casos, buffers, esquemas, catálogo
medidor_lawfare/  # Paquete Python (MCN, motor, RDB, CLI)
docs/           # Metodología y sesiones de trabajo
site/           # Plantillas Jinja2 y CSS
public/         # Salida generada (prensa + foss)
```

## Sitios generados

- **Prensa:** `public/prensa/` — portal para periodistas y ciudadanía
- **FOSS:** `public/foss/` — documentación técnica para desarrolladores

Tras `medidor build --target all`, abrir `public/index.html` (índice raíz) o los portales `public/prensa/` y `public/foss/`.

### GitHub Pages

1. En [Settings → Pages](https://github.com/alephscriptorium-eng/medidor-lawfare/settings/pages), elegir **GitHub Actions** como origen.
2. El workflow `.github/workflows/pages.yml` publica el contenido de `public/` en cada push a `main`.
3. La URL raíz enlaza a prensa y FOSS sin duplicar contenido.

## Caso ejemplo

**Zapatero / Plus Ultra** — tres mediciones publicadas:

| ID | Intensidad | Lectura |
|----|------------|---------|
| M0 | 5.0 | sospechas fundadas |
| M1 | 6.4 | alta probabilidad de lawfare |
| M2 | 6.5 | alta probabilidad de lawfare |

## Tests

```bash
pytest
```

## Licencia

GNU General Public License v3.0 — ver [LICENSE](LICENSE) y [public/foss/LICENSE.html](public/foss/LICENSE.html).

## Citación

Ver [CITATION.cff](CITATION.cff).
