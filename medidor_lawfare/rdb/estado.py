# SPDX-License-Identifier: GPL-3.0-or-later
"""Gestión de estado.json y commits de buffer."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from medidor_lawfare import __version__
from medidor_lawfare.mcn.cribador import (
    buffer_num,
    calcular_pct_l3,
    procesar_buffer,
    resultado_a_dict,
    ResultadoCribado,
)
from medidor_lawfare.motor.ejes import calcular_impacto_ejes, calcular_delta_intensidad
from medidor_lawfare.motor.intensidad import lectura_intensidad
from medidor_lawfare.rdb.deltas import clasificar_delta, nota_delta, promedio_capa
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


def _medicion_key(num: int) -> str:
    """Clave de medición en estado.json para el buffer N."""
    return f"post_mcs_{num}"


def _prev_key(num: int) -> str:
    """Clave de la medición previa al buffer N."""
    if num <= 1:
        return "baseline"
    return _medicion_key(num - 1)


def _medicion_id(num: int) -> str:
    """ID público de medición para el buffer N."""
    return f"M{num}"


def _delta_id(prev: str, num: int) -> str:
    """ID del delta entre la medición previa y la nueva."""
    desde = "0" if prev == "baseline" else prev.replace("post_mcs_", "")
    return f"D{desde}→{num}"


def _calcular_nuevo_estado_ejes(
    resultado: ResultadoCribado, m_prev: dict[str, Any]
) -> tuple[dict[str, float], dict[str, float], float, float, str, str]:
    delta_raw = calcular_impacto_ejes(resultado.items)
    ejes_prev = m_prev["ejes"]
    ejes_new = {k: round(ejes_prev[k] + delta_raw[k], 2) for k in ejes_prev}
    delta_ejes = {k: round(ejes_new[k] - ejes_prev[k], 2) for k in ejes_prev}
    intensidad_new = calcular_delta_intensidad(delta_ejes, m_prev["intensidad"])
    delta_intensidad = round(intensidad_new - m_prev["intensidad"], 2)
    direccion, clasificacion = clasificar_delta(delta_intensidad, delta_ejes)
    return ejes_new, delta_ejes, intensidad_new, delta_intensidad, direccion, clasificacion


def _crear_registro_buffer(
    resultado: ResultadoCribado, buffer_meta: dict[str, Any], pct_l3: float
) -> dict[str, Any]:
    return {
        "id": resultado.buffer_id,
        "tipo": buffer_meta.get("tipo", "contexto_fino"),
        "etiqueta": resultado.etiqueta,
        "fecha_carga": str(date.today()),
        "inmutable": True,
        "nivel_asépticidad_promedio": promedio_capa(resultado),
        "ranuras_pobladas": len({i.ranura_destino for i in resultado.items}),
        "items_cargados": len(resultado.items),
        "items_cuarentena": len(resultado.cuarentena),
        "resumen_capas": resultado.resumen_capas,
        "pct_l3": round(pct_l3, 2),
        "nota_origen": buffer_meta.get("nota_origen", ""),
    }


def _crear_registro_medicion(
    med_id: str, buffers_activos: list[str], ejes_new: dict[str, float], intensidad_new: float
) -> dict[str, Any]:
    return {
        "id": med_id,
        "buffers_activos": buffers_activos,
        "ejes": ejes_new,
        "intensidad": intensidad_new,
        "lectura": lectura_intensidad(intensidad_new),
    }


def _crear_registro_delta(
    did: str,
    desde_id: str,
    med_id: str,
    bid: str,
    delta_ejes: dict[str, float],
    delta_intensidad: float,
    direccion: str,
    clasificacion: str,
    nota: str,
) -> dict[str, Any]:
    return {
        "id": did,
        "desde": desde_id,
        "hasta": med_id,
        "buffer_aplicado": bid,
        "delta_ejes": delta_ejes,
        "delta_intensidad": delta_intensidad,
        "direccion": direccion,
        "clasificacion_impacto": clasificacion,
        "nota": nota,
    }


def commit_buffer(caso_id: str, entrada_path: Path) -> dict[str, Any]:
    estado = cargar_estado(caso_id)
    with open(entrada_path, encoding="utf-8") as f:
        data = json.load(f)

    resultado = procesar_buffer(data, estado)
    bid = resultado.buffer_id
    num = buffer_num(bid)

    prev = _prev_key(num)
    if prev not in estado["mediciones"]:
        raise ValueError(f"No existe medición previa '{prev}' para buffer {bid}")

    m_prev = estado["mediciones"][prev]

    # --- Cálculo de ejes y deltas ---
    ejes_new, delta_ejes, intensidad_new, delta_intensidad, direccion, clasificacion = _calcular_nuevo_estado_ejes(
        resultado, m_prev
    )

    # --- Metadatos del buffer ---
    pct_l3 = calcular_pct_l3(resultado)
    buffer_reg = _crear_registro_buffer(resultado, data["buffer_entrada"], pct_l3)
    estado["buffers"].append(buffer_reg)

    # --- Nueva medición ---
    med_id = _medicion_id(num)
    buffers_activos = [b["id"] for b in estado["buffers"]]
    med_key = _medicion_key(num)

    med_reg = _crear_registro_medicion(med_id, buffers_activos, ejes_new, intensidad_new)
    estado["mediciones"][med_key] = med_reg

    # --- Delta ---
    did = _delta_id(prev, num)
    desde_id = "M0" if prev == "baseline" else _medicion_id(num - 1)

    delta_reg = _crear_registro_delta(
        did,
        desde_id,
        med_id,
        bid,
        delta_ejes,
        delta_intensidad,
        direccion,
        clasificacion,
        nota_delta(resultado, delta_intensidad),
    )
    estado["deltas"].append(delta_reg)

    # --- Actualizar branches ---
    estado["branches"]["main"]["medicion_activa"] = med_id
    estado["branches"]["main"]["buffers_activos"] = buffers_activos
    estado["branches"]["main"]["historial_deltas"].append(did)

    guardar_estado(caso_id, estado)

    # --- Guardar cribado (formato unificado + medición/delta) ---
    out_dir = cribados_dir(caso_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    cribado_path = out_dir / f"cribado-{bid}.json"
    cribado_dict = resultado_a_dict(resultado)
    cribado_dict["medicion"] = med_reg
    cribado_dict["delta"] = delta_reg
    with open(cribado_path, "w", encoding="utf-8") as f:
        json.dump(cribado_dict, f, ensure_ascii=False, indent=2)

    return {
        "resultado": resultado,
        "prev": m_prev,
        "new": med_reg,
        "delta": delta_reg,
        "cribado_path": str(cribado_path),
        "pct_l3": pct_l3,
    }
