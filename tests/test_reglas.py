"""Pruebas de las reglas de negocio: KPI, formato y validación."""

from __future__ import annotations

import pytest

from renovable.models.entidades import Bloque, Figura, Fuente, Kpi
from renovable.models.reglas.formato import fecha_es, numero, porcentaje
from renovable.models.reglas.kpis import calcular_kpis
from renovable.models.reglas.validacion import numerar_paginas, validar_informe
from tests.dobles import series_sinteticas


def test_formato_colombiano():
    assert numero(2725.24, 1) == "2.725,2"
    assert numero(151146.9, 0) == "151.147"
    assert porcentaje(8.09, 1) == "8,1 %"
    assert fecha_es("2026-09-30") == "30 de septiembre de 2026"
    assert fecha_es(None) == "—"


def test_kpis_se_calculan_desde_las_series():
    kpis = calcular_kpis(series_sinteticas())
    assert kpis["anio"] == 2026
    assert kpis["cap_solar_mw"] == pytest.approx(2725.2)
    assert kpis["cap_renovable_mw"] == pytest.approx(2725.2 + 42.3)
    assert kpis["gen_renovable_gwh"] == pytest.approx(5303.4)
    assert kpis["gen_renovable_pct"] == pytest.approx(5303.4 / 65532.9 * 100)
    assert kpis["crecimiento_renovable_pct"] == pytest.approx((1229 / 725 - 1) * 100)
    assert kpis["proyectos_mayores_50mw"] == 2


def test_kpi_en_alerta_segun_direccion():
    kpi = Kpi(
        id="x",
        etiqueta="Participación",
        valor=8.1,
        unidad="%",
        periodo="2026",
        fuente="XM",
        direccion="up",
        umbral_alerta=20,
    )
    assert kpi.en_alerta is True
    kpi_ok = Kpi(
        id="y",
        etiqueta="Precio",
        valor=300,
        unidad="COP/kWh",
        periodo="2026",
        fuente="XM",
        direccion="down",
        umbral_alerta=400,
    )
    assert kpi_ok.en_alerta is False


def _bloque_valido() -> Bloque:
    return Bloque(
        id="seccion",
        tipo="seccion",
        titulo="Sección",
        parrafos=["texto"],
        conclusion="conclusión",
        tip="tip",
        advertencia="advertencia",
        metodo="q01",
        fuentes=["elecdb"],
    )


def test_validacion_exige_trazabilidad():
    assert validar_informe([_bloque_valido()]) == [
        "informe: falta portada",
        "informe: faltan conclusiones",
    ]
    incompleto = Bloque(id="x", tipo="seccion", titulo="X", parrafos=["a"])
    errores = validar_informe([incompleto])
    assert any("sin fuente" in e for e in errores)
    assert any("sin tip" in e for e in errores)
    assert any("sin advertencia" in e for e in errores)


def test_figura_sin_leyenda_falla():
    bloque = _bloque_valido()
    bloque.figuras = [Figura(id="f", titulo="F", archivo="x.png")]
    errores = validar_informe([bloque])
    assert any("sin leyenda" in e for e in errores)
    assert any("sin fuente" in e for e in errores)


def test_numerar_paginas_es_contiguo():
    bloques = numerar_paginas([_bloque_valido(), _bloque_valido()])
    assert [b.pagina for b in bloques] == [1, 2]


def test_portada_y_fuentes_no_exigen_trazabilidad():
    portada = Bloque(id="portada", tipo="portada", titulo="Portada")
    fuentes = Bloque(id="fuentes", tipo="fuentes", titulo="Fuentes")
    assert validar_informe([portada, fuentes]) == ["informe: faltan conclusiones"]


def test_fuente_expone_enlace():
    assert Fuente(id="a", titulo="A", url="https://x").enlace == "https://x"
