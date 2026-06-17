# SPDX-License-Identifier: GPL-3.0-or-later
"""Motor de medición — ejes e intensidad."""

from medidor_lawfare.motor.ejes import (
    RANURA_EJES,
    REDUNDANCIA_MCS1,
    CAP_DELTA_EJE,
    CAP_DELTA_INTENSIDAD,
    PESOS_INTENSIDAD,
    calcular_impacto_ejes,
    calcular_delta_intensidad,
    lectura_intensidad,
    clasificar_delta,
)

__all__ = [
    "RANURA_EJES",
    "REDUNDANCIA_MCS1",
    "CAP_DELTA_EJE",
    "CAP_DELTA_INTENSIDAD",
    "PESOS_INTENSIDAD",
    "calcular_impacto_ejes",
    "calcular_delta_intensidad",
    "lectura_intensidad",
    "clasificar_delta",
]
