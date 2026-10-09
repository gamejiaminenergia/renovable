"""Renderizador HTML (Jinja2): única frontera con el motor de plantillas."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from renovable.models.entidades import Bloque


class HtmlRenderer:
    def __init__(self, dir_plantillas: Path, dir_build: Path) -> None:
        self._env = Environment(
            loader=FileSystemLoader(str(dir_plantillas)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._env.filters["miles"] = lambda v: f"{float(v):,.0f}".replace(",", ".")
        self._dir_build = dir_build
        self._dir_build.mkdir(parents=True, exist_ok=True)

    def renderizar(self, bloques: list[Bloque], contexto: dict[str, Any]) -> str:
        plantilla = self._env.get_template("informe.html.j2")
        html = plantilla.render(bloques=bloques, **contexto)
        (self._dir_build / "informe.html").write_text(html, encoding="utf-8")
        return html
