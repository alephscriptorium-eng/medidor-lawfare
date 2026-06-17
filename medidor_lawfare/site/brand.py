# SPDX-License-Identifier: GPL-3.0-or-later
"""Metadatos de marca y proveniencia transmedia para plantillas Jinja."""

from __future__ import annotations

import json
from typing import Any

from medidor_lawfare.paths import SITE_DIR

BRAND_PATH = SITE_DIR / "brand.json"
GITHUB_REPO = "https://github.com/alephscriptorium-eng/medidor-lawfare"


def cargar_brand() -> dict[str, Any]:
    with open(BRAND_PATH, encoding="utf-8") as f:
        return json.load(f)


def provenance_context(brand: dict[str, Any] | None = None) -> dict[str, str]:
    if brand is None:
        brand = cargar_brand()
    return {
        "material_label": "Material transmedia",
        "license": "GPL-3.0",
        "repo_url": GITHUB_REPO,
        "arg_label": brand["arg"]["etiqueta"],
    }


def brand_context() -> dict[str, Any]:
    """Contexto Jinja: brand (dict), brand_name (str) y provenance."""
    brand = cargar_brand()
    return {
        "brand": brand,
        "brand_name": brand["producto"]["nombre"],
        "provenance": provenance_context(brand),
    }
