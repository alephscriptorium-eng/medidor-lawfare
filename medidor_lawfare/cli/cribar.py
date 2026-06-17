# SPDX-License-Identifier: GPL-3.0-or-later
"""Comando medidor cribar."""

from __future__ import annotations

import json
import sys
from argparse import Namespace
from pathlib import Path

from medidor_lawfare.mcn.cribador import (
    calcular_pct_l3,
    cargar_buffer_desde_archivo,
    procesar_buffer,
    resultado_a_dict,
)
from medidor_lawfare.paths import cribados_dir
from medidor_lawfare.rdb.estado import cargar_estado


def run(args: Namespace) -> int:
    caso_id = args.caso
    estado = cargar_estado(caso_id)
    arg = args.archivo

    if arg == "-":
        contenido = sys.stdin.read()
    else:
        contenido = Path(arg).read_text(encoding="utf-8")

    data = cargar_buffer_desde_archivo(contenido)
    resultado = procesar_buffer(data, estado)

    caso = estado["caso_foco"]["etiqueta"]
    activa = estado["branches"]["main"]["medicion_activa"]
    med_keys = {v["id"]: v for v in estado["mediciones"].values()}
    m_ref = med_keys.get(activa, list(estado["mediciones"].values())[-1])

    print("=" * 60)
    print(f"CASO FOCO: {caso} (inmutable)")
    print(f"BUFFER ENTRANTE: {resultado.buffer_id} — {resultado.etiqueta}")
    print(f"BUFFERS EXISTENTES (intactos): {[b['id'] for b in estado['buffers']]}")
    print("=" * 60)
    print("\nCRIBADO MCN:")
    for capa, n in sorted(resultado.resumen_capas.items()):
        if n:
            print(f"  {capa}: {n}")
    print(f"  → Cargables: {len(resultado.items)} | Cuarentena: {len(resultado.cuarentena)}")

    if resultado.cuarentena:
        print("\nCUARENTENA (L3/sin ranura — no alteran medición):")
        for it in resultado.cuarentena[:5]:
            print(f"  [{it.capa}] {it.texto_original[:80]}...")
        if len(resultado.cuarentena) > 5:
            print(f"  ... y {len(resultado.cuarentena) - 5} más")

    print("\nÍTEMS APROBADOS PARA CARGA:")
    for it in resultado.items[:10]:
        print(f"  [{it.capa} w={it.peso}] → {it.ranura_destino}: {it.texto_original[:70]}...")
    if len(resultado.items) > 10:
        print(f"  ... y {len(resultado.items) - 10} más")

    pct_l3 = calcular_pct_l3(resultado)
    print("\n" + "-" * 60)
    print(f"REFERENCIA {activa} (última medición):")
    print(f"  Intensidad: {m_ref['intensidad']} | Vector: {m_ref['ejes']['vector']}")
    print("\nPRÓXIMO PASO:")
    if pct_l3 > 0.4:
        print("  ⚠ >40% L3 — recomendar branch alternativo o revisión manual")
    print("  Confirmar commit del buffer para calcular siguiente medición")
    print("=" * 60)

    out_dir = cribados_dir(caso_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"cribado-{resultado.buffer_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resultado_a_dict(resultado), f, ensure_ascii=False, indent=2)
    print(f"\nCribado guardado en: {out_path}")
    return 0
