"""Adaptador de los catálogos YAML que definen el contenido del informe."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from renovable.models.entidades import Fuente


class CatalogoYaml:
    def __init__(self, dir_contenido: Path, dir_datos: Path) -> None:
        self._contenido = dir_contenido
        self._datos = dir_datos

    def _leer(self, ruta: Path) -> dict[str, Any]:
        return yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}

    def manifiesto(self) -> dict[str, Any]:
        return self._leer(self._contenido / "informe.yaml")

    def bloques(self) -> list[dict[str, Any]]:
        bloques: list[dict[str, Any]] = []
        for referencia in self.manifiesto().get("bloques", []):
            ruta = self._contenido / "bloques" / f"{referencia}.yaml"
            if not ruta.exists():
                raise FileNotFoundError(f"falta el bloque {referencia} en {ruta}")
            bloques.append(self._leer(ruta))
        return bloques

    def kpis(self) -> dict[str, dict[str, Any]]:
        return self._leer(self._datos / "catalogo_kpis.yaml").get("kpis", {})

    def fuentes(self) -> list[Fuente]:
        crudas = self._leer(self._datos / "catalogo_fuentes.yaml").get("fuentes", [])
        return [Fuente(**cruda) for cruda in crudas]

    def pipeline(self) -> list[dict[str, Any]]:
        return self._leer(self._datos / "pipeline_proyectos.yaml").get("proyectos", [])

    def graficas(self) -> dict[str, dict[str, Any]]:
        return self._leer(self._datos / "catalogo_graficas.yaml").get("graficas", {})
