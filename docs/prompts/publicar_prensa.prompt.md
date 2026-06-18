# Prompt — Publicar pieza en prensa

Orquestador para agentes: **analizar pack** → **rellenar lienzo** → **depositar en el repo**.

El operador rellena el bloque inferior y entrega este prompt junto al prompt de análisis referenciado.

---

## ORDEN (rellenar)

```
Crea [TIPO_PIEZA] para el caso [CASO_ID] basado en [PROMPT_ANALISIS].
Pack: [ruta al pack descomprimido].
Slug: [slug-kebab-case].
```

| Variable | Ejemplo |
|----------|---------|
| `TIPO_PIEZA` | `redes` · `articulo` · `sintesis` · `libre` |
| `CASO_ID` | `zapatero-plus-ultra` |
| `PROMPT_ANALISIS` | `docs/prompts/lectura_pack_ciudadano.prompt.md` |
| Pack | carpeta del ZIP descomprimido o nombre del ZIP |
| Slug | `update-m5-redes-jun26` |

---

## Fase A — Análisis (pack cerrado)

Seguir **íntegramente** el prompt de análisis indicado en `PROMPT_ANALISIS` (perímetro = solo archivos del pack).

Salida interna: mapa justicia ↔ política, cifras con archivo→campo, hechos para el relato.

---

## Fase B — Publicación (repo)

### Dónde localizar el caso en prensa

| Concepto | Ruta repo | URL tras `medidor build` |
|----------|-----------|--------------------------|
| Catálogo | `data/catalog.json` | `/prensa/index.html` |
| Ficha caso | `data/casos/{CASO_ID}/caso.json` | `/prensa/caso/{CASO_ID}.html` |
| Ficha medición | — | `/prensa/medicion/{MN}.html` |
| Pack | `public/prensa/downloads/{CASO_ID}-{MN}.zip` | mismo path en web |

### Drop zone (escribir aquí)

```
data/casos/{CASO_ID}/prensa/publicaciones/{slug}/
  meta.json
  cuerpo.html
```

- `slug` = kebab-case, único por caso; debe coincidir con `id` en `meta.json`.
- No editar `public/` a mano.

### Lienzos (solo lectura)

| Tipo | Lienzo repo | `cuerpo.html` |
|------|-------------|---------------|
| `articulo` · `sintesis` · `libre` | `site/templates/prensa/lienzo_fragmento.html` | Fragmento dentro de `<article class="pieza-agente">` |
| `redes` | `site/assets/prensa/plantilla_redes_lawfare.html` | HTML completo 1080×1080 sustituyendo `{{PLACEHOLDERS}}` |

Estilos prensa: `site/assets/prensa/style.css`. En artículo/síntesis **no** redefinir cabecera ni pie (el build los añade).

### `meta.json`

```json
{
  "id": "update-m5-redes-jun26",
  "caso_id": "zapatero-plus-ultra",
  "medicion_ref": "M9",
  "tipo": "redes",
  "titulo": "Actualización desde M5",
  "fecha": "2026-06-18",
  "prompt_analisis": "docs/prompts/lectura_pack_ciudadano.prompt.md",
  "pack_ref": "zapatero-plus-ultra-M9.zip",
  "lienzo": "site/assets/prensa/plantilla_redes_lawfare.html",
  "resumen": "Una línea para listados en la ficha del caso"
}
```

- `medicion_ref`: opcional; si existe, la pieza se lista también en la ficha de esa medición.
- `borrador: true` → no se publica en web (solo validación local).

---

## Mapa de campos — tipo `redes`

**Prohibido** inventar «índice de tensión» u otras etiquetas que no estén en el pack.

| Placeholder | Origen pack | Notas |
|-------------|-------------|-------|
| `{{INTENSIDAD}}` | `medicion/MN.json` → `intensidad` | Única cifra del titular principal |
| `{{LECTURA_ESCALA}}` | `medicion/MN.json` → `lectura` | Texto de escala del artefacto |
| `{{POLO_JUSTICIA}}` | media(`ejes.integridad`, `ejes.ventana`) | 2 decimales |
| `{{POLO_CONTEXTO}}` | media(`ejes.sincronia`, `ejes.impacto`) | 2 decimales |
| `{{POLO_JUSTICIA_BAR_PCT}}` | `POLO_JUSTICIA * 10` | entero 0–100 |
| `{{POLO_CONTEXTO_BAR_PCT}}` | `POLO_CONTEXTO * 10` | entero 0–100 |
| `{{SUBTITULO_HUECO}}` | redacción | Una línea: contraste justicia/política con cifras |
| `{{PARRAFO_1}}` · `{{PARRAFO_2}}` | hechos del pack | Sin jerga MCS/MCN/buffers |
| `{{CASO_ETIQUETA}}` | `caso.json` → `etiqueta` | |
| `{{MEDICION_ID}}` | `medicion/MN.json` → `id` | |
| `{{FECHA}}` | `meta.fecha` o fecha del informe | |
| `{{SELLO}}` | opcional | 2–4 palabras (ej. «Tensión medida») |

Pack solo medición: no hay `estado.json`; no inventar M0 ni deltas anteriores.

---

## Checklist antes de entregar

- [ ] Cada cifra trazable a un archivo del pack
- [ ] `caso_id` e `id` coherentes con rutas
- [ ] `cuerpo.html` según lienzo del `tipo`
- [ ] Operador ejecutará: `medidor prensa validate --caso {CASO_ID} --slug {slug}` y `medidor build --target prensa`

---

## FIN DEL PROMPT
