# SPDX-License-Identifier: GPL-3.0-or-later
"""Gestión de estado.json y commits de buffer."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

from medidor_lawfare import __version__
from medidor_lawfare.mcn.cribador import procesar_buffer, ResultadoCribado
from medidor_lawfare.motor.ejes import calcular_impacto_ejes, calcular_delta_intensidad
from medidor_lawfare.motor.intensidad import lectura_intensidad
from medidor_lawfare.rdb.deltas import clasificar_delta
from medidor_lawfare.paths import CASOS_DIR, estado_path, cribados_dir


def listar_casos() -> list[str]:
    if not CASOS_DIR.exists():
        return []
    return sorted(
        d.name for d in CASOS_DIR.iterdir() if d.is_dir() and (d / "estado.json").exists()
    )


def cargar_estado(caso_id: str) -> dict[str, Any]:
    path = estado_path(caso_id)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar_estado(caso_id: str, estado: dict[str, Any]) -> None:
    path = estado_path(caso_id)
    estado["motor_version"] = __version__
    with open(path, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def _promedio_capa(resultado: ResultadoCribado) -> str:
    caps = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    total = 0
    score = 0
    for it in resultado.items + resultado.cuarentena:
        total += 1
        score += caps.get(it.capa, 2)
    if not total:
        return "L1"
    avg = score / total
    if avg < 0.5:
        return "L0"
    if avg < 1.2:
        return "L1"
    if avg < 2.2:
        return "L2"
    return "L3"


def _nota_delta(resultado: ResultadoCribado, delta_intensidad: float) -> str:
    l0 = resultado.resumen_capas.get("L0", 0)
    l3 = resultado.resumen_capas.get("L3", 0)
    if l3 > l0:
        return (
            "Buffer mixto: datos duros (Alba, Cataluña, TEDH) confirman patrón; "
            f"bloque interpretativo parcialmente en cuarentena. Δ={delta_intensidad:+.2f}"
        )
    return f"Datos verificables refuerzan medición previa. Δ={delta_intensidad:+.2f}"


def _medicion_key_para_buffer(buffer_id: str) -> str:
    num = buffer_id.split("-")[-1]
    return f"post_mcs_{num}"


def commit_buffer(caso_id: str, entrada_path: Path) -> dict[str, Any]:
    estado = cargar_estado(caso_id)
    with open(entrada_path, encoding="utf-8") as f:
        data = json.load(f)

    resultado = procesar_buffer(data, estado)
    buffer_id = resultado.buffer_id
    prev_key = f"post_mcs_{int(buffer_id.split('-')[-1]) - 1}" if buffer_id != "MCS-1" else "baseline"
    if buffer_id == "MCS-1":
        prev_key = "baseline"
    else:
        prev_num = int(buffer_id.split("-")[-1]) - 1
        prev_key = "baseline" if prev_num == 0 else f"post_mcs_{prev_num}"

    if prev_key not in estado["mediciones"]:
        raise ValueError(f"No existe medición previa '{prev_key}' para buffer {buffer_id}")

    m_prev = estado["mediciones"][prev_key]
    ejes_prev = m_prev["ejes"]

    delta_raw = calcular_impacto_ejes(resultado.items)
    ejes_new = {k: round(ejes_prev[k] + delta_raw[k], 2) for k in ejes_prev}
    delta_ejes = {k: round(ejes_new[k] - ejes_prev[k], 2) for k in ejes_prev}
    intensidad_new = calcular_delta_intensidad(delta_ejes, m_prev["intensidad"])
    delta_intensidad = round(intensidad_new - m_prev["intensidad"], 2)
    direccion, clasificacion = clasificar_delta(delta_intensidad, delta_ejes)

    buffer_meta = data["buffer_entrada"]
    pct_l3 = resultado.resumen_capas.get("L3", 0) / max(
        1, sum(resultado.resumen_capas.values())
    )

    estado["buffers"].append(
        {
            "id": resultado.buffer_id,
            "tipo": buffer_meta.get("tipo", "contexto_fino"),
            "etiqueta": resultado.etiqueta,
            "fecha_carga": str(date.today()),
            "inmutable": True,
            "nivel_asépticidad_promedio": _promedio_capa(resultado),
            "ranuras_pobladas": len({i.ranura_destino for i in resultado.items}),
            "items_cargados": len(resultado.items),
            "items_cuarentena": len(resultado.cuarentena),
            "resumen_capas": resultado.resumen_capas,
            "pct_l3": round(pct_l3, 2),
            "nota_origen": buffer_meta.get("nota_origen", ""),
        }
    )

    medicion_id = f"M{buffer_id.split('-')[-1]}"
    buffers_activos = [b["id"] for b in estado["buffers"]]
    med_key = _medicion_key_para_buffer(buffer_id)

    estado["mediciones"][med_key] = {
        "id": medicion_id,
        "buffers_activos": buffers_activos,
        "ejes": ejes_new,
        "intensidad": intensidad_new,
        "lectura": lectura_intensidad(intensidad_new),
    }

    delta_id = f"D{prev_key.replace('post_mcs_', '') if prev_key != 'baseline' else '0'}→{buffer_id.split('-')[-1]}"
    if prev_key == "baseline":
        delta_id = f"D0→{buffer_id.split('-')[-1]}"
    else:
        desde = f"M{prev_key.replace('post_mcs_', '')}"
        hasta = medicion_id
        delta_id = f"D{prev_key.replace('post_mcs_', '')}→{buffer_id.split('-')[-1]}"

    estado["deltas"].append(
        {
            "id": delta_id,
            "desde": "M0" if prev_key == "baseline" else f"M{prev_key.replace('post_mcs_', '')}",
            "hasta": medicion_id,
            "buffer_aplicado": buffer_id,
            "delta_ejes": delta_ejes,
            "delta_intensidad": delta_intensidad,
            "direccion": direccion,
            "clasificacion_impacto": clasificacion,
            "nota": _nota_delta(resultado, delta_intensidad),
        }
    )

    estado["branches"]["main"]["medicion_activa"] = medicion_id
    estado["branches"]["main"]["buffers_activos"] = buffers_activos
    estado["branches"]["main"]["historial_deltas"].append(delta_id)

    guardar_estado(caso_id, estado)

    out_dir = cribados_dir(caso_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    cribado_path = out_dir / f"cribado-{resultado.buffer_id}.json"
    with open(cribado_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "buffer_id": resultado.buffer_id,
                "etiqueta": resultado.etiqueta,
                "resumen_capas": resultado.resumen_capas,
                "items": [asdict(i) for i in resultado.items],
                "cuarentena": [asdict(i) for i in resultado.cuarentena],
                "medicion": estado["mediciones"][med_key],
                "delta": estado["deltas"][-1],
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    return {
        "resultado": resultado,
        "prev": m_prev,
        "new": estado["mediciones"][med_key],
        "delta": estado["deltas"][-1],
        "cribado_path": str(cribado_path),
        "pct_l3": pct_l3,
    }
