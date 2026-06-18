# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests del subcatálogo prensa (publicaciones de agente)."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parent.parent
CASO_ID = "zapatero-plus-ultra"
EJEMPLO_SLUG = "_ejemplo"


@pytest.fixture
def schema() -> dict:
    with open(ROOT / "data/schema/publicacion.schema.json", encoding="utf-8") as f:
        return json.load(f)


def test_publicacion_schema_ejemplo(schema: dict) -> None:
    meta_path = (
        ROOT
        / f"data/casos/{CASO_ID}/prensa/publicaciones/{EJEMPLO_SLUG}/meta.json"
    )
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    jsonschema.validate(meta, schema)
    assert meta["borrador"] is True


def test_validar_ejemplo_borrador() -> None:
    from medidor_lawfare.site.prensa_publicaciones import validar_publicacion

    ok, errores = validar_publicacion(CASO_ID, EJEMPLO_SLUG)
    assert ok, errores


def test_listar_excluye_borradores() -> None:
    from medidor_lawfare.site.prensa_publicaciones import listar_publicaciones

    pubs = listar_publicaciones(CASO_ID, publicas=True)
    assert all(p["id"] != EJEMPLO_SLUG for p in pubs)


def test_sync_prensa_catalog_incluye_borrador() -> None:
    from medidor_lawfare.site.prensa_publicaciones import sync_prensa_catalog

    catalog = sync_prensa_catalog(CASO_ID)
    ids = {p["id"] for p in catalog["publicaciones"]}
    assert EJEMPLO_SLUG in ids
    borrador = next(p for p in catalog["publicaciones"] if p["id"] == EJEMPLO_SLUG)
    assert borrador["borrador"] is True


def test_href_desde_caso() -> None:
    from medidor_lawfare.site.prensa_publicaciones import listar_publicaciones

    pubs = listar_publicaciones(CASO_ID, publicas=False, desde="caso")
    ejemplo = next(p for p in pubs if p["id"] == EJEMPLO_SLUG)
    assert ejemplo["href"] == f"publicaciones/{EJEMPLO_SLUG}.html"


def test_campos_redes_desde_medicion() -> None:
    from medidor_lawfare.rdb.estado import cargar_estado
    from medidor_lawfare.site.prensa_publicaciones import campos_redes_desde_medicion

    estado = cargar_estado(CASO_ID)
    m9 = next(m for m in estado["mediciones"].values() if m["id"] == "M9")
    campos = campos_redes_desde_medicion(m9, "Zapatero Plus Ultra")
    assert campos["MEDICION_ID"] == "M9"
    assert "7,09" in campos["INTENSIDAD"]
    assert int(campos["POLO_JUSTICIA_BAR_PCT"]) == int(
        round((m9["ejes"]["integridad"] + m9["ejes"]["ventana"]) / 2 * 10)
    )


def test_build_no_publica_ejemplo(tmp_path: Path) -> None:
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    from medidor_lawfare.paths import SITE_DIR
    from medidor_lawfare.site.prensa_publicaciones import build_publicaciones_caso

    env = Environment(
        loader=FileSystemLoader([
            str(SITE_DIR / "templates" / "prensa"),
            str(SITE_DIR / "templates" / "_partials"),
        ]),
        autoescape=select_autoescape(["html", "xml"]),
    )
    out = tmp_path / "caso"
    out.mkdir()
    publicadas = build_publicaciones_caso(CASO_ID, env, out)
    assert all(p["id"] != EJEMPLO_SLUG for p in publicadas)
    assert not (out / "publicaciones" / f"{EJEMPLO_SLUG}.html").exists()


def test_cli_validate_ejemplo() -> None:
    from argparse import Namespace

    from medidor_lawfare.cli.prensa import run

    code = run(Namespace(caso=CASO_ID, slug=EJEMPLO_SLUG))
    assert code == 0
