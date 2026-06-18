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
    p_cribar.add_argument("--caso", required=True, help="ID del caso en data/casos/")

    p_commit = sub.add_parser("commit", help="Confirmar buffer y recalcular medición")
    p_commit.add_argument("archivo", help="Ruta al buffer JSON")
    p_commit.add_argument("--caso", required=True, help="ID del caso en data/casos/")

    p_build = sub.add_parser("build", help="Generar sitios estáticos")
    p_build.add_argument(
        "--target",
        choices=["all", "prensa", "foss"],
        default="all",
    )

    p_pack = sub.add_parser("pack", help="Generar paquete ZIP de caso o medición")
    p_pack.add_argument("--caso", required=True, help="ID del caso en data/casos/")
    p_pack.add_argument("--med", help="ID de medición (M0, M1, …); omitir para zip del caso")
    p_pack.add_argument(
        "--output",
        help="Directorio de salida (default: public/prensa/downloads)",
    )

    p_catalog = sub.add_parser("catalog", help="Operaciones de catálogo")
    p_catalog_sub = p_catalog.add_subparsers(dest="catalog_cmd", required=True)
    p_catalog_sub.add_parser("sync", help="Sincronizar catalog.json desde estados")

    p_prensa = sub.add_parser("prensa", help="Operaciones de publicaciones prensa")
    p_prensa_sub = p_prensa.add_subparsers(dest="prensa_cmd", required=True)
    p_prensa_validate = p_prensa_sub.add_parser(
        "validate", help="Validar meta.json y cuerpo.html de una publicación"
    )
    p_prensa_validate.add_argument("--caso", required=True, help="ID del caso")
    p_prensa_validate.add_argument("--slug", required=True, help="Slug de la publicación")

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
    if args.command == "pack":
        from medidor_lawfare.cli.pack import run as run_pack_cmd
        return run_pack_cmd(args)
    if args.command == "catalog" and args.catalog_cmd == "sync":
        cat = sincronizar_catalog()
        print(f"Catálogo sincronizado: {len(cat['mediciones_publicas'])} mediciones")
        return 0
    if args.command == "prensa" and args.prensa_cmd == "validate":
        from medidor_lawfare.cli.prensa import run as run_prensa_cmd
        return run_prensa_cmd(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
