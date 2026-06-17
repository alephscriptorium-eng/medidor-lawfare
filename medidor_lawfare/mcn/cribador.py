# SPDX-License-Identifier: GPL-3.0-or-later
"""Cribado MCN L0-L3 para buffers sucesivos."""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any

from medidor_lawfare.motor.constantes import RANURAS_VALIDAS

L0_PATTERNS = [
    r"\b\d{4}[-/]\d{2}[-/]\d{2}\b",
    r"\b\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\b",
    r"\b(?:sentencia|auto|resolución|BOE|DOUE|TEDH|Tribunal Supremo|TSJC)\b",
    r"https?://",
    r"[«\"].{10,}[»\"]",
    r"\bart(?:ículo)?\.?\s*\d+",
    r"\b\d+\s+años\s+y\s+medio\b",
    r"\bcondenad[oa]\b",
]
L3_PATTERNS = [
    r"\b(?:creo|parece|probablemente|sin duda|evidentemente|claramente)\b",
    r"\b(?:es obvio|sin lugar a dudas|indudablemente)\b",
    r"\b(?:debería|habría que|conviene)\b",
    r"\b(?:no busca|sino la|dejó de ser|mecánica estructural|predecible)\b",
    r"\b(?:pena de telediario|inhabilitación política de facto)\b",
    r"\b(?:es muy revelador|tu medición sube)\b",
]


@dataclass
class ItemCribado:
    id: str
    texto_original: str
    capa: str
    ranura_destino: str | None
    evidencias: list[str] = field(default_factory=list)
    peso: float = 0.0
    accion: str = "cuarentena"


@dataclass
class ResultadoCribado:
    buffer_id: str
    etiqueta: str
    items: list[ItemCribado]
    cuarentena: list[ItemCribado]
    conflictos: list[ItemCribado]
    resumen_capas: dict[str, int]


def clasificar_capa(texto: str) -> str:
    texto_lower = texto.lower()
    for pat in L3_PATTERNS:
        if re.search(pat, texto_lower):
            return "L3"
    score_l0 = sum(1 for pat in L0_PATTERNS if re.search(pat, texto, re.I))
    if score_l0 >= 2:
        return "L0"
    if score_l0 == 1 or re.search(r"\b(?:según|fuente|ref\.|cit\.)\b", texto_lower):
        return "L1"
    if re.search(r"\b(?:por tanto|por lo que|esto sugiere|indica que)\b", texto_lower):
        return "L2"
    return "L1"


def peso_por_capa(capa: str) -> float:
    return {"L0": 1.0, "L1": 1.0, "L2": 0.7, "L3": 0.0, "Lx": 0.0}.get(capa, 0.0)


def inferir_ranura(texto: str) -> str | None:
    t = texto.lower()
    mapa = [
        ("mediática", "cobertura_mediatica"),
        ("prensa", "cobertura_mediatica"),
        ("titular", "cobertura_mediatica"),
        ("imput", "historico_imputaciones"),
        ("acus", "patrones_acusacion"),
        ("sentencia", "precedentes_judiciales"),
        ("juzg", "precedentes_judiciales"),
        ("elecc", "ventanas_temporales"),
        ("campaña", "ventanas_temporales"),
        ("pp ", "vectores_politicos"),
        ("psoe", "vectores_politicos"),
        ("vox", "vectores_politicos"),
        ("actor", "actores_recurrentes"),
        ("patrón", "meta_patrones_sistemicos"),
        ("comparable", "intensidad_historica_comparable"),
    ]
    for clave, ranura in mapa:
        if clave in t:
            return ranura
    return None


def cribar_item(
    texto: str,
    ranura_sugerida: str | None = None,
    bloque: str | None = None,
) -> ItemCribado:
    capa = clasificar_capa(texto)
    if bloque == "interpretativo" and capa in ("L1", "L2"):
        score_l0 = sum(1 for pat in L0_PATTERNS if re.search(pat, texto, re.I))
        if score_l0 < 2:
            capa = "L3"
    ranura = ranura_sugerida or inferir_ranura(texto)
    if ranura and ranura not in RANURAS_VALIDAS:
        ranura = None
    peso = peso_por_capa(capa)
    accion = "cargar" if capa in ("L0", "L1", "L2") and ranura else "cuarentena"
    return ItemCribado(
        id=str(uuid.uuid4())[:8],
        texto_original=texto.strip(),
        capa=capa,
        ranura_destino=ranura,
        peso=peso,
        accion=accion,
    )


