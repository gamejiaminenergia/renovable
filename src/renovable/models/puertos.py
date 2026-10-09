"""Puertos (Protocols) que aíslan el modelo de las librerías externas."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Protocol

from renovable.models.entidades import Bloque, Fuente


class FuenteDatos(Protocol):
    """Acceso a series del mercado mayorista (elecdb)."""

    def serie(self, consulta: str, refrescar: bool = False) -> list[dict[str, Any]]: ...

    def disponibles(self) -> Sequence[str]: ...


class FuenteRegulatoria(Protocol):
    """Acceso a la evidencia normativa recogida del asistente CREG."""

    def respuestas(self) -> dict[str, str]: ...

    def preguntas(self) -> list[dict[str, str]]: ...


class FuenteWeb(Protocol):
    """Acceso a fuentes públicas de internet con caché local."""

    def obtener(self, url: str, refrescar: bool = False) -> str: ...


class Catalogo(Protocol):
    """Acceso a los catálogos YAML que definen el informe."""

    def manifiesto(self) -> dict[str, Any]: ...

    def bloques(self) -> list[dict[str, Any]]: ...

    def kpis(self) -> dict[str, dict[str, Any]]: ...

    def fuentes(self) -> list[Fuente]: ...

    def pipeline(self) -> list[dict[str, Any]]: ...


class RenderizadorGraficas(Protocol):
    """Convierte una gráfica en un archivo de imagen."""

    def dibujar(self, figura_id: str, datos: Any) -> str: ...


class Renderizador(Protocol):
    """Convierte los bloques del informe en HTML o PDF."""

    def renderizar(self, bloques: list[Bloque], contexto: dict[str, Any]) -> str: ...


class ExportadorPdf(Protocol):
    """Exporta un HTML ya compuesto a un archivo PDF."""

    def exportar(self, html: str, destino: Path) -> str: ...
