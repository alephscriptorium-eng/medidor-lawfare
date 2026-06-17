# SPDX-License-Identifier: GPL-3.0-or-later
"""Motor de medición — ejes e intensidad."""

from medidor_lawfare.motor.constantes import (
    RANURA_EJES,
    RANURAS_VALIDAS,
    REDUNDANCIA_MCS1,
    CAP_DELTA_EJE,
    CAP_DELTA_INTENSIDAD,
    PESOS_INTENSIDAD,
)
from medidor_lawfare.motor.ejes import (
    calcular_impacto_ejes,
    calcular_delta_intensidad,
)
from medidor_lawfare.motor.intensidad import lectura_intensidad

__all__ = [
    "RANURA_EJES",
    "RANURAS_VALIDAS",
    "REDUNDANCIA_MCS1",
    "CAP_DELTA_EJE",
    "CAP_DELTA_INTENSIDAD",
    "PESOS_INTENSIDAD",
    "calcular_impacto_ejes",
    "calcular_delta_intensidad",
    "lectura_intensidad",
]
