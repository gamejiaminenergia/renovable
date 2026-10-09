"""Comando `regulatorio`: estado de la evidencia normativa (fase 1 del informe)."""

from __future__ import annotations

from renovable.controllers.composicion import Aplicacion


def ejecutar(app: Aplicacion) -> int:
    preguntas = app.regulatorio.preguntas()
    faltantes = app.regulatorio.faltantes()
    respondidas = len(preguntas) - len(faltantes)
    print(f"[regulatorio] {len(preguntas)} preguntas, {respondidas} respondidas")
    for consulta in preguntas:
        estado = "OK" if app.regulatorio.disponible(consulta["id"]) else "PENDIENTE"
        print(f"[regulatorio] {estado:9} {consulta['id']:24} {consulta.get('eje', '')}")
    if faltantes:
        print("[regulatorio] ejecuta: python3 tools/fetch_regulatorio.py")
        return 1
    print("[regulatorio] evidencia completa en " + str(app.settings.regulatorio))
    return 0
