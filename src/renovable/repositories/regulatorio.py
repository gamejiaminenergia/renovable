"""Adaptador de la evidencia regulatoria recogida del asistente CREG."""

from __future__ import annotations

from pathlib import Path


class RegulatorioRepository:
    def __init__(self, dir_respuestas: Path, ruta_preguntas: Path) -> None:
        self._dir = dir_respuestas
        self._preguntas = ruta_preguntas

    def preguntas(self) -> list[dict[str, str]]:
        return _leer_preguntas(self._preguntas)

    def respuestas(self) -> dict[str, str]:
        """Devuelve el texto completo de cada respuesta, indexado por id."""

        respuestas: dict[str, str] = {}
        for ruta in sorted(self._dir.glob("R*.md")):
            respuestas[ruta.stem] = ruta.read_text(encoding="utf-8")
        return respuestas

    def faltantes(self) -> list[str]:
        return [p["id"] for p in self.preguntas() if not self.disponible(p["id"])]

    def disponible(self, id_consulta: str) -> bool:
        return (self._dir / f"{id_consulta}.md").exists()

    def extracto(self, id_consulta: str, limite: int = 1200) -> str:
        """Devuelve el cuerpo de la respuesta sin encabezados, recortado."""

        texto = (self._dir / f"{id_consulta}.md").read_text(encoding="utf-8")
        cuerpo: list[str] = []
        capturando = False
        for linea in texto.splitlines():
            if linea.startswith("## Respuesta CREG"):
                capturando = True
                continue
            if capturando and linea.startswith("## "):
                break
            if capturando:
                cuerpo.append(linea)
        limpio = "\n".join(cuerpo).strip()
        return limpio[:limite].rstrip() + ("…" if len(limpio) > limite else "")


def _leer_preguntas(ruta: Path) -> list[dict[str, str]]:
    consultas: list[dict[str, str]] = []
    actual: dict[str, str] = {}
    clave: str | None = None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
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
