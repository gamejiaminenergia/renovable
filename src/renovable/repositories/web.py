"""Adaptador de fuentes web con caché en disco.

Se usa para dejar constancia de la investigación de internet (UPME, MME, XM,
IRENA y demás). El contenido descargado queda cacheado para que la construcción
del informe sea reproducible sin red.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import requests

AGENTE = "Mozilla/5.0 (compatible; MinMinasInforme/0.1)"


class WebRepository:
    def __init__(self, cache_dir: Path, timeout_s: int = 20) -> None:
        self._cache_dir = cache_dir / "web"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._timeout_s = timeout_s

    def _ruta(self, url: str) -> Path:
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
        return self._cache_dir / f"{digest}.html"

    def obtener(self, url: str, refrescar: bool = False) -> str:
        destino = self._ruta(url)
        if destino.exists() and not refrescar:
            return destino.read_text(encoding="utf-8", errors="replace")
        try:
            respuesta = requests.get(url, timeout=self._timeout_s, headers={"User-Agent": AGENTE})
            respuesta.raise_for_status()
            html = respuesta.text
        except requests.RequestException as exc:  # pragma: no cover - depende de red
            destino.write_text(f"<!-- fallo al descargar {url}: {exc} -->", encoding="utf-8")
            return ""
        destino.write_text(html, encoding="utf-8")
        (self._cache_dir / f"{destino.stem}.url").write_text(url, encoding="utf-8")
        return html
