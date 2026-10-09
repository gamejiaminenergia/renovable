"""Dobles de prueba: series sintéticas para no depender de la base ni de la red."""

from __future__ import annotations

from typing import Any


def series_sinteticas() -> dict[str, list[dict[str, Any]]]:
    return {
        "q01_capacidad_renovable_anual": [
            {"anio": 2020, "solar_mw": 60.8, "eolica_mw": 0.0, "plantas_con_capacidad": 10},
            {"anio": 2025, "solar_mw": 2301.3, "eolica_mw": 41.1, "plantas_con_capacidad": 1075},
            {"anio": 2026, "solar_mw": 2725.2, "eolica_mw": 42.3, "plantas_con_capacidad": 2019},
        ],
        "q02_generacion_renovable_mensual": [
            {"mes": "2025-01", "solar_gwh": 300.0, "eolica_gwh": 12.0},
            {"mes": "2025-09", "solar_gwh": 400.0, "eolica_gwh": 13.0},
            {"mes": "2026-01", "solar_gwh": 500.0, "eolica_gwh": 14.0},
            {"mes": "2026-09", "solar_gwh": 700.0, "eolica_gwh": 15.0},
        ],
        "q03_mix_generacion_anual": [
            {
                "anio": 2025,
                "hidro_gwh": 68099.4,
                "termica_gwh": 10710.9,
                "solar_gwh": 4473.8,
                "eolica_gwh": 154.9,
                "biomasa_gwh": 972.9,
            },
            {
                "anio": 2026,
                "hidro_gwh": 46977.6,
                "termica_gwh": 12494.5,
                "solar_gwh": 5150.1,
                "eolica_gwh": 153.3,
                "biomasa_gwh": 757.4,
            },
        ],
        "q04_proyectos_renovables_detalle": [
            {
                "proyecto": "GUAYEPO",
                "fuente": "RAD SOLAR",
                "capacidad_mw": 388.0,
                "gen_2026_gwh": 600.0,
                "fecha_operacion": "2024-06-30",
            },
            {
                "proyecto": "PARQUE SOLAR PUERTA DE ORO",
                "fuente": "RAD SOLAR",
                "capacidad_mw": 300.0,
                "gen_2026_gwh": 480.0,
                "fecha_operacion": "2025-03-31",
            },
        ],
        "q05_proyectos_por_anio": [
            {"anio": 2024, "proyectos": 484, "fuente": "RAD SOLAR"},
            {"anio": 2025, "proyectos": 739, "fuente": "RAD SOLAR"},
        ],
        "q06_rendimiento_solar_mensual": [
            {
                "mes": "2026-06",
                "irr_global_wh_m2": 381.0,
                "temp_ambiente_c": 27.2,
                "temp_panel_c": 38.3,
                "registros": 504,
            }
        ],
        "q07_precios_mensual": [
            {
                "mes": "2026-09",
                "bolsa_cop_kwh": 683.7,
                "contratos_cop_kwh": 322.0,
                "escasez_cop_kwh": 698.6,
                "embalses_pct": 76.1,
                "demanda_prom_gwh_dia": 243.01,
            },
            {
                "mes": "2026-08",
                "bolsa_cop_kwh": 948.2,
                "contratos_cop_kwh": 331.5,
                "escasez_cop_kwh": 667.0,
                "embalses_pct": 78.8,
                "demanda_prom_gwh_dia": 198.80,
            },
        ],
        "q08_embalses_mensual": [
            {
                "mes": "2026-09",
                "embalses_pct": 76.1,
                "aportes_gwh": 0.0,
                "aportes_vs_media_pct": 90.0,
                "vertimientos_gwh": 0.0,
            }
        ],
        "q09_factor_emision_anual": [
            {
                "anio": 2026,
                "generacion_gwh": 65532.9,
                "emisiones_ton_co2e": 1868678.0,
                "factor_emision_gco2e_kwh": 28.5,
            }
        ],
        "q10_demanda_anual": [{"anio": 2026, "demanda_gwh": 63300.1, "demanda_max_mw": 12683}],
        "q11_cargos_mensuales": [
            {
                "mes": "2026-08",
                "cee": 67.8,
                "cere": 66.9,
                "mc": 330.98,
                "cargo_uso_stn": 363709927420,
                "cargo_uso_str": 242337842375.8,
                "prec_fazni": 3.2695,
                "faer": 0,
            }
        ],
        "q12_perfil_horario_solar": [
            {"hora": 12, "solar_promedio_mw": 2340},
            {"hora": 18, "solar_promedio_mw": 4},
        ],
        "q13_geo_municipios": [
            {
                "cod_mpio": codigo,
                "cod_dpto": codigo[:2],
                "departamento": departamento,
                "municipio": municipio,
                "latitud": latitud,
                "longitud": longitud,
                "fuente": "DIVIPOLA (datos.gov.co, dataset gdxc-w37w)",
            }
            for codigo, departamento, municipio, latitud, longitud in [
                ("25320", "CUNDINAMARCA", "GUADUAS", 5.0694, -74.5964),
                ("08638", "ATLÁNTICO", "SABANALARGA", 10.6307, -74.9209),
                ("73001", "TOLIMA", "IBAGUÉ", 4.4389, -75.2322),
                ("20250", "CESAR", "EL PASO", 9.7186, -73.4376),
                ("23001", "CÓRDOBA", "MONTERÍA", 8.7480, -75.8814),
                ("47288", "MAGDALENA", "FUNDACIÓN", 10.5207, -74.1851),
                ("17380", "CALDAS", "LA DORADA", 5.4561, -74.6660),
                ("20383", "CESAR", "LA GLORIA", 8.6217, -73.8047),
                ("08433", "ATLÁNTICO", "MALAMBO", 10.8583, -74.7744),
                ("44847", "LA GUAJIRA", "URIBIA", 11.7139, -72.2664),
            ]
        ],
        "q14_agentes_solar_energetico": [
            {
                "agente_code": "ENDG",
                "agente": "ENEL COLOMBIA SA ESP",
                "plantas": 11,
                "plantas_con_capacidad": 11,
                "capacidad_mw": 1110.4,
                "generacion_gwh": 1700.6,
                "generacion_capacitada_gwh": 1699.0,
                "capacidad_kwh_periodo": 7248691200,
                "enficc_kwh": 6039622,
                "oef_kwh": 4158344,
            },
            {
                "agente_code": "OROG",
                "agente": "PARQUE SOLAR PUERTA DE ORO S.A.S. E.S.P.",
                "plantas": 1,
                "plantas_con_capacidad": 1,
                "capacidad_mw": 300.0,
                "generacion_gwh": 481.6,
                "generacion_capacitada_gwh": 481.6,
                "capacidad_kwh_periodo": 1958400000,
                "enficc_kwh": 1395372,
                "oef_kwh": 190142,
            },
            {
                "agente_code": "ISGG",
                "agente": "ISAGEN S.A. E.S.P.",
                "plantas": 11,
                "plantas_con_capacidad": 11,
                "capacidad_mw": 297.3,
                "generacion_gwh": 560.1,
                "generacion_capacitada_gwh": 560.1,
                "capacidad_kwh_periodo": 1940774400,
                "enficc_kwh": 832958,
                "oef_kwh": 1620321,
            },
            {
                "agente_code": "EPSG",
                "agente": "CELSIA COLOMBIA S.A. E.S.P.",
                "plantas": 56,
                "plantas_con_capacidad": 56,
                "capacidad_mw": 111.6,
                "generacion_gwh": 670.9,
                "generacion_capacitada_gwh": 116.6,
                "capacidad_kwh_periodo": 728394240,
                "enficc_kwh": 538377,
                "oef_kwh": 2496017,
            },
        ],
        "q15_agentes_solar_financiero": [
            {
                "agente_code": "ENDG",
                "agente": "ENEL COLOMBIA SA ESP",
                "actividad": "GENERACIÓN",
                "ventas_contratos_gwh": 11939.9,
                "ventas_bolsa_gwh": 2819.1,
                "compras_contratos_gwh": 3090.2,
                "compras_bolsa_gwh": 638.2,
                "pct_ventas_contratos": 80.9,
            },
            {
                "agente_code": "EPSG",
                "agente": "CELSIA COLOMBIA S.A. E.S.P.",
                "actividad": "GENERACIÓN",
                "ventas_contratos_gwh": 3239.9,
                "ventas_bolsa_gwh": 555.1,
                "compras_contratos_gwh": 498.8,
                "compras_bolsa_gwh": 478.0,
                "pct_ventas_contratos": 85.4,
            },
        ],
    }


class FuenteDatosFalsa:
    def __init__(self, series: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self._series = series if series is not None else series_sinteticas()

    def disponibles(self):
        return list(self._series)

    def serie(self, consulta: str, refrescar: bool = False):
        return self._series.get(consulta, [])

    def extraer_todo(self, refrescar: bool = False):
        return dict(self._series)


class RegulatorioFalso:
    def preguntas(self):
        return [{"id": "R01_marco_general", "eje": "Marco regulatorio", "pregunta": "?"}]

    def respuestas(self):
        return {"R01_marco_general": "contenido"}

    def faltantes(self):
        return []

    def disponible(self, id_consulta: str) -> bool:
        return True
