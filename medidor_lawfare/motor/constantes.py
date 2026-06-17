# SPDX-License-Identifier: GPL-3.0-or-later
"""Constantes compartidas del motor de medición.

Módulo sin dependencias internas para evitar imports circulares.
"""

from __future__ import annotations

# ─── Ranuras → contribución a ejes ───────────────────────────────────────────
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

# Ranuras válidas derivadas automáticamente de RANURA_EJES
RANURAS_VALIDAS: frozenset[str] = frozenset(RANURA_EJES.keys())

# ─── Constantes del motor ────────────────────────────────────────────────────
REDUNDANCIA_MCS1 = 0.55
CAP_DELTA_EJE = 0.55
CAP_DELTA_INTENSIDAD = 0.50

PESOS_INTENSIDAD: dict[str, float] = {
    "integridad": 0.12,
    "sincronia": 0.15,
    "ventana": 0.12,
    "impacto": 0.18,
    "vector": 0.10,
}
