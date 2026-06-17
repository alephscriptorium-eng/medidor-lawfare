# SPDX-License-Identifier: GPL-3.0-or-later
"""Cálculo de ejes e intensidad."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from medidor_lawfare.mcn.cribador import ItemCribado
from medidor_lawfare.motor.constantes import (
    CAP_DELTA_EJE,
    CAP_DELTA_INTENSIDAD,
    PESOS_INTENSIDAD,
    RANURA_EJES,
    REDUNDANCIA_MCS1,
)

# Re-export para compatibilidad de API
__all__ = [
    "RANURA_EJES",
    "REDUNDANCIA_MCS1",
    "CAP_DELTA_EJE",
    "CAP_DELTA_INTENSIDAD",
    "PESOS_INTENSIDAD",
    "calcular_impacto_ejes",
    "calcular_delta_intensidad",
]


def calcular_impacto_ejes(items: list[ItemCribado]) -> dict[str, float]:
    acum: dict[str, float] = {
        "integridad": 0.0,
        "sincronia": 0.0,
        "ventana": 0.0,
        "impacto": 0.0,
        "vector": 0.0,
    }
    for it in items:
        if it.accion != "cargar" or not it.ranura_destino:
            continue
        for eje, base in RANURA_EJES.get(it.ranura_destino, {}).items():
            acum[eje] += base * it.peso

    for eje in acum:
        acum[eje] = min(acum[eje] * REDUNDANCIA_MCS1, CAP_DELTA_EJE)
    return acum


def calcular_delta_intensidad(
    delta_ejes: dict[str, float], intensidad_base: float
) -> float:
    delta = sum(
        delta_ejes[eje] * peso for eje, peso in PESOS_INTENSIDAD.items()
    )
    delta = max(-CAP_DELTA_INTENSIDAD, min(CAP_DELTA_INTENSIDAD, delta))
    return round(intensidad_base + delta, 2)
