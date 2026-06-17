# SPDX-License-Identifier: GPL-3.0-or-later
"""Generación de paquetes ZIP estáticos para prensa."""

from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from medidor_lawfare import __version__
from medidor_lawfare.paths import BUFFERS_DIR, PROJECT_ROOT, caso_dir
from medidor_lawfare.site.prensa_context import buffer_para_medicion


@dataclass
class PackContents:
    files: list[tuple[Path, str]] = field(default_factory=list)
    generated: list[tuple[str, str]] = field(default_factory=list)
    omitidos: list[str] = field(default_factory=list)

    def arcnames(self) -> list[str]:
        names = [arc for _, arc in self.files]
        names.extend(arc for _, arc in self.generated)
        return sorted(names)


def _medicion_por_id(estado: dict[str, Any], med_id: str) -> dict[str, Any] | None:
    for med in estado.get("mediciones", {}).values():
        if med.get("id") == med_id:
            return med
    if med_id == "M0":
        baseline = estado.get("mediciones", {}).get("baseline")
        if baseline:
            return baseline
    return None


def _snapshot_medicion(medicion: dict[str, Any]) -> str:
    snap = {
        "id": medicion["id"],
        "ejes": medicion.get("ejes", {}),
        "intensidad": medicion["intensidad"],
        "lectura": medicion["lectura"],
        "buffers_activos": medicion.get("buffers_activos", []),
    }
    return json.dumps(snap, ensure_ascii=False, indent=2) + "\n"


def _add_file(
    path: Path, arcname: str, contents: PackContents
) -> None:
    if path.exists():
        contents.files.append((path, arcname))
    else:
        contents.omitidos.append(arcname)


def _sesion_path(buffer_id: str) -> Path:
    num = buffer_id.rsplit("-", 1)[-1]
    return PROJECT_ROOT / f"docs/sesiones/buffer-{int(num):02d}.md"


def archivos_medicion(
    caso_id: str, med_id: str, estado: dict[str, Any]
) -> PackContents:
    contents = PackContents()
    cdir = caso_dir(caso_id)

    _add_file(cdir / "caso.json", "caso.json", contents)

    medicion = _medicion_por_id(estado, med_id)
    if medicion:
        contents.generated.append(
            (_snapshot_medicion(medicion), f"medicion/{med_id}.json")
        )
    else:
        contents.omitidos.append(f"medicion/{med_id}.json")

    if med_id == "M0":
        return contents

    delta, buffer = buffer_para_medicion(estado, med_id, caso_id)
    if delta:
        contents.generated.append(
            (
                json.dumps(delta, ensure_ascii=False, indent=2) + "\n",
                f"delta/{delta['id']}.json",
            )
        )
    if buffer:
        bid = buffer["id"]
        _add_file(
            BUFFERS_DIR / f"{bid}-entrada.json",
            f"buffers/{bid}-entrada.json",
            contents,
        )
        _add_file(
            cdir / "cribados" / f"cribado-{bid}.json",
            f"cribados/cribado-{bid}.json",
            contents,
        )
        sesion = _sesion_path(bid)
        if sesion.exists():
            contents.files.append(
                (sesion, f"docs/sesiones/buffer-{int(buffer['num']):02d}.md")
            )
        else:
            contents.omitidos.append(
                f"docs/sesiones/buffer-{int(buffer['num']):02d}.md"
            )

    return contents


def archivos_caso(caso_id: str, estado: dict[str, Any]) -> PackContents:
    contents = PackContents()
    cdir = caso_dir(caso_id)

    _add_file(cdir / "caso.json", "caso.json", contents)
    _add_file(cdir / "estado.json", "estado.json", contents)

    cribados = cdir / "cribados"
    if cribados.is_dir():
        for cribado in sorted(cribados.glob("*.json")):
            contents.files.append(
                (cribado, f"cribados/{cribado.name}")
            )

    for buf in estado.get("buffers", []):
        bid = buf["id"]
        _add_file(
            BUFFERS_DIR / f"{bid}-entrada.json",
            f"buffers/{bid}-entrada.json",
            contents,
        )
        num = bid.rsplit("-", 1)[-1]
        sesion = _sesion_path(bid)
        arc = f"docs/sesiones/buffer-{int(num):02d}.md"
        if sesion.exists():
            contents.files.append((sesion, arc))
        else:
            contents.omitidos.append(arc)

    return contents


