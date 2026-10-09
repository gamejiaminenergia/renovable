"""Prueba de integración del contenido real con una fuente de datos sintética."""

from __future__ import annotations

import json
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
    assert any("Guajira" in " ".join(fila) for tabla in proyectos.tablas for fila in tabla.filas), (
        "la frontera eólica debe quedar en alguna tabla del bloque de proyectos"
    )


def test_kpi_de_participacion_queda_en_alerta():
    contexto = _servicio().componer(dibujar=False)
    resumen = next(b for b in contexto.bloques if b.id == "resumen_ejecutivo")
    participacion = next(k for k in resumen.kpis if k.id == "gen_renovable_pct")
    assert participacion.en_alerta is True


def test_cada_seccion_trae_marco_regulatorio_y_actualidad():
    contexto = _servicio().componer(dibujar=False)
    trazables = [b for b in contexto.bloques if b.exige_trazabilidad]
    assert trazables, "debe haber secciones trazables"
    for bloque in trazables:
        assert bloque.marco_regulatorio, f"{bloque.id} sin marco regulatorio"
        assert bloque.actualidad, f"{bloque.id} sin actualidad regulatoria"
        for instrumento in bloque.marco_regulatorio:
            assert instrumento.norma and instrumento.alcance


def test_actualidad_cita_la_fecha_de_verificacion():
    contexto = _servicio().componer(dibujar=False)
    regulatorio = next(b for b in contexto.bloques if b.id == "regulatorio")
    assert "{" not in regulatorio.actualidad
    assert len(regulatorio.marco_regulatorio) >= 10


def test_registro_de_instrumentos_resuelve_todos_los_ids():
    catalogo = CatalogoYaml(RAIZ / "content", RAIZ / "data")
    registro = catalogo.instrumentos()
    usados = {
        referencia
        for bloque in catalogo.bloques()
        for referencia in bloque.get("marco_regulatorio", [])
        if isinstance(referencia, str)
    }
    assert usados, "los bloques deben referenciar instrumentos regulatorios"
    assert not usados - set(registro), "hay instrumentos citados sin ficha en el registro"
    for id_instrumento, ficha in registro.items():
        assert ficha.get("norma"), f"{id_instrumento} sin norma"
        assert ficha.get("alcance"), f"{id_instrumento} sin alcance"
        assert ficha.get("vigencia"), f"{id_instrumento} sin vigencia"


def test_evidencia_regulatoria_tiene_sello_de_vigencia():
    ruta = RAIZ / "data" / "regulatorio" / "_meta.json"
    meta = json.loads(ruta.read_text(encoding="utf-8"))
    assert meta["verificado"], "la evidencia debe tener fecha de verificación"
    assert len(meta["consultas"]) == 21, "deben estar las 21 consultas CREG"
    for registro in meta["consultas"].values():
        assert registro.get("obtenido"), "cada consulta debe tener fecha de obtención"


def test_el_informe_trae_ficha_pais_y_glosario():
    contexto = _servicio().componer(dibujar=False)
    ids = [b.id for b in contexto.bloques]
    assert "ficha_pais" in ids
    assert "glosario" in ids
    glosario = next(b for b in contexto.bloques if b.id == "glosario")
    assert glosario.tablas and len(glosario.tablas[0].filas) >= 25
    assert not glosario.exige_trazabilidad


def test_la_georreferenciacion_cubre_la_mayoria_de_la_capacidad():
    contexto = _servicio().componer(dibujar=False)
    puntos = contexto.datos["geo_proyectos"]
    localizados = [p for p in puntos if p["localizado"]]
    assert len(localizados) >= 13, "deben quedar georreferenciados los proyectos clave"
    assert contexto.valores["cap_georreferenciada_pct"] >= 80
    assert contexto.valores["proyectos_sin_georreferenciar"] >= 1
    for punto in puntos:
        if punto["localizado"]:
            assert -80 < punto["lon"] < -66
            assert -5 < punto["lat"] < 14


def test_el_informe_esta_en_espanol():
    ingles = {
        "executive",
        "summary",
        "renewable",
        "energy",
        "growth",
        "framework",
        "policy",
        "figure",
        "source",
    }
    contexto = _servicio().componer(dibujar=False)
    texto = " ".join(
        " ".join([b.titulo, b.resumen, b.actualidad, *b.parrafos]) for b in contexto.bloques
    ).lower()
    encontradas = {palabra for palabra in ingles if palabra in texto.split()}
    assert not encontradas, f"texto en inglés: {encontradas}"
