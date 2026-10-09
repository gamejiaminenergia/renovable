"""Catálogo de gráficas: cada figura es una función pura datos -> Figure."""

from __future__ import annotations

import json
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Any

import plotly.graph_objects as go

from renovable.views.charts import paleta

Filas = list[dict[str, Any]]

# La capa de departamentos es un activo de la vista; vive en assets/geo.
RAIZ = Path(__file__).resolve().parents[4]
GEOJSON_DEPARTAMENTOS = RAIZ / "assets" / "geo" / "colombia_departamentos.geo.json"


@lru_cache
def _geojson_departamentos() -> dict[str, Any]:
    if not GEOJSON_DEPARTAMENTOS.exists():
        return {"type": "FeatureCollection", "features": []}
    return json.loads(GEOJSON_DEPARTAMENTOS.read_text(encoding="utf-8"))


def _f(valor: Any) -> float:
    if valor in (None, "", "None"):
        return 0.0
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0


def _plantilla(titulo: str, alto: int = 380) -> dict[str, Any]:
    return {
        "template": "plotly_white",
        "height": alto,
        "margin": {"l": 60, "r": 30, "t": 60, "b": 50},
        "title": {"text": titulo, "font": {"size": 17, "color": paleta.AZUL}},
        "font": {"family": "Helvetica, Arial, sans-serif", "size": 12},
        "legend": {"orientation": "h", "y": -0.2},
        "paper_bgcolor": paleta.FONDO,
        "plot_bgcolor": paleta.FONDO,
    }


def mix_anual(filas: Filas) -> go.Figure:
    series = {
        "Hidroeléctrica": ("hidro_gwh", paleta.TEAL),
        "Térmica": ("termica_gwh", paleta.GRIS),
        "Solar": ("solar_gwh", paleta.AMBAR),
        "Eólica": ("eolica_gwh", paleta.CELESTE),
        "Biomasa": ("biomasa_gwh", paleta.VERDE),
    }
    figura = go.Figure()
    anios = [str(int(_f(f.get("anio")))) for f in filas]
    for etiqueta, (clave, color) in series.items():
        figura.add_bar(
            x=anios,
            y=[_f(f.get(clave)) for f in filas],
            name=etiqueta,
            marker_color=color,
        )
    figura.update_layout(**_plantilla("Generación del SIN por tecnología (GWh)"))
    figura.update_layout(barmode="stack")
    figura.update_yaxes(title_text="GWh", gridcolor=paleta.REJILLA, tickformat=",.0f")
    return figura


def capacidad_evolucion(filas: Filas) -> go.Figure:
    anios = [str(int(_f(f.get("anio")))) for f in filas]
    figura = go.Figure()
    figura.add_scatter(
        x=anios,
        y=[_f(f.get("solar_mw")) for f in filas],
        name="Solar FV",
        mode="lines+markers",
        line={"color": paleta.AMBAR, "width": 3},
        fill="tozeroy",
        fillcolor="rgba(242,169,0,0.15)",
    )
    figura.add_scatter(
        x=anios,
        y=[_f(f.get("eolica_mw")) for f in filas],
        name="Eólica",
        mode="lines+markers",
        line={"color": paleta.CELESTE, "width": 3},
    )
    figura.update_layout(**_plantilla("Capacidad efectiva neta renovable (MW)"))
    figura.update_yaxes(title_text="MW", gridcolor=paleta.REJILLA)
    return figura


def generacion_mensual(filas: Filas) -> go.Figure:
    meses = [str(f.get("mes", ""))[:7] for f in filas]
    figura = go.Figure()
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("solar_gwh")) for f in filas],
        name="Solar FV",
        mode="lines",
        stackgroup="uno",
        line={"color": paleta.AMBAR, "width": 1},
    )
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("eolica_gwh")) for f in filas],
        name="Eólica",
        mode="lines",
        stackgroup="uno",
        line={"color": paleta.CELESTE, "width": 1},
    )
    figura.update_layout(**_plantilla("Generación renovable mensual (GWh)"))
    figura.update_yaxes(title_text="GWh", gridcolor=paleta.REJILLA)
    return figura


