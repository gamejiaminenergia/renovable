"""Cálculo determinista de los indicadores del informe.

Recibe las series extraídas de elecdb (diccionario consulta -> filas) y devuelve
un mapa de valores. Ninguna cifra del informe se escribe a mano: todas salen de
aquí y quedan trazadas a su consulta SQL.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

Fila = dict[str, Any]


def _num(valor: Any) -> float | None:
    if valor in (None, "", "None"):
        return None
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _ultimo(filas: Iterable[Fila], clave: str = "anio") -> Fila | None:
    ordenadas = sorted(filas, key=lambda f: float(f[clave]), reverse=True)
    return ordenadas[0] if ordenadas else None


def _por_anio(filas: Iterable[Fila], anio: int) -> Fila | None:
    for fila in filas:
        if _num(fila.get("anio")) == anio:
            return fila
    return None


def _suma_enero_septiembre(filas: Iterable[Fila], anio: int) -> float:
    total = 0.0
    for fila in filas:
        mes = str(fila.get("mes", ""))
        if mes.startswith(f"{anio}-") and int(mes[5:7]) <= 9:
            total += (_num(fila.get("solar_gwh")) or 0.0) + (_num(fila.get("eolica_gwh")) or 0.0)
    return total


def calcular_kpis(datos: dict[str, list[Fila]]) -> dict[str, float]:
    """Deriva todos los indicadores publicados en el informe."""

    capacidad = datos.get("q01_capacidad_renovable_anual", [])
    mix = datos.get("q03_mix_generacion_anual", [])
    generacion = datos.get("q02_generacion_renovable_mensual", [])
    proyectos = datos.get("q04_proyectos_renovables_detalle", [])
    arranques = datos.get("q05_proyectos_por_anio", [])
    precios = datos.get("q07_precios_mensual", [])
    emisiones = datos.get("q09_factor_emision_anual", [])
    demanda = datos.get("q10_demanda_anual", [])

    anio = int(_num(_ultimo(capacidad)["anio"])) if capacidad else 0
    cap_ult = _ultimo(capacidad) or {}
    cap_solar = _num(cap_ult.get("solar_mw")) or 0.0
    cap_eolica = _num(cap_ult.get("eolica_mw")) or 0.0

    mix_2026 = _por_anio(mix, anio) or {}
    gen_solar = _num(mix_2026.get("solar_gwh")) or 0.0
    gen_eolica = _num(mix_2026.get("eolica_gwh")) or 0.0
    gen_total = sum((_num(v) or 0.0) for k, v in mix_2026.items() if k.endswith("_gwh"))
    mix_2025 = _por_anio(mix, anio - 1) or {}
    gen_total_2025 = sum((_num(v) or 0.0) for k, v in mix_2025.items() if k.endswith("_gwh"))

    parcial_2026 = _suma_enero_septiembre(generacion, 2026)
    parcial_2025 = _suma_enero_septiembre(generacion, 2025)
    crecimiento = (parcial_2026 / parcial_2025 - 1) * 100 if parcial_2025 else 0.0

    precios_2026 = [f for f in precios if str(f.get("mes", "")).startswith(f"{anio}-")]
    bolsa = [(_num(f.get("bolsa_cop_kwh")) or 0.0) for f in precios_2026]
    contratos = [(_num(f.get("contratos_cop_kwh")) or 0.0) for f in precios_2026]
    emb = [(_num(f.get("embalses_pct")) or 0.0) for f in precios_2026]

    emi_2026 = _por_anio(emisiones, anio) or {}
    factor_emision = _num(emi_2026.get("factor_emision_gco2e_kwh")) or 0.0
    gen_renovable = gen_solar + gen_eolica
    emisiones_evitadas = gen_renovable * 1e6 * factor_emision / 1e6  # GWh * gCO2e/kWh -> ton

    demanda_2026 = _por_anio(demanda, anio) or {}

    total_proyectos = sum((_num(f.get("proyectos")) or 0.0) for f in arranques)

    return {
        "anio": float(anio),
        "cap_solar_mw": cap_solar,
        "cap_eolica_mw": cap_eolica,
        "cap_renovable_mw": cap_solar + cap_eolica,
        "cap_plantas": _num(cap_ult.get("plantas_con_capacidad")) or 0.0,
        "gen_solar_gwh": gen_solar,
        "gen_eolica_gwh": gen_eolica,
        "gen_renovable_gwh": gen_renovable,
        "gen_total_gwh": gen_total,
        "gen_renovable_pct": (gen_renovable / gen_total * 100) if gen_total else 0.0,
        "gen_solar_pct": (gen_solar / gen_total * 100) if gen_total else 0.0,
        "gen_renovable_2025_gwh": (_num(mix_2025.get("solar_gwh")) or 0.0)
        + (_num(mix_2025.get("eolica_gwh")) or 0.0),
        "gen_renovable_pct_2025": (
            ((_num(mix_2025.get("solar_gwh")) or 0.0) + (_num(mix_2025.get("eolica_gwh")) or 0.0))
            / gen_total_2025
            * 100
            if gen_total_2025
            else 0.0
        ),
        "crecimiento_renovable_pct": crecimiento,
        "proyectos_mayores_50mw": float(len(proyectos)),
        "proyectos_operando": total_proyectos,
        "precio_bolsa_cop_kwh": sum(bolsa) / len(bolsa) if bolsa else 0.0,
        "precio_contratos_cop_kwh": sum(contratos) / len(contratos) if contratos else 0.0,
        "prima_bolsa_contratos_pct": (
            (sum(bolsa) / len(bolsa)) / (sum(contratos) / len(contratos)) * 100 - 100
            if contratos and sum(contratos)
            else 0.0
        ),
        "embalses_pct": sum(emb) / len(emb) if emb else 0.0,
        "factor_emision_gco2e_kwh": factor_emision,
        "emisiones_evitadas_ton": emisiones_evitadas,
        "demanda_gwh": _num(demanda_2026.get("demanda_gwh")) or 0.0,
        "demanda_max_mw": _num(demanda_2026.get("demanda_max_mw")) or 0.0,
    }
