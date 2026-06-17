# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests de regresión y validación de esquemas."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parent.parent
ESTADO_PATH = ROOT / "data/casos/zapatero-plus-ultra/estado.json"
SCHEMA_DIR = ROOT / "data/schema"


@pytest.fixture
def estado() -> dict:
    with open(ESTADO_PATH, encoding="utf-8") as f:
        return json.load(f)


def test_m0_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["baseline"]["intensidad"] == 5.0


def test_m1_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_1"]["intensidad"] == 6.4


def test_m2_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_2"]["intensidad"] == 6.5


def test_m3_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_3"]["intensidad"] == 6.56


def test_m4_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_4"]["intensidad"] == 6.68


def test_m5_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_5"]["intensidad"] == 6.79


def test_m6_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_6"]["intensidad"] == 6.97


def test_m7_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_7"]["intensidad"] == 6.98


def test_m8_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_8"]["intensidad"] == 7.01


def test_m9_intensidad(estado: dict) -> None:
    assert estado["mediciones"]["post_mcs_9"]["intensidad"] == 7.09


def test_motor_version(estado: dict) -> None:
    assert estado["motor_version"] == "1.0.0"


def test_estado_schema(estado: dict) -> None:
    with open(SCHEMA_DIR / "estado.schema.json", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(estado, schema)


def test_catalog_schema() -> None:
    catalog_path = ROOT / "data/catalog.json"
    if not catalog_path.exists():
        pytest.skip("catalog.json not generated yet")
    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)
    with open(SCHEMA_DIR / "catalog.schema.json", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(catalog, schema)


def test_mcn_cribado_mcs2() -> None:
    from medidor_lawfare.mcn.cribador import cargar_buffer_desde_archivo, procesar_buffer
    from medidor_lawfare.rdb.estado import cargar_estado

    estado = cargar_estado("zapatero-plus-ultra")
    # estado ya tiene MCS-2; usar copia sin MCS-2 para cribado
    estado_test = json.loads(json.dumps(estado))
    estado_test["buffers"] = [b for b in estado_test["buffers"] if b["id"] != "MCS-2"]

    buf_path = ROOT / "data/buffers/MCS-2-entrada.json"
    data = cargar_buffer_desde_archivo(buf_path.read_text(encoding="utf-8"))
    resultado = procesar_buffer(data, estado_test)

    assert resultado.resumen_capas.get("L3", 0) == 10
    assert len(resultado.items) == 8
    assert len(resultado.cuarentena) == 10
