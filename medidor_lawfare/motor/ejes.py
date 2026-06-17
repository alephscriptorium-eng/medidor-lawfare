# SPDX-License-Identifier: GPL-3.0-or-later
"""Cálculo de ejes e intensidad."""

from __future__ import annotations

from medidor_lawfare.mcn.cribador import ItemCribado

RANURA_EJES: dict[str, dict[str, float]] = {
    "historico_imputaciones": {"integridad": 0.06, "impacto": 0.09},
    "patrones_acusacion": {"integridad": 0.04, "sincronia": 0.05, "impacto": 0.07},
    "cobertura_mediatica": {"sincronia": 0.05, "impacto": 0.06, "ventana": 0.03},
    "ventanas_temporales": {"sincronia": 0.10, "ventana": 0.09},
    "actores_recurrentes": {"vector": -0.04},
    "precedentes_judiciales": {"integridad": 0.09, "impacto": 0.05},
    "vectores_politicos": {"vector": -0.05, "sincronia": 0.03},
    "intensidad_historica_comparable": {"impacto": 0.08, "integridad": 0.04},
    "meta_patrones_sistemicos": {
        "integridad": 0.05,
        "sincronia": 0.05,
        "ventana": 0.04,
        "impacto": 0.05,
    },
}

REDUNDANCIA_MCS1 = 0.55
CAP_DELTA_EJE = 0.55
CAP_DELTA_INTENSIDAD = 0.50

PESOS_INTENSIDAD = {
    "integridad": 0.12,
    "sincronia": 0.15,
    "ventana": 0.12,
    "impacto": 0.18,
    "vector": 0.10,
}


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


from medidor_lawfare.motor.intensidad import lectura_intensidad  # noqa: F401
from medidor_lawfare.rdb.deltas import clasificar_delta  # noqa: F401
