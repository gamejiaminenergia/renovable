"""Adaptador de lectura a la base de datos del mercado mayorista (elecdb).

Cada consulta vive en sql/qNN_*.sql y se guarda en caché como CSV junto con una
copia del SQL exacto que la produjo, de modo que cualquier cifra del informe se
puede reproducir sin volver a golpear la base.
"""

from __future__ import annotations

import csv
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import psycopg

Ejecutor = Callable[[str], tuple[list[str], list[tuple[Any, ...]]]]


def _ejecutor_psycopg(dsn: str) -> Ejecutor:
    def ejecutar(sql: str) -> tuple[list[str], list[tuple[Any, ...]]]:
        with psycopg.connect(dsn) as conexion, conexion.cursor() as cursor:
            cursor.execute(sql)
            columnas = [d.name for d in (cursor.description or [])]
            return columnas, cursor.fetchall()

    return ejecutar


class ElecdbRepository:
    def __init__(
        self,
        dsn: str,
        sql_dir: Path,
        cache_dir: Path,
        ejecutor: Ejecutor | None = None,
    ) -> None:
        self._sql_dir = sql_dir
        self._cache_dir = cache_dir
        self._ejecutor = ejecutor or _ejecutor_psycopg(dsn)
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def disponibles(self) -> Sequence[str]:
        return [ruta.stem for ruta in sorted(self._sql_dir.glob("q*.sql"))]

    def _ruta_sql(self, consulta: str) -> Path:
        coincidencias = sorted(self._sql_dir.glob(f"{consulta}*.sql"))
        if not coincidencias:
            raise FileNotFoundError(f"no existe la consulta {consulta} en {self._sql_dir}")
        return coincidencias[0]

    def serie(self, consulta: str, refrescar: bool = False) -> list[dict[str, Any]]:
        """Devuelve las filas de una consulta, leyendo o poblando la caché CSV."""

        ruta_sql = self._ruta_sql(consulta)
        id_consulta = ruta_sql.stem
        ruta_csv = self._cache_dir / f"{id_consulta}.csv"
        if ruta_csv.exists() and not refrescar:
            return self._leer_csv(ruta_csv)

        sql = ruta_sql.read_text(encoding="utf-8")
        columnas, filas = self._ejecutor(sql)
        registros = [dict(zip(columnas, fila, strict=False)) for fila in filas]
        self._escribir_csv(ruta_csv, columnas, registros)
        (self._cache_dir / f"{id_consulta}.sql").write_text(sql, encoding="utf-8")
        return registros

    def extraer_todo(self, refrescar: bool = False) -> dict[str, list[dict[str, Any]]]:
        return {consulta: self.serie(consulta, refrescar) for consulta in self.disponibles()}

    @staticmethod
    def _leer_csv(ruta: Path) -> list[dict[str, Any]]:
        with ruta.open(encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))

    @staticmethod
    def _escribir_csv(ruta: Path, columnas: list[str], filas: list[dict[str, Any]]) -> None:
        with ruta.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(filas)