def participacion_renovable(filas: Filas) -> go.Figure:
    anios, porcentajes = [], []
    for fila in filas:
        total = sum(_f(fila.get(k)) for k in fila if str(k).endswith("_gwh"))
        renovable = _f(fila.get("solar_gwh")) + _f(fila.get("eolica_gwh"))
        anios.append(str(int(_f(fila.get("anio")))))
        porcentajes.append(renovable / total * 100 if total else 0.0)
    figura = go.Figure(
        go.Bar(
            x=anios,
            y=porcentajes,
            marker_color=paleta.AMBAR,
            text=[f"{p:.1f}%" for p in porcentajes],
            textposition="outside",
        )
    )
    figura.update_layout(**_plantilla("Participación solar y eólica en la generación (%)"))
    figura.update_yaxes(title_text="%", gridcolor=paleta.REJILLA)
    return figura


def perfil_horario(filas: Filas) -> go.Figure:
    figura = go.Figure(
        go.Scatter(
            x=[int(_f(f.get("hora"))) for f in filas],
            y=[_f(f.get("solar_promedio_mw")) for f in filas],
            mode="lines+markers",
            line={"color": paleta.AMBAR, "width": 3},
            fill="tozeroy",
            fillcolor="rgba(242,169,0,0.18)",
        )
    )
    figura.update_layout(**_plantilla("Perfil horario promedio de la generación solar (MW)"))
    figura.update_xaxes(title_text="Hora del día", dtick=2)
    figura.update_yaxes(title_text="MW promedio", gridcolor=paleta.REJILLA)
    return figura


def precios(filas: Filas) -> go.Figure:
    meses = [str(f.get("mes", ""))[:7] for f in filas]
    figura = go.Figure()
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("bolsa_cop_kwh")) for f in filas],
        name="Precio de bolsa",
        mode="lines",
        line={"color": paleta.ROJO, "width": 2.5},
    )
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("contratos_cop_kwh")) for f in filas],
        name="Precio de contratos",
        mode="lines",
        line={"color": paleta.AZUL, "width": 2.5},
    )
    figura.update_layout(**_plantilla("Precio de bolsa y de contratos (COP/kWh)"))
    figura.update_yaxes(title_text="COP/kWh", gridcolor=paleta.REJILLA)
    return figura


def embalses_precios(filas: Filas) -> go.Figure:
    meses = [str(f.get("mes", ""))[:7] for f in filas]
    figura = go.Figure()
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("embalses_pct")) for f in filas],
        name="Embalses (% volumen útil)",
        mode="lines",
        line={"color": paleta.TEAL, "width": 3},
        fill="tozeroy",
        fillcolor="rgba(27,127,121,0.15)",
    )
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("bolsa_cop_kwh")) for f in filas],
        name="Precio de bolsa (COP/kWh)",
        mode="lines",
        line={"color": paleta.ROJO, "width": 2, "dash": "dot"},
        yaxis="y2",
    )
    figura.update_layout(**_plantilla("Embalses y precio de bolsa: la señal hidrológica"))
    figura.update_layout(
        yaxis={"title": "% volumen útil", "gridcolor": paleta.REJILLA},
        yaxis2={"title": "COP/kWh", "overlaying": "y", "side": "right", "showgrid": False},
    )
    return figura


def factor_emision(filas: Filas) -> go.Figure:
    figura = go.Figure(
        go.Bar(
            x=[str(int(_f(f.get("anio")))) for f in filas],
            y=[_f(f.get("factor_emision_gco2e_kwh")) for f in filas],
            marker_color=paleta.GRIS,
            text=[f"{_f(f.get('factor_emision_gco2e_kwh')):.1f}" for f in filas],
            textposition="outside",
        )
    )
    figura.update_layout(**_plantilla("Factor de emisión del SIN (gCO₂e/kWh)"))
    figura.update_yaxes(title_text="gCO₂e/kWh", gridcolor=paleta.REJILLA)
    return figura


