"""Composition root: único lugar que conoce las implementaciones concretas."""

from __future__ import annotations

from dataclasses import dataclass

from renovable.config import Settings, get_settings
from renovable.models.servicios import ServicioInforme
from renovable.repositories import (
    CatalogoYaml,
    ElecdbRepository,
    RegulatorioRepository,
    WebRepository,
)
from renovable.views import HtmlRenderer, PdfRenderer
from renovable.views.charts import RenderizadorPlotly


@dataclass
class Aplicacion:
    servicio: ServicioInforme
    html: HtmlRenderer
    pdf: PdfRenderer
    elecdb: ElecdbRepository
    regulatorio: RegulatorioRepository
    web: WebRepository
    settings: Settings


def construir(settings: Settings | None = None, dibujar: bool = True) -> Aplicacion:
    settings = settings or get_settings()
    elecdb = ElecdbRepository(settings.elecdb_dsn, settings.sql, settings.cache)
    regulatorio = RegulatorioRepository(
        settings.regulatorio, settings.datos / "preguntas_creg.yaml"
    )
    catalogo = CatalogoYaml(settings.contenido, settings.datos)
    dibujante = RenderizadorPlotly(settings.build / "figuras").dibujar if dibujar else None
    servicio = ServicioInforme(catalogo, elecdb, regulatorio, dibujante)
    return Aplicacion(
        servicio=servicio,
        html=HtmlRenderer(settings.plantillas, settings.build),
        pdf=PdfRenderer(settings.plantillas),
        elecdb=elecdb,
        regulatorio=regulatorio,
        web=WebRepository(settings.cache),
        settings=settings,
    )
