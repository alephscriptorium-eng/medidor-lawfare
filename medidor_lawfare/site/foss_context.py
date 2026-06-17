# SPDX-License-Identifier: GPL-3.0-or-later
"""Contexto Jinja para plantillas FOSS."""

from __future__ import annotations

from medidor_lawfare.site.prensa_context import GITHUB_BRANCH, GITHUB_REPO, github_blob

PROMPTS: list[dict[str, str]] = [
    {
        "id": "llenar_buffer",
        "titulo": "Llenar buffer",
        "archivo": "docs/prompts/llenar_buffer.md",
        "descripcion": "Pedir a un agente externo un nuevo buffer MCS-N.",
    },
    {
        "id": "limpiar_cuarentena_pedir",
        "titulo": "Limpiar cuarentena (pedir)",
        "archivo": "docs/prompts/limpiar_cuarentena_pedir.md",
        "descripcion": "Solicitar solidificación o descarte de ítems en cuarentena L3.",
    },
    {
        "id": "limpiar_cuarentena_recibir",
        "titulo": "Limpiar cuarentena (recibir)",
        "archivo": "docs/prompts/limpiar_cuarentena_recibir.md",
        "descripcion": "Formato de respuesta del agente para convertir a buffer o sesión.",
    },
]


def foss_context() -> dict[str, object]:
    prompts = [
        {**p, "github": github_blob(p["archivo"])} for p in PROMPTS
    ]
    llms_path = "llms.md"
    return {
        "github_repo": GITHUB_REPO,
        "github_branch": GITHUB_BRANCH,
        "prompts": prompts,
        "llms_github": github_blob(llms_path),
        "llms_raw": f"{GITHUB_REPO}/raw/{GITHUB_BRANCH}/{llms_path}",
        "llms_local": "llms.md",
    }
