"""QA del documento: HTML y PDF se generan con las secciones exigidas."""

from __future__ import annotations

from pathlib import Path

import pytest

from renovable.models.servicios import ServicioInforme
from renovable.repositories.catalogos import CatalogoYaml
from renovable.views import HtmlRenderer, PdfRenderer
from tests.dobles import FuenteDatosFalsa, RegulatorioFalso

RAIZ = Path(__file__).resolve().parents[1]


def _contexto():
    catalogo = CatalogoYaml(RAIZ / "content", RAIZ / "data")
    servicio = ServicioInforme(catalogo, FuenteDatosFalsa(), RegulatorioFalso())
    return catalogo, servicio.componer(dibujar=False)


def test_html_incluye_las_secciones_y_las_cajas():
    _, contexto = _contexto()
    renderer = HtmlRenderer(RAIZ / "templates", RAIZ / "build")
    html = renderer.renderizar(
        contexto.bloques,
        {
            "meta": contexto.meta,
            "fuentes": contexto.fuentes,
            "indice": contexto.indice,
            "corte": contexto.corte,
        },
    )
    assert "Resumen ejecutivo" in html
    assert "Dimensión regulatoria" in html
    assert "Conclusión" in html
    assert "Advertencia" in html
    assert "Tip" in html
    assert "target" not in html or html.count("<a") >= 10
    assert (RAIZ / "build" / "informe.html").exists()


def test_pdf_se_exporta_con_todas_las_paginas(tmp_path):
    _, contexto = _contexto()
    html = HtmlRenderer(RAIZ / "templates", RAIZ / "build").renderizar(
        contexto.bloques,
        {
            "meta": contexto.meta,
            "fuentes": contexto.fuentes,
            "indice": contexto.indice,
            "corte": contexto.corte,
        },
    )
    destino = tmp_path / "informe.pdf"
    PdfRenderer(RAIZ / "templates").exportar(html, destino)
    assert destino.exists() and destino.stat().st_size > 20_000
    from pypdf import PdfReader  # noqa: PLC0415

    lector = PdfReader(str(destino))
    assert len(lector.pages) >= 10, "el informe debe superar las diez páginas"


def test_generador_rechaza_marcadores_inexistentes():
    catalogo = CatalogoYaml(RAIZ / "content", RAIZ / "data")
    servicio = ServicioInforme(catalogo, FuenteDatosFalsa(), RegulatorioFalso())
    with pytest.raises(KeyError):
        servicio._resolver_texto("valor {no_existe}", {"existe": "1"})
