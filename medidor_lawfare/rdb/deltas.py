# SPDX-License-Identifier: GPL-3.0-or-later
"""Clasificación de deltas y notas."""

from __future__ import annotations

from medidor_lawfare.mcn.cribador import ResultadoCribado


def clasificar_delta(delta: float, delta_ejes: dict[str, float]) -> tuple[str, str]:
    suben = sum(1 for v in delta_ejes.values() if v > 0.05)
    bajan = sum(1 for v in delta_ejes.values() if v < -0.05)
    if delta > 0.3:
        direccion = "UP"
    elif delta < -0.3:
        direccion = "DOWN"
    elif suben and bajan:
        direccion = "MIXED"
    else:
        direccion = "NEUTRAL"

    if direccion == "UP":
        impacto = "eleva_lawfare"
    elif direccion == "DOWN":
        impacto = "reduce_lawfare"
    else:
        impacto = "ambiguo"
    return direccion, impacto


def promedio_capa(resultado: ResultadoCribado) -> str:
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


def nota_delta(resultado: ResultadoCribado, delta_intensidad: float) -> str:
    l0 = resultado.resumen_capas.get("L0", 0)
    l3 = resultado.resumen_capas.get("L3", 0)
    if l3 > l0:
        return (
            "Buffer mixto: datos duros (Alba, Cataluña, TEDH) confirman patrón; "
            f"bloque interpretativo parcialmente en cuarentena. Δ={delta_intensidad:+.2f}"
        )
    return f"Datos verificables refuerzan medición previa. Δ={delta_intensidad:+.2f}"
