# SPDX-License-Identifier: GPL-3.0-or-later
"""CLI: medidor prensa validate."""

from __future__ import annotations

import argparse

from medidor_lawfare.site.prensa_publicaciones import validar_publicacion


def run(args: argparse.Namespace) -> int:
    ok, errores = validar_publicacion(args.caso, args.slug)
    if ok:
        print(f"OK: {args.caso}/{args.slug}")
        return 0
    for err in errores:
        print(f"ERROR: {err}")
    return 1
