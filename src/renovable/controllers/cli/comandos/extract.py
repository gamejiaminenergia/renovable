"""Comando `extract`: ejecuta el SQL versionado y puebla la caché."""

from __future__ import annotations

from renovable.controllers.composicion import Aplicacion


def ejecutar(app: Aplicacion, refrescar: bool = False) -> int:
    consultas = app.elecdb.disponibles()
    print(f"[extract] {len(consultas)} consultas sql")
    for consulta in consultas:
        filas = app.elecdb.serie(consulta, refrescar=refrescar)
        print(f"[extract] {consulta}: {len(filas)} filas")
    print(f"[extract] caché en {app.settings.cache}")
    return 0
