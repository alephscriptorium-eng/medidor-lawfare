# SPDX-License-Identifier: GPL-3.0-or-later
"""Sincronización de catalog.json desde estados de casos."""

from __future__ import annotations

import json
from typing import Any

from medidor_lawfare import __version__
from medidor_lawfare.paths import CATALOG_PATH, caso_dir
from medidor_lawfare.rdb.estado import cargar_estado, listar_casos


def cargar_catalog() -> dict[str, Any]:
    if not CATALOG_PATH.exists():
        return {"version": __version__, "mediciones_publicas": [], "casos": []}
    with open(CATALOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def guardar_catalog(catalog: dict[str, Any]) -> None:
    catalog["version"] = __version__
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)


def sync_catalog() -> dict[str, Any]:
    catalog = cargar_catalog()
    casos_map: dict[str, dict[str, Any]] = {c["id"]: c for c in catalog.get("casos", [])}
    mediciones: list[dict[str, Any]] = []

    for caso_id in listar_casos():
        estado = cargar_estado(caso_id)
        cj = caso_dir(caso_id) / "caso.json"
        meta_caso: dict[str, Any] = {}
        if cj.exists():
            with open(cj, encoding="utf-8") as f:
                meta_caso = json.load(f)

        caso_info = casos_map.get(caso_id) or {
            "id": caso_id,
            "etiqueta": meta_caso.get("etiqueta", estado["caso_foco"]["etiqueta"]),
            "inaugural": meta_caso.get("inaugural", False),
            "nota_registro": meta_caso.get("nota_registro", ""),
        }
        if meta_caso:
            caso_info["etiqueta"] = meta_caso.get("etiqueta", caso_info["etiqueta"])
            if meta_caso.get("inaugural"):
                caso_info["inaugural"] = True
                caso_info["nota_registro"] = meta_caso.get(
                    "nota_registro", caso_info.get("nota_registro", "")
                )
        casos_map[caso_id] = caso_info

        activa = estado["branches"]["main"]["medicion_activa"]
        for key, med in estado["mediciones"].items():
            med_id = med["id"]
            destacada = med_id == activa
            mediciones.append(
                {
                    "id": med_id,
                    "caso_id": caso_id,
                    "caso_etiqueta": caso_info["etiqueta"],
                    "intensidad": med["intensidad"],
                    "lectura": med["lectura"],
                    "buffers_activos": med.get("buffers_activos", []),
                    "destacada": destacada,
                    "url_prensa": f"/prensa/medicion/{med_id}.html",
                }
            )

    catalog["casos"] = list(casos_map.values())
    catalog["mediciones_publicas"] = sorted(mediciones, key=lambda m: m["id"])
    guardar_catalog(catalog)
    return catalog


sincronizar_catalog = sync_catalog