def proyectos_por_anio(filas: Filas) -> go.Figure:
    anios = sorted({str(int(_f(f.get("anio")))) for f in filas})
    solar = {str(int(_f(f.get("anio")))): 0.0 for f in filas}
    eolica = dict(solar)
    for fila in filas:
        clave = str(int(_f(fila.get("anio"))))
        destino = eolica if str(fila.get("fuente", "")).upper() == "VIENTO" else solar
        destino[clave] = destino.get(clave, 0.0) + _f(fila.get("proyectos"))
    figura = go.Figure()
    figura.add_bar(x=anios, y=[solar[a] for a in anios], name="Solar FV", marker_color=paleta.AMBAR)
    figura.add_bar(
        x=anios, y=[eolica[a] for a in anios], name="Eólica", marker_color=paleta.CELESTE
    )
    figura.update_layout(**_plantilla("Proyectos renovables que iniciaron operación por año"))
    figura.update_layout(barmode="stack")
    figura.update_yaxes(title_text="Proyectos", gridcolor=paleta.REJILLA)
    return figura


def top_proyectos(filas: Filas) -> go.Figure:
    ordenadas = sorted(filas, key=lambda f: _f(f.get("capacidad_mw")))[-12:]
    figura = go.Figure(
        go.Bar(
            x=[_f(f.get("capacidad_mw")) for f in ordenadas],
            y=[str(f.get("proyecto", ""))[:38] for f in ordenadas],
            orientation="h",
            marker_color=paleta.AMBAR,
            text=[f"{_f(f.get('capacidad_mw')):.0f} MW" for f in ordenadas],
            textposition="outside",
        )
    )
    figura.update_layout(**_plantilla("Mayores proyectos renovables del SIN (MW)", alto=470))
    figura.update_xaxes(title_text="MW", gridcolor=paleta.REJILLA)
    maximo = max([_f(f.get("capacidad_mw")) for f in ordenadas] or [0])
    figura.update_xaxes(range=[0, maximo * 1.2 if maximo else 1])
    return figura


def rendimiento_solar(filas: Filas) -> go.Figure:
    meses = [str(f.get("mes", ""))[:7] for f in filas]
    figura = go.Figure()
    figura.add_bar(
        x=meses,
        y=[_f(f.get("irr_global_wh_m2")) for f in filas],
        name="Irradiación global (Wh/m²)",
        marker_color=paleta.AMBAR,
    )
    figura.add_scatter(
        x=meses,
        y=[_f(f.get("temp_panel_c")) for f in filas],
        name="Temperatura de panel (°C)",
        mode="lines+markers",
        line={"color": paleta.ROJO, "width": 2},
        yaxis="y2",
    )
    figura.update_layout(**_plantilla("Rendimiento de la flota solar: irradiación y temperatura"))
    figura.update_layout(
        yaxis={"title": "Wh/m²", "gridcolor": paleta.REJILLA},
        yaxis2={"title": "°C", "overlaying": "y", "side": "right", "showgrid": False},
    )
    return figura


