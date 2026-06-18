# Publicación de ejemplo (`_ejemplo`)

Carpeta de referencia para operadores y agentes. **No se publica en el build** mientras `meta.json` tenga `"borrador": true`.

## Crear una pieza real

1. Copiar esta carpeta a `data/casos/zapatero-plus-ultra/prensa/publicaciones/{slug}/`
2. Editar `meta.json`: quitar `borrador` o poner `false`, ajustar campos
3. Rellenar `cuerpo.html` según el `tipo` y el lienzo indicado en `meta.lienzo`
4. `medidor prensa validate --caso zapatero-plus-ultra --slug {slug}`
5. `medidor build --target prensa`

Ver `docs/prompts/publicar_prensa.prompt.md` para el protocolo completo.
