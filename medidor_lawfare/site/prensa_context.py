# SPDX-License-Identifier: GPL-3.0-or-later
"""Contexto Jinja para plantillas prensa."""

from __future__ import annotations

import json
from typing import Any

from medidor_lawfare.paths import caso_dir

GITHUB_REPO = "https://github.com/alephscriptorium-eng/medidor-lawfare"
GITHUB_BRANCH = "main"

BUFFER_SESION: dict[str, str] = {
    "MCS-1": "docs/sesiones/buffer-01.md",
    "MCS-2": "docs/sesiones/buffer-02.md",
    "MCS-3": "docs/sesiones/buffer-03.md",
    "MCS-4": "docs/sesiones/buffer-04.md",
}

MCS_MEDICION: dict[str, str] = {
    "MCS-1": "M1",
    "MCS-2": "M2",
    "MCS-3": "M3",
    "MCS-4": "M4",
}


def github_blob(path: str) -> str:
    return f"{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{path}"


def _buffer_enriquecido(buf: dict[str, Any], caso_id: str) -> dict[str, Any]:
    bid = buf["id"]
    num = bid.rsplit("-", 1)[-1]
    sesion = BUFFER_SESION.get(bid)
    entrada = f"data/buffers/{bid}-entrada.json"
    cribado = f"data/casos/{caso_id}/cribados/cribado-{bid}.json"
    return {
        **buf,
        "num": num,
        "medicion": MCS_MEDICION.get(bid),
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
    return {
        **med,
        "caso_nombre": med.get("caso_etiqueta", med.get("caso_id", "")),
        "ejes": medicion_estado.get("ejes", {}),
        "buffers_activos": medicion_estado.get(
            "buffers_activos", med.get("buffers_activos", [])
        ),
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
        "mediciones": [
            {"id": m["id"], "intensidad": m["intensidad"], "lectura": m["lectura"]}
            for m in meds
        ],
        "buffers": buffers,
    }
