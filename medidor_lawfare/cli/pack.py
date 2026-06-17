# SPDX-License-Identifier: GPL-3.0-or-later
"""CLI: medidor pack — genera paquetes ZIP de datos."""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from medidor_lawfare.paths import PUBLIC_PRENSA
from medidor_lawfare.rdb.estado import cargar_estado
from medidor_lawfare.site.packs import generar_pack_caso


def run(args: Namespace) -> int:
    caso_id = args.caso
    estado = cargar_estado(caso_id)
    dest = Path(args.output) if args.output else PUBLIC_PRENSA / "downloads"
    generados = generar_pack_caso(caso_id, estado, dest, med_id=args.med)
    for path in generados:
        print(f"Paquete generado: {path}")
    return 0
