"""Prepara el GeoJSON departamental de Colombia usado por el mapa del informe.

Toma la capa de departamentos disponible en el escritorio, redondea las
coordenadas y elimina puntos consecutivos repetidos para que el SVG del mapa
pese poco y WeasyPrint lo renderice rápido. Guarda el resultado en
assets/geo/colombia_departamentos.geo.json.

Uso:
    python3 tools/simplificar_geojson.py [ruta_origen]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "assets" / "geo" / "colombia_departamentos.geo.json"
ORIGEN_POR_DEFECTO = Path("/home/alde/Escritorio/PUI_SIMPLE/static/geo/colombia.geo.json")
DECIMALES = 3


def _simplificar_linea(linea: list[list[float]]) -> list[list[float]]:
    salida: list[list[float]] = []
    for punto in linea:
        redondeado = [round(float(punto[0]), DECIMALES), round(float(punto[1]), DECIMALES)]
        if not salida or salida[-1] != redondeado:
            salida.append(redondeado)
    if len(salida) >= 3 and salida[0] != salida[-1]:
        salida.append(salida[0])
    return salida


def _simplificar_geometria(geometria: dict[str, Any]) -> dict[str, Any]:
    tipo = geometria["type"]
    if tipo == "Polygon":
        anillos = [_simplificar_linea(anillo) for anillo in geometria["coordinates"]]
    elif tipo == "MultiPolygon":
        anillos = [
            [_simplificar_linea(anillo) for anillo in poligono]
            for poligono in geometria["coordinates"]
        ]
    else:  # pragma: no cover - la capa de origen solo trae polígonos
        raise ValueError(f"geometría no soportada: {tipo}")
    return {"type": tipo, "coordinates": anillos}


def main() -> int:
    origen = Path(sys.argv[1]) if len(sys.argv) > 1 else ORIGEN_POR_DEFECTO
    datos = json.loads(origen.read_text(encoding="utf-8"))
    features = [
        {
            "type": "Feature",
            "properties": {
                "codigo": str(f["properties"].get("DPTO", "")).zfill(2),
                "nombre": f["properties"].get("NOMBRE_DPT", ""),
            },
            "geometry": _simplificar_geometria(f["geometry"]),
        }
        for f in datos["features"]
    ]
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False),
        encoding="utf-8",
    )
    kb = DESTINO.stat().st_size / 1024
    print(f"[geo] {len(features)} departamentos -> {DESTINO} ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
