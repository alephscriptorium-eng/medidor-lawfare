# SPDX-License-Identifier: GPL-3.0-or-later
"""Contexto Jinja para plantillas prensa."""

from __future__ import annotations

import json
from typing import Any

from medidor_lawfare.paths import caso_dir, GITHUB_REPO, PROJECT_ROOT

GITHUB_BRANCH = "main"


def pack_medicion_href(caso_id: str, med_id: str, base_href: str = "") -> str:
    return f"{base_href}downloads/{caso_id}-{med_id}.zip"


def pack_caso_href(caso_id: str, base_href: str = "") -> str:
    return f"{base_href}downloads/{caso_id}.zip"


def github_blob(path: str) -> str:
    return f"{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{path}"


def _buffer_enriquecido(buf: dict[str, Any], caso_id: str) -> dict[str, Any]:
    bid = buf["id"]
    num = bid.rsplit("-", 1)[-1]
    
    sesion_path = f"docs/sesiones/buffer-{int(num):02d}.md"
    sesion = sesion_path if (PROJECT_ROOT / sesion_path).exists() else None
    
    entrada = f"data/buffers/{bid}-entrada.json"
    cribado = f"data/casos/{caso_id}/cribados/cribado-{bid}.json"
    return {
        **buf,
        "num": num,
        "medicion": f"M{num}",
        "sesion": sesion,
        "entrada": entrada,
        "cribado": cribado,
        "sesion_github": github_blob(sesion) if sesion else None,
        "entrada_github": github_blob(entrada),
        "cribado_github": github_blob(cribado),
    }


def buffer_para_medicion(
    estado: dict[str, Any], med_id: str, caso_id: str
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if med_id == "M0":
        return None, None
    delta = next(
        (d for d in estado.get("deltas", []) if d.get("hasta") == med_id),
        None,
    )
    if not delta:
        return None, None
    bid = delta.get("buffer_aplicado")
    if not bid:
        return delta, None
    buffers_map = {b["id"]: b for b in estado.get("buffers", [])}
    buf_meta = buffers_map.get(bid, {"id": bid})
    return delta, _buffer_enriquecido(buf_meta, caso_id)


def timeline_mediciones(estado: dict[str, Any]) -> list[dict[str, Any]]:
    meds = sorted(estado.get("mediciones", {}).values(), key=lambda m: m["id"])
    return [
        {"id": m["id"], "intensidad": m["intensidad"], "lectura": m["lectura"]}
        for m in meds
    ]


def med_enriquecida(med: dict[str, Any], medicion_estado: dict[str, Any]) -> dict[str, Any]:
    caso_id = med.get("caso_id", "")
    med_id = med.get("id", "")
    return {
        **med,
        "caso_nombre": med.get("caso_etiqueta", med.get("caso_id", "")),
        "ejes": medicion_estado.get("ejes", {}),
        "buffers_activos": medicion_estado.get(
            "buffers_activos", med.get("buffers_activos", [])
        ),
        "pack_medicion_href": pack_medicion_href(caso_id, med_id, "../"),
    }


def cargar_meta_caso(caso_id: str) -> dict[str, Any]:
    path = caso_dir(caso_id) / "caso.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def caso_enriquecido(caso: dict[str, Any], estado: dict[str, Any]) -> dict[str, Any]:
    meta = cargar_meta_caso(caso["id"])
    activa = estado["branches"]["main"]["medicion_activa"]
    meds = sorted(estado.get("mediciones", {}).values(), key=lambda m: m["id"])
    activa_med = next(m for m in meds if m["id"] == activa)
    buffers = [_buffer_enriquecido(b, caso["id"]) for b in estado.get("buffers", [])]
    return {
        **caso,
        "nombre": caso.get("etiqueta", caso["id"]),
        "descripcion": meta.get("descripcion") or caso.get("nota_registro", ""),
        "medicion_activa": activa,
        "intensidad_actual": activa_med["intensidad"],
        "lectura_actual": activa_med["lectura"],
        "pack_caso_href": pack_caso_href(caso["id"], "../"),
        "mediciones": [
            {"id": m["id"], "intensidad": m["intensidad"], "lectura": m["lectura"]}
            for m in meds
        ],
        "buffers": buffers,
    }
