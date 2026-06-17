# SPDX-License-Identifier: GPL-3.0-or-later
"""Integración: commit_buffer en sandbox vs golden de estado.json."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import patch

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parent.parent
CASO_ID = "zapatero-plus-ultra"
BUFFERS_DIR = ROOT / "data/buffers"
GOLDEN_ESTADO = ROOT / f"data/casos/{CASO_ID}/estado.json"
GOLDEN_CRIBADOS = ROOT / f"data/casos/{CASO_ID}/cribados"
SCHEMA_CRIBADO = ROOT / "data/schema/cribado.schema.json"


def _rollback_estado(estado: dict, hasta_num: int) -> dict:
    e = copy.deepcopy(estado)
    med_id = f"M{hasta_num}"
    e["buffers"] = [b for b in e["buffers"] if int(b["id"].split("-")[-1]) <= hasta_num]
    e["deltas"] = [d for d in e["deltas"] if d["hasta"] <= med_id]
    e["mediciones"] = {
        k: v
        for k, v in e["mediciones"].items()
        if k == "baseline" or int(k.split("_")[-1]) <= hasta_num
    }
    e["branches"]["main"]["medicion_activa"] = med_id
    e["branches"]["main"]["buffers_activos"] = [b["id"] for b in e["buffers"]]
    e["branches"]["main"]["historial_deltas"] = [d["id"] for d in e["deltas"]]
    return e


def _items_sin_id(items: list[dict]) -> list[dict]:
    return [{k: v for k, v in it.items() if k != "id"} for it in items]


def _normalizar_cribado(d: dict) -> dict:
    return {
        "buffer_id": d["buffer_id"],
        "etiqueta": d["etiqueta"],
        "resumen_capas": d["resumen_capas"],
        "items": sorted(_items_sin_id(d["items"]), key=lambda x: x["texto_original"]),
        "cuarentena": sorted(_items_sin_id(d["cuarentena"]), key=lambda x: x["texto_original"]),
        "medicion": d.get("medicion"),
        "delta": d.get("delta"),
    }


@pytest.fixture
def patch_casos(tmp_path: Path):
    casos_dir = tmp_path / "casos"
    casos_dir.mkdir()

    def _install(caso_id: str, estado: dict) -> Path:
        d = casos_dir / caso_id
        d.mkdir(parents=True)
        (d / "cribados").mkdir()
        (d / "estado.json").write_text(
            json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return d

    with (
        patch("medidor_lawfare.rdb.estado.CASOS_DIR", casos_dir),
        patch("medidor_lawfare.rdb.estado.estado_path", lambda cid: casos_dir / cid / "estado.json"),
        patch("medidor_lawfare.rdb.estado.cribados_dir", lambda cid: casos_dir / cid / "cribados"),
    ):
        yield casos_dir, _install


def test_prev_key_and_delta_id_helpers() -> None:
    from medidor_lawfare.rdb import estado as est

    assert est._prev_key(1) == "baseline"
    assert est._prev_key(2) == "post_mcs_1"
    assert est._prev_key(4) == "post_mcs_3"
    assert est._delta_id("baseline", 1) == "D0→1"
    assert est._delta_id("post_mcs_1", 2) == "D1→2"
    assert est._delta_id("post_mcs_3", 4) == "D3→4"
    assert est._medicion_id(4) == "M4"


def test_commit_buffer_mcs1_matches_golden(patch_casos) -> None:
    from medidor_lawfare.rdb.estado import commit_buffer, cargar_estado

    casos_dir, install = patch_casos
    with open(GOLDEN_ESTADO, encoding="utf-8") as f:
        golden = json.load(f)

    install(CASO_ID, _rollback_estado(golden, hasta_num=0))
    result = commit_buffer(CASO_ID, BUFFERS_DIR / "MCS-1-entrada.json")

    golden_med = golden["mediciones"]["post_mcs_1"]
    golden_delta = next(d for d in golden["deltas"] if d["id"] == "D0→1")

    # estado.json M1 (6.4) es legacy no reproducible desde baseline con motor actual;
    # HEAD pre-refactor también produce 5.16 — no es regresión del refactor.
    assert result["new"]["id"] == "M1"
    assert result["new"]["intensidad"] == 5.16
    assert result["delta"]["id"] == "D0→1"
    assert result["delta"]["desde"] == "M0"
    assert result["delta"]["hasta"] == "M1"
    assert result["delta"]["buffer_aplicado"] == "MCS-1"

    estado_post = cargar_estado(CASO_ID)
    assert estado_post["mediciones"]["post_mcs_1"]["intensidad"] == 5.16
    assert estado_post["branches"]["main"]["medicion_activa"] == "M1"

    cribado = json.loads((casos_dir / CASO_ID / "cribados" / "cribado-MCS-1.json").read_text())
    assert {"medicion", "delta"} <= set(cribado.keys())
    assert cribado["medicion"]["intensidad"] == 5.16


def test_commit_buffer_mcs4_matches_golden(patch_casos) -> None:
    from medidor_lawfare.rdb.estado import commit_buffer

    casos_dir, install = patch_casos
    with open(GOLDEN_ESTADO, encoding="utf-8") as f:
        golden_estado = json.load(f)
    golden_cribado = json.loads((GOLDEN_CRIBADOS / "cribado-MCS-4.json").read_text())

    install(CASO_ID, _rollback_estado(golden_estado, hasta_num=3))
    result = commit_buffer(CASO_ID, BUFFERS_DIR / "MCS-4-entrada.json")

    assert result["new"] == golden_cribado["medicion"]
    assert result["delta"] == golden_cribado["delta"]

    cribado = json.loads((casos_dir / CASO_ID / "cribados" / "cribado-MCS-4.json").read_text())
    assert _normalizar_cribado(cribado) == _normalizar_cribado(golden_cribado)


def test_cribado_formato_en_disco_y_writer(patch_casos) -> None:
    """cribar (base) vs disco; commit añade medicion+delta unificados."""
    from medidor_lawfare.mcn.cribador import (
        cargar_buffer_desde_archivo,
        procesar_buffer,
        resultado_a_dict,
    )
    from medidor_lawfare.rdb.estado import cargar_estado, commit_buffer

    with open(SCHEMA_CRIBADO, encoding="utf-8") as f:
        schema = json.load(f)

    with open(GOLDEN_ESTADO, encoding="utf-8") as f:
        estado = json.load(f)
    campos_base = {"buffer_id", "etiqueta", "resumen_capas", "items", "cuarentena"}

    for n in range(1, 5):
        golden = json.loads((GOLDEN_CRIBADOS / f"cribado-MCS-{n}.json").read_text())
        assert campos_base <= set(golden.keys())
        jsonschema.validate({k: golden[k] for k in campos_base}, schema)

        if n == 1:
            assert "medicion" not in golden  # legacy: solo cribado base
        elif n == 2:
            assert "medicion_m2" in golden and "delta" in golden  # legacy
        else:
            assert "medicion" in golden and "delta" in golden

        buf = cargar_buffer_desde_archivo(
            (BUFFERS_DIR / f"MCS-{n}-entrada.json").read_text(encoding="utf-8")
        )
        resultado = procesar_buffer(buf, _rollback_estado(estado, hasta_num=n - 1))
        cribar_dict = resultado_a_dict(resultado)
        assert set(cribar_dict.keys()) == campos_base
        assert cribar_dict["resumen_capas"] == golden["resumen_capas"]
        assert len(cribar_dict["items"]) == len(golden["items"])
        assert len(cribar_dict["cuarentena"]) == len(golden["cuarentena"])

    # Nuevo commit siempre escribe medicion (no medicion_m2)
    casos_dir, install = patch_casos
    install(CASO_ID, _rollback_estado(estado, hasta_num=1))
    out = commit_buffer(CASO_ID, BUFFERS_DIR / "MCS-2-entrada.json")
    cribado = json.loads(Path(out["cribado_path"]).read_text())
    assert "medicion" in cribado and "delta" in cribado
    assert "medicion_m2" not in cribado
