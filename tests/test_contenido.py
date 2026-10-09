"""Prueba de integración del contenido real con una fuente de datos sintética."""

from __future__ import annotations

from pathlib import Path

from renovable.models.servicios import ServicioInforme
from renovable.repositories.catalogos import CatalogoYaml
from tests.dobles import FuenteDatosFalsa, RegulatorioFalso

RAIZ = Path(__file__).resolve().parents[1]


def _servicio() -> ServicioInforme:
    catalogo = CatalogoYaml(RAIZ / "content", RAIZ / "data")
    return ServicioInforme(catalogo, FuenteDatosFalsa(), RegulatorioFalso())


def test_el_informe_compone_sin_marcadores_huerfanos():
    contexto = _servicio().componer(dibujar=False)
    assert contexto.errores == []
    ids = [b.id for b in contexto.bloques]
    for esperado in [
        "portada",
        "resumen_ejecutivo",
        "regulatorio",
        "energetico",
        "proyectos",
        "financiero",
        "territorial",
        "riesgos",
        "conclusiones",
        "fuentes",
    ]:
        assert esperado in ids


def test_las_cifras_aterrizan_en_el_texto():
    contexto = _servicio().componer(dibujar=False)
    resumen = next(b for b in contexto.bloques if b.id == "resumen_ejecutivo")
    assert "{" not in " ".join(resumen.parrafos)
    assert "2.725,2" in " ".join(resumen.parrafos)


def test_tablas_se_construyen_desde_las_series():
    contexto = _servicio().componer(dibujar=False)
    proyectos = next(b for b in contexto.bloques if b.id == "proyectos")
    assert proyectos.tablas, "el bloque de proyectos debe traer tablas"
    assert proyectos.tablas[0].filas, "la tabla de proyectos no puede estar vacía"
    eolica = proyectos.tablas[1]
    assert any("Guajira" in " ".join(fila) for fila in eolica.filas)


def test_kpi_de_participacion_queda_en_alerta():
    contexto = _servicio().componer(dibujar=False)
    resumen = next(b for b in contexto.bloques if b.id == "resumen_ejecutivo")
    participacion = next(k for k in resumen.kpis if k.id == "gen_renovable_pct")
    assert participacion.en_alerta is True
