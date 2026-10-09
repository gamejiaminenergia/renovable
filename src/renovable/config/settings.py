"""Ajustes y rutas del proyecto (fuente única de verdad).

Las rutas se derivan de la ubicación del paquete para que el proyecto funcione
desde cualquier directorio de trabajo. Las credenciales se sobreescriben por
variables de entorno con el prefijo RENOVABLE_.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RENOVABLE_", extra="ignore")

    elecdb_dsn: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    creg_api: str = "http://localhost:3000/api/ask"
    creg_timeout_s: int = 300

    raiz: Path = Path(__file__).resolve().parents[3]

    @property
    def sql(self) -> Path:
        return self.raiz / "sql"

    @property
    def cache(self) -> Path:
        return self.raiz / "data" / "cache"

    @property
    def regulatorio(self) -> Path:
        return self.raiz / "data" / "regulatorio"

    @property
    def datos(self) -> Path:
        return self.raiz / "data"

    @property
    def contenido(self) -> Path:
        return self.raiz / "content"

    @property
    def plantillas(self) -> Path:
        return self.raiz / "templates"

    @property
    def build(self) -> Path:
        return self.raiz / "build"

    @property
    def output(self) -> Path:
        return self.raiz / "output"


@lru_cache
def get_settings() -> Settings:
    return Settings()
