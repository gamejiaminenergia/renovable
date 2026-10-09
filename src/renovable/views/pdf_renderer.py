"""Exportador PDF (WeasyPrint): única frontera con el motor de PDF."""

from __future__ import annotations

from pathlib import Path

from weasyprint import HTML


class PdfRenderer:
    def __init__(self, base_url: Path) -> None:
        self._base_url = base_url

    def exportar(self, html: str, destino: Path) -> str:
        destino.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=html, base_url=str(self._base_url)).write_pdf(str(destino))
        return str(destino)
