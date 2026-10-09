"""Las gráficas del informe se exportan en SVG y son autocontenidas."""

from __future__ import annotations

from pathlib import Path

import pytest

from renovable.views.charts import figuras
from renovable.views.charts.renderer import RenderizadorPlotly
from tests.dobles import series_sinteticas

RAIZ = Path(__file__).resolve().parents[1]

SERIES = {"q01": "q01_capacidad_renovable_anual", "q03": "q03_mix_generacion_anual"}


def test_todas_las_figuras_estan_registradas():
    catalogo = (RAIZ / "data" / "catalogo_graficas.yaml").read_text(encoding="utf-8")
    for figura_id in figuras.REGISTRO:
        assert figura_id in catalogo, f"{figura_id} no está en catalogo_graficas.yaml"


def test_el_renderizador_exporta_svg(tmp_path):
    renderizador = RenderizadorPlotly(tmp_path)
    archivo = renderizador.dibujar("fig_mix_anual", series_sinteticas())
    ruta = Path(archivo)
    assert ruta.suffix == ".svg", "todas las imágenes del informe deben ser SVG"
    assert ruta.exists() and ruta.stat().st_size > 1000
    assert ruta.read_text(encoding="utf-8").lstrip().startswith("<svg")


def test_no_queda_ninguna_imagen_png_en_el_catalogo():
    for definicion in figuras.REGISTRO:
        assert not definicion.endswith(".png")


def test_el_mapa_necesita_puntos_georreferenciados():
    with pytest.raises(ValueError):
        figuras.mapa_proyectos([{"tecnologia": "Solar FV", "capacidad_mw": 10.0}])
