# SPDX-License-Identifier: GPL-3.0-or-later
"""CLI: medidor build — genera public/prensa y public/foss."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from medidor_lawfare import __version__
from medidor_lawfare.catalog.sync import cargar_catalog, sincronizar_catalog
from medidor_lawfare.rdb.estado import listar_casos
from medidor_lawfare.paths import (
    CASOS_DIR,
    LICENSE,
    PUBLIC_DIR,
    PUBLIC_FOSS,
    PUBLIC_PRENSA,
    SITE_DIR,
    estado_path,
)


def _jinja_env(subdir: str) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(SITE_DIR / "templates" / subdir)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _copiar_assets(subdir: str, dest: Path) -> None:
    src = SITE_DIR / "assets" / subdir
    if src.exists():
        shutil.copytree(src, dest / "assets", dirs_exist_ok=True)


def _cargar_estados() -> dict[str, dict]:
    estados: dict[str, dict] = {}
    for caso_path in sorted(CASOS_DIR.iterdir()):
        if not caso_path.is_dir():
            continue
        ep = caso_path / "estado.json"
        if ep.exists():
            with open(ep, encoding="utf-8") as f:
                estados[caso_path.name] = json.load(f)
    return estados


def build_prensa() -> None:
    catalog = cargar_catalog()
    estados = _cargar_estados()
    env = _jinja_env("prensa")
    PUBLIC_PRENSA.mkdir(parents=True, exist_ok=True)
    _copiar_assets("prensa", PUBLIC_PRENSA)

    ctx_base = {
        "version": __version__,
        "catalog": catalog,
        "estados": estados,
        "brand": "Medidor de Lawfare",
    }

    (PUBLIC_PRENSA / "index.html").write_text(
        env.get_template("index.html").render(**ctx_base),
        encoding="utf-8",
    )
    (PUBLIC_PRENSA / "artefacto.html").write_text(
        env.get_template("artefacto.html").render(**ctx_base),
        encoding="utf-8",
    )

    medicion_dir = PUBLIC_PRENSA / "medicion"
    medicion_dir.mkdir(exist_ok=True)
    for med in catalog.get("mediciones_publicas", []):
        med_id = med["id"]
        caso_id = med["caso_id"]
        estado = estados.get(caso_id, {})
        mediciones_list = list(estado.get("mediciones", {}).values())
        medicion_estado = next((m for m in mediciones_list if m["id"] == med_id), {})
        (medicion_dir / f"{med_id}.html").write_text(
            env.get_template("medicion.html").render(
                **ctx_base,
                med=med,
                medicion=medicion_estado,
                estado=estado,
                mediciones=mediciones_list,
                deltas=estado.get("deltas", []),
            ),
            encoding="utf-8",
        )

    caso_dir = PUBLIC_PRENSA / "caso"
    caso_dir.mkdir(exist_ok=True)
    for caso in catalog.get("casos", []):
        caso_id = caso["id"]
        estado = estados.get(caso_id, {})
        (caso_dir / f"{caso_id}.html").write_text(
            env.get_template("caso.html").render(
                **ctx_base,
                caso=caso,
                estado=estado,
                mediciones=list(estado.get("mediciones", {}).values()),
                deltas=estado.get("deltas", []),
            ),
            encoding="utf-8",
        )


def build_foss() -> None:
    catalog = cargar_catalog()
    estados = _cargar_estados()
    env = _jinja_env("foss")
    PUBLIC_FOSS.mkdir(parents=True, exist_ok=True)
    _copiar_assets("foss", PUBLIC_FOSS)

    ctx_base = {
        "version": __version__,
        "catalog": catalog,
        "estados": estados,
        "brand": "Medidor de Lawfare",
        "license_text": LICENSE.read_text(encoding="utf-8") if LICENSE.exists() else "",
    }

    pages = [
        "index.html",
        "tecnico.html",
        "funcional.html",
        "datos-publicados.html",
        "devops.html",
        "LICENSE.html",
    ]
    for page in pages:
        (PUBLIC_FOSS / page).write_text(
            env.get_template(page).render(**ctx_base),
            encoding="utf-8",
        )


def build_root() -> None:
    """Índice DRY en public/ para GitHub Pages."""
    env = _jinja_env("root")
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    _copiar_assets("root", PUBLIC_DIR)
    ctx = {
        "version": __version__,
        "brand": "Medidor de Lawfare",
    }
    (PUBLIC_DIR / "index.html").write_text(
        env.get_template("index.html").render(**ctx),
        encoding="utf-8",
    )


def run_build(target: str = "all") -> None:
    if not listar_casos():
        raise FileNotFoundError("No hay casos en data/casos/")
    sincronizar_catalog()
    if target in ("all", "prensa", "foss"):
        build_root()
        print(f"Índice raíz generado en {PUBLIC_DIR / 'index.html'}")
    if target in ("all", "prensa"):
        build_prensa()
        print(f"Prensa generada en {PUBLIC_PRENSA}")
    if target in ("all", "foss"):
        build_foss()
        print(f"FOSS generado en {PUBLIC_FOSS}")
