"""Comando `build`: compone el informe, dibuja las gráficas y exporta el PDF."""

from __future__ import annotations

from renovable.controllers.composicion import Aplicacion

NOMBRE_PDF = "Informe_Renovables_Cancilleria.pdf"


def ejecutar(app: Aplicacion, refrescar: bool = False) -> int:
    contexto = app.servicio.componer(refrescar=refrescar, dibujar=True)
    errores = app.servicio.validar(contexto)
    if errores:
        for error in errores:
            print(f"[build] ERROR {error}")
        return 1
    html = app.html.renderizar(
        contexto.bloques,
        {
            "meta": contexto.meta,
            "fuentes": contexto.fuentes,
            "indice": contexto.indice,
            "corte": contexto.corte,
        },
    )
    destino = app.settings.output / NOMBRE_PDF
    ruta = app.pdf.exportar(html, destino)
    print(f"[build] {len(contexto.bloques)} bloques -> {ruta}")
    return 0