def generar_readme(
    tipo: Literal["medicion", "caso"],
    caso_id: str,
    med_id: str | None,
    version: str,
    arcnames: list[str],
    omitidos: list[str],
) -> str:
    if tipo == "medicion":
        titulo = f"Paquete de medición {med_id} — caso {caso_id}"
    else:
        titulo = f"Paquete completo del caso {caso_id}"

    lines = [
        titulo,
        f"Motor Medidor de Lawfare v{version}",
        "Licencia: GPL-3.0-or-later",
        "",
        "Archivos incluidos:",
    ]
    for name in arcnames:
        lines.append(f"  - {name}")
    if omitidos:
        lines.append("")
        lines.append("Archivos referenciados no encontrados (omitidos):")
        for name in omitidos:
            lines.append(f"  - {name}")
    lines.append("")
    lines.append(
        "Generado con medidor build. Fuente canónica: repositorio medidor-lawfare."
    )
    return "\n".join(lines) + "\n"


def escribir_zip(dest: Path, contents: PackContents, readme: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.txt", readme)
        for path, arcname in contents.files:
            zf.write(path, arcname)
        for data, arcname in contents.generated:
            zf.writestr(arcname, data)


def _version_estado(estado: dict[str, Any]) -> str:
    return estado.get("motor_version") or __version__


def generar_packs_prensa(
    catalog: dict[str, Any],
    estados: dict[str, dict[str, Any]],
    dest_dir: Path,
) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    generados: list[Path] = []

    for med in catalog.get("mediciones_publicas", []):
        med_id = med["id"]
        caso_id = med["caso_id"]
        estado = estados.get(caso_id, {})
        contents = archivos_medicion(caso_id, med_id, estado)
        readme = generar_readme(
            "medicion",
            caso_id,
            med_id,
            _version_estado(estado),
            contents.arcnames(),
            contents.omitidos,
        )
        dest = dest_dir / f"{caso_id}-{med_id}.zip"
        escribir_zip(dest, contents, readme)
        generados.append(dest)

    for caso in catalog.get("casos", []):
        caso_id = caso["id"]
        estado = estados.get(caso_id, {})
        contents = archivos_caso(caso_id, estado)
        readme = generar_readme(
            "caso",
            caso_id,
            None,
            _version_estado(estado),
            contents.arcnames(),
            contents.omitidos,
        )
        dest = dest_dir / f"{caso_id}.zip"
        escribir_zip(dest, contents, readme)
        generados.append(dest)

    return generados


def generar_pack_caso(
    caso_id: str,
    estado: dict[str, Any],
    dest_dir: Path,
    med_id: str | None = None,
) -> list[Path]:
    """CLI: genera zip(s) de un caso sin rebuild completo."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    generados: list[Path] = []

    if med_id:
        contents = archivos_medicion(caso_id, med_id, estado)
        readme = generar_readme(
            "medicion",
            caso_id,
            med_id,
            _version_estado(estado),
            contents.arcnames(),
            contents.omitidos,
        )
        dest = dest_dir / f"{caso_id}-{med_id}.zip"
        escribir_zip(dest, contents, readme)
        generados.append(dest)
    else:
        contents = archivos_caso(caso_id, estado)
        readme = generar_readme(
            "caso",
            caso_id,
            None,
            _version_estado(estado),
            contents.arcnames(),
            contents.omitidos,
        )
        dest = dest_dir / f"{caso_id}.zip"
        escribir_zip(dest, contents, readme)
        generados.append(dest)

    return generados
