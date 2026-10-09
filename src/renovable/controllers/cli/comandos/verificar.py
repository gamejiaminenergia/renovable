"""Comando `verificar`: valida el informe compuesto sin producir el PDF."""

from __future__ import annotations

from renovable.controllers.composicion import Aplicacion


def ejecutar(app: Aplicacion, refrescar: bool = False) -> int:
    contexto = app.servicio.componer(refrescar=refrescar, dibujar=False)
    errores = app.servicio.validar(contexto)
    print(f"[verificar] {len(contexto.bloques)} bloques, {len(contexto.fuentes)} fuentes")
    for bloque in contexto.bloques:
        print(f"[verificar] {bloque.pagina:>3} {bloque.id:24} {bloque.titulo}")
    if errores:
        for error in errores:
            print(f"[verificar] ERROR {error}")
        return 1
    print("[verificar] informe válido")
    return 0
