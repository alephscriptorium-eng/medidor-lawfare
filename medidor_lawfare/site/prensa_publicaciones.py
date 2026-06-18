# SPDX-License-Identifier: GPL-3.0-or-later
"""Publicaciones prensa por caso (drop zone → build estático)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
from jinja2 import Environment

from medidor_lawfare.paths import PROJECT_ROOT, SCHEMA_DIR, caso_dir
from medidor_lawfare.rdb.estado import cargar_estado

SCHEMA_PATH = SCHEMA_DIR / "publicacion.schema.json"
TIPOS_FRAGMENTO = frozenset({"articulo", "sintesis", "libre"})
TIPOS_REDES = frozenset({"redes"})


def publicaciones_dir(caso_id: str) -> Path:
    return caso_dir(caso_id) / "prensa" / "publicaciones"


def prensa_catalog_path(caso_id: str) -> Path:
    return caso_dir(caso_id) / "prensa" / "catalog.json"


def _cargar_schema() -> dict[str, Any]:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _slug_desde_carpeta(path: Path) -> str:
    return path.name


def _cargar_meta(slug_dir: Path) -> dict[str, Any] | None:
    meta_path = slug_dir / "meta.json"
    if not meta_path.exists():
        return None
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def _es_borrador(meta: dict[str, Any]) -> bool:
    return bool(meta.get("borrador"))


def validar_meta(meta: dict[str, Any], slug: str | None = None) -> list[str]:
    errores: list[str] = []
    try:
        jsonschema.validate(meta, _cargar_schema())
    except jsonschema.ValidationError as exc:
        errores.append(str(exc.message))
        return errores

    folder_slug = slug or meta.get("id", "")
    if meta.get("id") != folder_slug:
        errores.append(f"id en meta.json ({meta.get('id')!r}) no coincide con carpeta ({folder_slug!r})")

    caso_path = caso_dir(meta["caso_id"]) / "caso.json"
    if not caso_path.exists():
        errores.append(f"caso_id desconocido: {meta['caso_id']!r}")

    if meta.get("medicion_ref"):
        try:
            estado = cargar_estado(meta["caso_id"])
        except (FileNotFoundError, OSError):
            errores.append(f"no se pudo cargar estado de {meta['caso_id']!r}")
        else:
            meds = {m["id"] for m in estado.get("mediciones", {}).values()}
            if meta["medicion_ref"] not in meds:
                errores.append(
                    f"medicion_ref {meta['medicion_ref']!r} no existe en estado de {meta['caso_id']!r}"
                )

    return errores


def validar_publicacion(caso_id: str, slug: str) -> tuple[bool, list[str]]:
    slug_dir = publicaciones_dir(caso_id) / slug
    if not slug_dir.is_dir():
        return False, [f"no existe carpeta {slug_dir.relative_to(PROJECT_ROOT)}"]

    meta = _cargar_meta(slug_dir)
    if meta is None:
        return False, ["falta meta.json"]

    errores = validar_meta(meta, slug)
    if meta.get("caso_id") != caso_id:
        errores.append(f"caso_id en meta ({meta.get('caso_id')!r}) no coincide con --caso ({caso_id!r})")

    cuerpo = slug_dir / "cuerpo.html"
    if not cuerpo.exists():
        errores.append("falta cuerpo.html")

    return len(errores) == 0, errores


def _enriquecer_publicacion(
    meta: dict[str, Any],
    slug: str,
    *,
    desde: str = "caso",
    base_href: str = "",
) -> dict[str, Any]:
    tipo = meta["tipo"]
    caso_id = meta["caso_id"]
    if desde == "caso":
        href = f"publicaciones/{slug}.html"
        card_href = f"publicaciones/{slug}/card.html" if tipo in TIPOS_REDES else None
    elif desde == "medicion":
        href = f"{base_href}caso/{caso_id}/publicaciones/{slug}.html"
        card_href = (
            f"{base_href}caso/{caso_id}/publicaciones/{slug}/card.html"
            if tipo in TIPOS_REDES
            else None
        )
    else:
        href = f"caso/{caso_id}/publicaciones/{slug}.html"
        card_href = (
            f"caso/{caso_id}/publicaciones/{slug}/card.html" if tipo in TIPOS_REDES else None
        )
    return {
        **meta,
        "slug": slug,
        "href": href,
        "card_href": card_href,
    }


def listar_publicaciones(
    caso_id: str,
    *,
    publicas: bool = True,
    desde: str = "caso",
    base_href: str = "",
) -> list[dict[str, Any]]:
    root = publicaciones_dir(caso_id)
    if not root.is_dir():
        return []

    publicaciones: list[dict[str, Any]] = []
    for slug_dir in sorted(root.iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = _slug_desde_carpeta(slug_dir)
        meta = _cargar_meta(slug_dir)
        if meta is None:
            continue
        if publicas and _es_borrador(meta):
            continue
        if meta.get("caso_id") != caso_id:
            continue
        publicaciones.append(_enriquecer_publicacion(meta, slug, desde=desde, base_href=base_href))

    publicaciones.sort(key=lambda p: (p.get("fecha", ""), p.get("id", "")), reverse=True)
    return publicaciones


def publicaciones_para_medicion(
    caso_id: str,
    med_id: str,
    *,
    publicas: bool = True,
    base_href: str = "../",
) -> list[dict[str, Any]]:
    return [
        p
        for p in listar_publicaciones(
            caso_id, publicas=publicas, desde="medicion", base_href=base_href
        )
        if p.get("medicion_ref") == med_id
    ]


def sync_prensa_catalog(caso_id: str) -> dict[str, Any]:
    root = publicaciones_dir(caso_id)
    root.parent.mkdir(parents=True, exist_ok=True)

    entradas: list[dict[str, Any]] = []
    if root.is_dir():
        for slug_dir in sorted(root.iterdir()):
            if not slug_dir.is_dir():
                continue
            slug = _slug_desde_carpeta(slug_dir)
            meta = _cargar_meta(slug_dir)
            if meta is None:
                continue
            entradas.append(
                {
                    "id": meta.get("id", slug),
                    "slug": slug,
                    "tipo": meta.get("tipo"),
                    "titulo": meta.get("titulo"),
                    "fecha": meta.get("fecha"),
                    "medicion_ref": meta.get("medicion_ref"),
                    "resumen": meta.get("resumen"),
                    "borrador": _es_borrador(meta),
                }
            )

    catalog = {
        "caso_id": caso_id,
        "generado": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publicaciones": entradas,
    }
    dest = prensa_catalog_path(caso_id)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return catalog


def _leer_cuerpo(slug_dir: Path) -> str:
    return (slug_dir / "cuerpo.html").read_text(encoding="utf-8")


def _nombre_caso(caso_id: str) -> str:
    path = caso_dir(caso_id) / "caso.json"
    if not path.exists():
        return caso_id
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    return meta.get("etiqueta", caso_id)


def render_publicacion_pagina(
    env: Environment,
    caso_id: str,
    slug: str,
    meta: dict[str, Any],
    ctx: dict[str, Any] | None = None,
) -> str:
    pub = _enriquecer_publicacion(meta, slug, desde="prensa")
    cuerpo = ""
    es_redes = meta["tipo"] in TIPOS_REDES
    if not es_redes:
        cuerpo = _leer_cuerpo(publicaciones_dir(caso_id) / slug)
    render_ctx: dict[str, Any] = {
        "pub": pub,
        "cuerpo": cuerpo,
        "es_redes": es_redes,
        "caso_nombre": _nombre_caso(caso_id),
        "base_href": "../../../",
        "prensa_href": "../../index.html",
        "portal_href": "../../../index.html",
        "show_inicio": True,
    }
    if ctx:
        render_ctx = {**ctx, **render_ctx}
    return env.get_template("publicacion.html").render(**render_ctx)


def build_publicaciones_caso(
    caso_id: str,
    env: Environment,
    out_caso_dir: Path,
    ctx: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    sync_prensa_catalog(caso_id)
    publicadas: list[dict[str, Any]] = []
    root = publicaciones_dir(caso_id)
    if not root.is_dir():
        return publicadas

    pub_out = out_caso_dir / "publicaciones"
    pub_out.mkdir(parents=True, exist_ok=True)

    for slug_dir in sorted(root.iterdir()):
        if not slug_dir.is_dir():
            continue
        slug = _slug_desde_carpeta(slug_dir)
        meta = _cargar_meta(slug_dir)
        if meta is None or _es_borrador(meta):
            continue
        if meta.get("caso_id") != caso_id:
            continue

        errores = validar_meta(meta, slug)
        if errores:
            print(f"  ⚠ publicación {caso_id}/{slug} omitida: {'; '.join(errores)}")
            continue

        tipo = meta["tipo"]
        if tipo in TIPOS_REDES:
            card_dir = pub_out / slug
            card_dir.mkdir(parents=True, exist_ok=True)
            (card_dir / "card.html").write_text(_leer_cuerpo(slug_dir), encoding="utf-8")

        (pub_out / f"{slug}.html").write_text(
            render_publicacion_pagina(env, caso_id, slug, meta, ctx=ctx),
            encoding="utf-8",
        )
        publicadas.append(_enriquecer_publicacion(meta, slug, desde="caso"))

    return publicadas


def campos_redes_desde_medicion(medicion: dict[str, Any], caso_etiqueta: str) -> dict[str, str]:
    """Mapa de placeholders para plantilla_redes_lawfare.html desde medición del estado."""
    ejes = medicion.get("ejes", {})
    polo_justicia = round((ejes.get("integridad", 0) + ejes.get("ventana", 0)) / 2, 2)
    polo_contexto = round((ejes.get("sincronia", 0) + ejes.get("impacto", 0)) / 2, 2)
    intensidad = medicion.get("intensidad", 0)
    return {
        "CASO_ETIQUETA": caso_etiqueta,
        "MEDICION_ID": medicion.get("id", ""),
        "INTENSIDAD": f"{intensidad:.2f}".replace(".", ","),
        "POLO_JUSTICIA": f"{polo_justicia:.2f}".replace(".", ","),
        "POLO_JUSTICIA_BAR_PCT": str(int(round(polo_justicia * 10))),
        "POLO_CONTEXTO": f"{polo_contexto:.2f}".replace(".", ","),
        "POLO_CONTEXTO_BAR_PCT": str(int(round(polo_contexto * 10))),
        "LECTURA_ESCALA": "ESCALA 0–10",
        "SUBTITULO_HUECO": medicion.get("lectura", ""),
    }
