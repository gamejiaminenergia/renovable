"""Repositorios: adaptadores a elecdb, la evidencia CREG, la web y los catálogos."""

from renovable.repositories.catalogos import CatalogoYaml
from renovable.repositories.elecdb import ElecdbRepository
from renovable.repositories.regulatorio import RegulatorioRepository
from renovable.repositories.web import WebRepository

__all__ = ["CatalogoYaml", "ElecdbRepository", "RegulatorioRepository", "WebRepository"]
