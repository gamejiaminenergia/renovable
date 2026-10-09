"""Recolector de evidencia regulatoria desde el asistente CREG.

Ejecuta cada pregunta de data/preguntas_creg.yaml contra el servidor HTTP de la
skill creg-ai-client (localhost:3000) y archiva la respuesta y los enlaces en
data/regulatorio/<id>.md. Es idempotente: si el archivo ya existe y no se pide
--forzar, no vuelve a consultar.

Uso:
    python3 tools/fetch_regulatorio.py [--forzar] [--solo R01_marco_general]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PREGUNTAS = RAIZ / "data" / "preguntas_creg.yaml"
SALIDA = RAIZ / "data" / "regulatorio"
API = "http://localhost:3000/api/ask"


def _leer_preguntas() -> list[dict[str, str]]:
    """Lee el YAML de preguntas sin depender de pyyaml (formato controlado)."""
    consultas: list[dict[str, str]] = []
    actual: dict[str, str] = {}
    clave: str | None = None
    for linea in PREGUNTAS.read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.strip().startswith("#"):
            continue
        if linea.lstrip().startswith("- id:"):
            if actual:
                consultas.append(actual)
            actual = {"id": linea.split(":", 1)[1].strip()}
            clave = None
        elif ":" in linea:
            k, v = linea.strip().split(":", 1)
            if k in {"eje", "pregunta"}:
                valor = v.strip()
                actual[k] = "" if valor in {">-", ">", "|", "|-"} else valor
                clave = k
        elif clave:
            actual[clave] = (actual.get(clave, "") + " " + linea.strip()).strip()
    if actual:
        consultas.append(actual)
    return consultas


def _preguntar(pregunta: str, timeout_s: int = 300) -> dict:
    cuerpo = json.dumps({"question": pregunta, "timeout": timeout_s * 1000}).encode()
    req = urllib.request.Request(API, data=cuerpo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout_s + 30) as resp:
        return json.loads(resp.read().decode())


def _render(consulta: dict[str, str], datos: dict) -> str:
    lineas = [
        f"# {consulta['id']} — {consulta.get('eje', '')}",
        "",
        "## Pregunta",
        "",
        consulta["pregunta"],
        "",
        f"## Respuesta CREG: {datos.get('title', '(sin título)')}",
        "",
        datos.get("content", "(sin contenido)").strip(),
        "",
    ]
    enlaces = datos.get("links") or []
    if enlaces:
        lineas += ["## Enlaces", ""]
        lineas += [f"- [{e.get('text', 'enlace')}]({e.get('href', '')})" for e in enlaces]
        lineas.append("")
    listas = datos.get("lists") or []
    for i, lista in enumerate(listas, start=1):
        lineas += [f"## Lista {i}", ""]
        lineas += [f"- {item}" for item in lista]
        lineas.append("")
    return "\n".join(lineas)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--forzar", action="store_true")
    parser.add_argument("--solo", default=None)
    parser.add_argument("--ids", default=None, help="lista separada por comas")
    args = parser.parse_args()

    SALIDA.mkdir(parents=True, exist_ok=True)
    consultas = _leer_preguntas()
    ruta_meta = SALIDA / "_meta.json"
    meta = json.loads(ruta_meta.read_text(encoding="utf-8")) if ruta_meta.exists() else {}
    meta.setdefault("consultas", {})
    deseados = None
    if args.ids:
        deseados = {x.strip() for x in args.ids.split(",") if x.strip()}
    pendientes = [
        c
        for c in consultas
        if (not args.solo or c["id"] == args.solo) and (deseados is None or c["id"] in deseados)
    ]
    print(f"[creg] {len(pendientes)} consultas a procesar")

    fallos = 0
    for consulta in pendientes:
        destino = SALIDA / f"{consulta['id']}.md"
        if destino.exists() and not args.forzar:
            print(f"[creg] {consulta['id']}: ya existe, se omite")
            continue
        print(f"[creg] {consulta['id']}: consultando...", flush=True)
        inicio = time.time()
        try:
            respuesta = _preguntar(consulta["pregunta"])
            if not respuesta.get("success"):
                raise RuntimeError(respuesta.get("error", "error desconocido"))
            destino.write_text(_render(consulta, respuesta["data"]), encoding="utf-8")
            sello = datetime.now().astimezone().isoformat(timespec="minutes")
            meta["consultas"][consulta["id"]] = {
                "eje": consulta.get("eje", ""),
                "obtenido": sello,
                "pregunta": consulta["pregunta"],
                "titulo": respuesta["data"].get("title", ""),
                "enlaces": [e.get("href", "") for e in (respuesta["data"].get("links") or [])],
            }
            meta["verificado"] = sello
            ruta_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[creg] {consulta['id']}: OK en {time.time() - inicio:.0f}s")
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            fallos += 1
            print(f"[creg] {consulta['id']}: FALLO ({exc})", flush=True)

    # Sella toda la evidencia existente con la fecha real de su archivo, de modo
    # que el comando `renovable vigencia` pueda probar qué tan reciente es.
    for consulta in consultas:
        destino = SALIDA / f"{consulta['id']}.md"
        if not destino.exists():
            continue
        mtime = datetime.fromtimestamp(destino.stat().st_mtime).astimezone()
        registro = meta["consultas"].setdefault(consulta["id"], {})
        registro["eje"] = consulta.get("eje", "")
        registro["pregunta"] = consulta["pregunta"]
        registro.setdefault("titulo", "")
        registro.setdefault("enlaces", [])
        if args.forzar or "obtenido" not in registro:
            registro["obtenido"] = mtime.isoformat(timespec="minutes")
            meta["verificado"] = mtime.isoformat(timespec="minutes")
    ruta_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[creg] terminado, fallos={fallos}")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
