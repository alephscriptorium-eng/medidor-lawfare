# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests de generación de paquetes ZIP para prensa."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from medidor_lawfare.rdb.estado import cargar_estado
from medidor_lawfare.site.packs import (
    archivos_caso,
    archivos_medicion,
    escribir_zip,
    generar_readme,
)

ROOT = Path(__file__).resolve().parent.parent
CASO_ID = "zapatero-plus-ultra"


@pytest.fixture
def estado() -> dict:
    return cargar_estado(CASO_ID)


def test_archivos_medicion_m0_sin_buffers(estado: dict) -> None:
    contents = archivos_medicion(CASO_ID, "M0", estado)
    arcnames = contents.arcnames()
    assert "caso.json" in arcnames
    assert "medicion/M0.json" in arcnames
    assert not any(a.startswith("buffers/") for a in arcnames)
    assert not any(a.startswith("delta/") for a in arcnames)


def test_archivos_medicion_m3_incluye_buffer_y_delta(estado: dict) -> None:
    contents = archivos_medicion(CASO_ID, "M3", estado)
    arcnames = contents.arcnames()
    assert "medicion/M3.json" in arcnames
    assert "delta/D2→3.json" in arcnames
    assert "buffers/MCS-3-entrada.json" in arcnames
    assert "cribados/cribado-MCS-3.json" in arcnames
    assert "docs/sesiones/buffer-03.md" in arcnames


def test_archivos_caso_incluye_estado_y_buffers(estado: dict) -> None:
    contents = archivos_caso(CASO_ID, estado)
    arcnames = contents.arcnames()
    assert "caso.json" in arcnames
    assert "estado.json" in arcnames
    assert "cribados/cribado-MCS-1.json" in arcnames
    assert "buffers/MCS-9-entrada.json" in arcnames
    assert "docs/sesiones/buffer-09.md" in arcnames
    assert len([a for a in arcnames if a.startswith("cribados/")]) == 9


def test_zip_medicion_contiene_readme_y_rutas(estado: dict, tmp_path: Path) -> None:
    contents = archivos_medicion(CASO_ID, "M3", estado)
    readme = generar_readme(
        "medicion",
        CASO_ID,
        "M3",
        estado["motor_version"],
        contents.arcnames(),
        contents.omitidos,
    )
    dest = tmp_path / f"{CASO_ID}-M3.zip"
    escribir_zip(dest, contents, readme)

    with zipfile.ZipFile(dest) as zf:
        names = zf.namelist()
        assert "README.txt" in names
        assert "medicion/M3.json" in names
        assert "delta/D2→3.json" in names
        readme_text = zf.read("README.txt").decode("utf-8")
        assert "GPL-3.0" in readme_text
        snap = json.loads(zf.read("medicion/M3.json"))
        assert snap["id"] == "M3"
        assert snap["intensidad"] == 6.56


def test_zip_caso_contiene_estado(estado: dict, tmp_path: Path) -> None:
    contents = archivos_caso(CASO_ID, estado)
    readme = generar_readme(
        "caso",
        CASO_ID,
        None,
        estado["motor_version"],
        contents.arcnames(),
        contents.omitidos,
    )
    dest = tmp_path / f"{CASO_ID}.zip"
    escribir_zip(dest, contents, readme)

    with zipfile.ZipFile(dest) as zf:
        names = zf.namelist()
        assert "README.txt" in names
        assert "estado.json" in names
        estado_zip = json.loads(zf.read("estado.json"))
        assert estado_zip["caso_id"] == CASO_ID
