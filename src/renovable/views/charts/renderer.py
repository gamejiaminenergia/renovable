"""Renderizador de gráficas a PNG usando Plotly + Kaleido (única frontera)."""

from __future__ import annotations

from pathlib import Path

from renovable.views.charts import figuras


class RenderizadorPlotly:
    def __init__(self, dir_salida: Path) -> None:
        self._dir = dir_salida
        self._dir.mkdir(parents=True, exist_ok=True)

    def dibujar(self, figura_id: str, datos: dict) -> str:
        constructor = figuras.REGISTRO.get(figura_id)
        if constructor is None:
            raise KeyError(f"figura desconocida: {figura_id}")
        filas = datos.get(figuras.fuente_de(figura_id), [])
        figura = constructor(filas)
        destino = self._dir / f"{figura_id}.png"
        figura.write_image(str(destino), width=900, height=figura.layout.height or 380, scale=2)
        return str(destino)
