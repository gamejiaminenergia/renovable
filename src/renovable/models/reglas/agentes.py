"""Análisis de la participación empresarial en la generación solar.

Combina la participación energética (capacidad, generación, energía firme) con la
participación financiera (ventas en contratos y en bolsa) de cada agente. Las
ventas del mercado se reportan a nivel de agente porque XM no las desagrega por
tecnología: el informe lo declara y usa la generación solar como base para
valorar la energía.
"""

from __future__ import annotations

from typing import Any

Fila = dict[str, Any]


def _num(valor: Any) -> float:
    if valor in (None, "", "None"):
        return 0.0
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0


def analizar_agentes_solar(
    energetico: list[Fila],
    financiero: list[Fila],
    precio_bolsa: float,
    precio_contratos: float,
) -> dict[str, Any]:
    """Cruza las dos miradas y devuelve filas ordenadas más el resumen de mercado."""

    fin = {str(f.get("agente_code")): f for f in financiero}
    total_mw = sum(_num(e.get("capacidad_mw")) for e in energetico)
    total_gen = sum(_num(e.get("generacion_gwh")) for e in energetico)

    filas: list[Fila] = []
    for entrada in energetico:
        mw = _num(entrada.get("capacidad_mw"))
        gen = _num(entrada.get("generacion_gwh"))
        cap_kwh = _num(entrada.get("capacidad_kwh_periodo"))
        gen_cap = _num(entrada.get("generacion_capacitada_gwh"))
        ventas = fin.get(str(entrada.get("agente_code")), {})
        filas.append(
            {
                "agente_code": entrada.get("agente_code", ""),
                "agente": entrada.get("agente", ""),
                "plantas": _num(entrada.get("plantas")),
                "capacidad_mw": mw,
                "generacion_gwh": gen,
                "factor_planta_pct": (gen_cap * 1e6 / cap_kwh * 100) if cap_kwh else 0.0,
                "share_capacidad_pct": (mw / total_mw * 100) if total_mw else 0.0,
                "share_generacion_pct": (gen / total_gen * 100) if total_gen else 0.0,
                "enficc_kwh": _num(entrada.get("enficc_kwh")),
                "oef_kwh": _num(entrada.get("oef_kwh")),
                "ventas_contratos_gwh": _num(ventas.get("ventas_contratos_gwh")),
                "ventas_bolsa_gwh": _num(ventas.get("ventas_bolsa_gwh")),
                "pct_ventas_contratos": _num(ventas.get("pct_ventas_contratos")),
                "valor_bolsa_cop": gen * 1e6 * precio_bolsa,
                "valor_contratos_cop": gen * 1e6 * precio_contratos,
            }
        )

    filas.sort(key=lambda f: f["capacidad_mw"], reverse=True)
    acumulado = 0.0
    for fila in filas:
        acumulado += fila["share_capacidad_pct"]
        fila["share_acumulado_pct"] = acumulado

    hhi = sum(f["share_capacidad_pct"] ** 2 for f in filas)
    valor_bolsa = sum(f["valor_bolsa_cop"] for f in filas)
    valor_contratos = sum(f["valor_contratos_cop"] for f in filas)
    return {
        "filas": filas,
        "total_mw": total_mw,
        "total_gwh": total_gen,
        "agentes": float(len(filas)),
        "hhi": hhi,
        "participacion_lider_pct": filas[0]["share_capacidad_pct"] if filas else 0.0,
        "participacion_top3_pct": sum(f["share_capacidad_pct"] for f in filas[:3]),
        "participacion_top5_pct": sum(f["share_capacidad_pct"] for f in filas[:5]),
        "valor_bolsa_cop": valor_bolsa,
        "valor_contratos_cop": valor_contratos,
        "precio_bolsa": precio_bolsa,
        "precio_contratos": precio_contratos,
    }


def nivel_concentracion(hhi: float) -> str:
    """Clasificación estándar del HHI sobre participaciones en porcentaje."""

    if hhi < 1500:
        return "desconcentrado"
    if hhi < 2500:
        return "moderadamente concentrado"
    return "concentrado"
