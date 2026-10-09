"""Comando `vigencia`: verifica que la evidencia regulatoria sea la más reciente."""

from __future__ import annotations

import json
from datetime import datetime

from renovable.controllers.composicion import Aplicacion

DIAS_VIGENCIA = 30


def ejecutar(app: Aplicacion, dias: int = DIAS_VIGENCIA) -> int:
    ruta = app.settings.regulatorio / "_meta.json"
    preguntas = app.regulatorio.preguntas()
    pendientes = app.regulatorio.faltantes()
    if pendientes:
        print(f"[vigencia] ERROR evidencias faltantes: {', '.join(pendientes)}")
        print("[vigencia] ejecuta: python3 tools/fetch_regulatorio.py")
        return 1

    if not ruta.exists():
        print("[vigencia] ERROR no hay _meta.json: no se puede probar la fecha de verificación")
        print("[vigencia] ejecuta: python3 tools/fetch_regulatorio.py --forzar")
        return 1

    meta = json.loads(ruta.read_text(encoding="utf-8"))
    ahora = datetime.now().astimezone()
    vencidas: list[str] = []
    for consulta in preguntas:
        registro = meta.get("consultas", {}).get(consulta["id"])
        if not registro:
            vencidas.append(f"{consulta['id']} (sin sello de verificación)")
            continue
        edad = (ahora - datetime.fromisoformat(registro["obtenido"])).days
        estado = "OK" if edad <= dias else "VENCIDA"
        if estado == "VENCIDA":
            vencidas.append(f"{consulta['id']} ({edad} días)")
        obtenido = registro["obtenido"][:10]
        print(f"[vigencia] {estado:8} {consulta['id']:28} {obtenido} · {edad} días")

    print(f"[vigencia] verificación global: {meta.get('verificado', '(sin sello)')}")
    print(f"[vigencia] umbral de vigencia: {dias} días")
    if vencidas:
        print(f"[vigencia] evidencia por refrescar: {', '.join(vencidas)}")
        print("[vigencia] ejecuta: python3 tools/fetch_regulatorio.py --forzar")
        return 1
    print("[vigencia] la evidencia regulatoria está vigente")
    return 0
