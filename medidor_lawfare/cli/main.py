# SPDX-License-Identifier: GPL-3.0-or-later
"""Punto de entrada CLI: medidor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from medidor_lawfare.catalog.sync import sincronizar_catalog
from medidor_lawfare.cli.build import run_build


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="medidor",
        description="Medidor de Lawfare — cribado, commit, build y catálogo",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_cribar = sub.add_parser("cribar", help="Cribar buffer entrante (MCN)")
    p_cribar.add_argument("archivo", help="Ruta al buffer JSON/txt o '-' para stdin")
    p_cribar.add_argument("--caso", default="zapatero-plus-ultra")

    p_commit = sub.add_parser("commit", help="Confirmar buffer y recalcular medición")
    p_commit.add_argument("archivo", help="Ruta al buffer JSON")
    p_commit.add_argument("--caso", default="zapatero-plus-ultra")

    p_build = sub.add_parser("build", help="Generar sitios estáticos")
    p_build.add_argument(
        "--target",
        choices=["all", "prensa", "foss"],
        default="all",
    )

    p_catalog = sub.add_parser("catalog", help="Operaciones de catálogo")
    p_catalog_sub = p_catalog.add_subparsers(dest="catalog_cmd", required=True)
    p_catalog_sub.add_parser("sync", help="Sincronizar catalog.json desde estados")

    args = parser.parse_args(argv)

    if args.command == "cribar":
        from medidor_lawfare.cli.cribar import run as run_cribar_cmd
        return run_cribar_cmd(args)
    if args.command == "commit":
        from medidor_lawfare.cli.commit import run as run_commit_cmd
        return run_commit_cmd(args)
    if args.command == "build":
        run_build(target=args.target)
        return 0
    if args.command == "catalog" and args.catalog_cmd == "sync":
        cat = sincronizar_catalog()
        print(f"Catálogo sincronizado: {len(cat['mediciones_publicas'])} mediciones")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
