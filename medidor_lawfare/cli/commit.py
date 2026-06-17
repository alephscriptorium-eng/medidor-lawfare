# SPDX-License-Identifier: GPL-3.0-or-later
"""Comando medidor commit."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from medidor_lawfare.rdb.estado import commit_buffer, estado_path


def run(args: Namespace) -> int:
    caso_id = args.caso
    path = Path(args.archivo)
    out = commit_buffer(caso_id, path)
    r = out["resultado"]
    m_prev, m_new, d = out["prev"], out["new"], out["delta"]

    print("=" * 64)
    print(f"CASO: {caso_id}")
    print(f"BRANCH: main | BUFFERS: {', '.join(m_new['buffers_activos'])}")
    print("=" * 64)
    print(f"\nCRIBADO {r.buffer_id}:")
    for capa, n in sorted(r.resumen_capas.items()):
        if n:
            print(f"  {capa}: {n}")
    print(f"  Cargables: {len(r.items)} | Cuarentena: {len(r.cuarentena)} | L3%: {out['pct_l3']:.0%}")

    if r.cuarentena:
        print("\nCUARENTENA (no alteran medición):")
        for it in r.cuarentena:
            print(f"  [{it.capa}] {it.texto_original[:75]}...")

    print("\n" + "-" * 64)
    print(f"MEDICIÓN {d['desde']} → {d['hasta']}")
    for eje in m_prev["ejes"]:
        print(
            f"  {eje.capitalize():12} {m_prev['ejes'][eje]} → {m_new['ejes'][eje]}  "
            f"(Δ {d['delta_ejes'][eje]:+.2f})"
        )
    print(f"\n  INTENSIDAD:  {m_prev['intensidad']} → {m_new['intensidad']}  (Δ {d['delta_intensidad']:+.2f})")
    print(f"  Lectura:     {m_new['lectura']}")
    print(f"  Dirección:   {d['direccion']} | {d.get('clasificacion_impacto', '')}")
    print("=" * 64)
    print(f"\nEstado: {estado_path(caso_id)}")
    print(f"Cribado: {out['cribado_path']}")
    return 0