def mapa_proyectos(filas: Filas) -> go.Figure:
    """Mapa de georreferenciación: cada proyecto en el centroide de su municipio."""

    puntos = [f for f in filas if f.get("lat") and f.get("lon")]
    if not puntos:
        raise ValueError("el mapa requiere al menos un proyecto georreferenciado")
    solares = [p for p in puntos if str(p.get("tecnologia", "")).startswith("Solar")]
    eolicos = [p for p in puntos if not str(p.get("tecnologia", "")).startswith("Solar")]

    def tamano(mw: float) -> float:
        return max(6.0, min(26.0, 5.0 + float(mw) ** 0.5 * 0.95))

    figura = go.Figure()
    geojson = _geojson_departamentos()
    if geojson["features"]:
        por_departamento: dict[str, float] = {}
        for punto in solares:
            codigo = str(punto.get("codigo_municipio") or "")[:2]
            if codigo:
                por_departamento[codigo] = por_departamento.get(codigo, 0.0) + punto["capacidad_mw"]
        figura.add_trace(
            go.Choropleth(
                geojson=geojson,
                locations=[f["properties"]["codigo"] for f in geojson["features"]],
                z=[
                    por_departamento.get(f["properties"]["codigo"], 0.0)
                    for f in geojson["features"]
                ],
                featureidkey="properties.codigo",
                colorscale=[[0, "#E4EAF0"], [1, "#F2A900"]],
                marker_line_color="#9CB3C2",
                marker_line_width=0.7,
                colorbar={
                    "title": {"text": "MW<br>solares", "font": {"size": 10}},
                    "thickness": 9,
                    "len": 0.55,
                    "x": 0.98,
                    "tickfont": {"size": 9},
                },
                hovertemplate="%{location}: %{z:.0f} MW<extra></extra>",
                name="Capacidad solar por departamento",
            )
        )
    figura.add_scattergeo(
        lon=[p["lon"] for p in solares],
        lat=[p["lat"] for p in solares],
        text=[f"{p['nombre']} · {p['capacidad_mw']:.0f} MW" for p in solares],
        name="Solar FV de 50 MW o más",
        mode="markers",
        marker={
            "size": [tamano(p["capacidad_mw"]) for p in solares],
            "color": paleta.AMBAR,
            "line": {"width": 0.8, "color": "#7A5600"},
            "opacity": 0.9,
        },
    )
    if eolicos:
        figura.add_scattergeo(
            lon=[p["lon"] for p in eolicos],
            lat=[p["lat"] for p in eolicos],
            text=[f"{p['nombre']} · {p['capacidad_mw']:.1f} MW" for p in eolicos],
            name="Eólica en operación",
            mode="markers",
            marker={
                "size": [tamano(p["capacidad_mw"]) for p in eolicos],
                "color": paleta.CELESTE,
                "symbol": "diamond",
                "line": {"width": 0.8, "color": "#14536E"},
            },
        )
    etiquetas = [p for p in solares if p["capacidad_mw"] >= 150]
    if etiquetas:
        figura.add_scattergeo(
            lon=[p["lon"] for p in etiquetas],
            lat=[p["lat"] for p in etiquetas],
            text=[str(p["municipio"]).title() for p in etiquetas],
            mode="text",
            textposition="top center",
            textfont={"size": 13, "color": paleta.AZUL},
            showlegend=False,
        )

    figura.update_layout(
        **_plantilla("Georreferenciación de los proyectos solares del SIN", alto=900)
    )
    figura.update_layout(
        width=820,
        legend={"orientation": "h", "y": -0.015, "x": 0.02, "font": {"size": 12}},
    )
    figura.update_layout(
        geo={
            "scope": "south america",
            "showcountries": False,
            "showcoastlines": False,
            "showland": True,
            "landcolor": "#EDF1F5",
            "showlakes": True,
            "lakecolor": "#DCE9F2",
            "showocean": True,
            "oceancolor": "#CFE1EF",
            "projection": {"type": "mercator"},
            "resolution": 50,
            "domain": {"x": [0.0, 0.86], "y": [0.03, 1.0]},
            "lonaxis": {"range": [-79.6, -66.4]},
            "lataxis": {"range": [-4.6, 13.4]},
        }
    )
    return figura


REGISTRO: dict[str, Callable[[Filas], go.Figure]] = {
    "fig_mix_anual": mix_anual,
    "fig_capacidad_evolucion": capacidad_evolucion,
    "fig_generacion_mensual": generacion_mensual,
    "fig_participacion_renovable": participacion_renovable,
    "fig_perfil_horario": perfil_horario,
    "fig_precios": precios,
    "fig_embalses_precios": embalses_precios,
    "fig_factor_emision": factor_emision,
    "fig_proyectos_por_anio": proyectos_por_anio,
    "fig_top_proyectos": top_proyectos,
    "fig_rendimiento_solar": rendimiento_solar,
    "fig_mapa_proyectos": mapa_proyectos,
}


def fuente_de(figura_id: str) -> str:
    return {
        "fig_mix_anual": "q03_mix_generacion_anual",
        "fig_capacidad_evolucion": "q01_capacidad_renovable_anual",
        "fig_generacion_mensual": "q02_generacion_renovable_mensual",
        "fig_participacion_renovable": "q03_mix_generacion_anual",
        "fig_perfil_horario": "q12_perfil_horario_solar",
        "fig_precios": "q07_precios_mensual",
        "fig_embalses_precios": "q07_precios_mensual",
        "fig_factor_emision": "q09_factor_emision_anual",
        "fig_proyectos_por_anio": "q05_proyectos_por_anio",
        "fig_top_proyectos": "q04_proyectos_renovables_detalle",
        "fig_rendimiento_solar": "q06_rendimiento_solar_mensual",
        "fig_mapa_proyectos": "geo_proyectos",
    }[figura_id]
