# SPDX-License-Identifier: GPL-3.0-or-later
"""Lectura cualitativa de intensidad."""


def lectura_intensidad(v: float) -> str:
    if v < 4.0:
        return "bajo"
    if v < 5.0:
        return "marginal"
    if v < 6.0:
        return "sospechas fundadas"
    if v < 7.0:
        return "alta probabilidad de lawfare"
    return "lawfare sistémico confirmado"
