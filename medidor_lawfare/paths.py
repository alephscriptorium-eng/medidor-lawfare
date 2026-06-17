# SPDX-License-Identifier: GPL-3.0-or-later
"""Rutas del proyecto."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
DATA_DIR = PROJECT_ROOT / "data"
SCHEMA_DIR = DATA_DIR / "schema"
CASOS_DIR = DATA_DIR / "casos"
BUFFERS_DIR = DATA_DIR / "buffers"
CATALOG_PATH = DATA_DIR / "catalog.json"
SITE_DIR = PROJECT_ROOT / "site"
PUBLIC_DIR = PROJECT_ROOT / "public"
PUBLIC_PRENSA = PUBLIC_DIR / "prensa"
PUBLIC_FOSS = PUBLIC_DIR / "foss"
LICENSE = PROJECT_ROOT / "LICENSE"

GITHUB_REPO = "https://github.com/alephscriptorium-eng/medidor-lawfare"


def caso_dir(caso_id: str) -> Path:
    return CASOS_DIR / caso_id


def estado_path(caso_id: str) -> Path:
    return caso_dir(caso_id) / "estado.json"


def cribados_dir(caso_id: str) -> Path:
    return caso_dir(caso_id) / "cribados"