def parse_texto_libre(contenido: str) -> dict[str, Any]:
    """Parsea formato --- BUFFER MCS-N --- ... --- FIN BUFFER ---"""
    match = re.search(
        r"---\s*BUFFER\s+(MCS-\d+)\s*---(.*?)---\s*FIN\s+BUFFER\s*---",
        contenido,
        re.DOTALL | re.I,
    )
    if not match:
        raise ValueError("No se encontró bloque --- BUFFER MCS-N --- ... --- FIN BUFFER ---")

    buffer_id = match.group(1).upper()
    cuerpo = match.group(2)

    etiqueta = "sin etiqueta"
    tipo = "contexto_fino"
    etq_match = re.search(r"etiqueta:\s*(.+)", cuerpo, re.I)
    if etq_match:
        etiqueta = etq_match.group(1).strip()
    tipo_match = re.search(r"tipo:\s*(\S+)", cuerpo, re.I)
    if tipo_match:
        tipo = tipo_match.group(1).strip()

    items_raw: list[tuple[str, str | None]] = []
    en_items = False
    for linea in cuerpo.splitlines():
        if re.match(r"items:\s*$", linea.strip(), re.I):
            en_items = True
            continue
        if not en_items:
            continue
        m = re.match(r"^-\s+(.+?)(?:\s*→\s*ranura:\s*(\S+))?\s*$", linea.strip())
        if m:
            items_raw.append((m.group(1).strip(), m.group(2)))

    if not items_raw:
        parrafos = [p.strip() for p in cuerpo.split("\n\n") if len(p.strip()) > 40]
        items_raw = [(p, None) for p in parrafos]

    return {
        "buffer_entrada": {
            "id": buffer_id,
            "tipo": tipo,
            "etiqueta": etiqueta,
            "items": [{"texto": t, "ranura_sugerida": r} for t, r in items_raw],
        }
    }


def cargar_buffer_desde_archivo(contenido: str) -> dict[str, Any]:
    try:
        return json.loads(contenido)
    except json.JSONDecodeError:
        return parse_texto_libre(contenido)


def procesar_buffer(data: dict[str, Any], estado: dict[str, Any]) -> ResultadoCribado:
    entrada = data["buffer_entrada"]
    buffer_id = entrada["id"]
    caso_foco = entrada.get("caso_foco", estado["caso_foco"]["id"])

    if caso_foco != estado["caso_foco"]["id"]:
        raise ValueError(
            f"Caso foco del buffer ({caso_foco}) no coincide con "
            f"{estado['caso_foco']['id']}. El foco no puede cambiar."
        )

    ids_existentes = {b["id"] for b in estado["buffers"]}
    if buffer_id in ids_existentes:
        raise ValueError(f"Buffer {buffer_id} ya existe y es inmutable.")

    items: list[ItemCribado] = []
    cuarentena: list[ItemCribado] = []

    for raw in entrada.get("items", []):
        texto = raw["texto"] if isinstance(raw, dict) else str(raw)
        ranura = raw.get("ranura_sugerida") if isinstance(raw, dict) else None
        bloque = raw.get("bloque") if isinstance(raw, dict) else None
        item = cribar_item(texto, ranura, bloque)
        if item.accion == "cargar":
            items.append(item)
        else:
            cuarentena.append(item)

    resumen: dict[str, int] = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "Lx": 0}
    for it in items + cuarentena:
        resumen[it.capa] = resumen.get(it.capa, 0) + 1

    return ResultadoCribado(
        buffer_id=buffer_id,
        etiqueta=entrada.get("etiqueta", ""),
        items=items,
        cuarentena=cuarentena,
        conflictos=[],
        resumen_capas=resumen,
    )


def resultado_a_dict(resultado: ResultadoCribado) -> dict[str, Any]:
    return {
        "buffer_id": resultado.buffer_id,
        "etiqueta": resultado.etiqueta,
        "resumen_capas": resultado.resumen_capas,
        "items": [asdict(i) for i in resultado.items],
        "cuarentena": [asdict(i) for i in resultado.cuarentena],
    }


def buffer_num(buffer_id: str) -> int:
    """Extrae el número de un buffer_id 'MCS-N' → N."""
    return int(buffer_id.split("-")[-1])


def calcular_pct_l3(resultado: ResultadoCribado) -> float:
    """Porcentaje de ítems L3 sobre el total del resultado."""
    total = sum(resultado.resumen_capas.values())
    return resultado.resumen_capas.get("L3", 0) / max(1, total)
