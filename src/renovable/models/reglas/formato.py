"""Regla de formato numérico del informe (convención colombiana).

Vive en el modelo porque es una regla de presentación del dominio: cualquier
vista (HTML, PDF, consola) debe mostrar las cifras igual.
"""

from __future__ import annotations

MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def numero(valor: float, decimales: int = 1) -> str:
    """Formatea con punto de miles y coma decimal: 12345.6 -> '12.345,6'."""

    texto = f"{float(valor):,.{decimales}f}"
    return texto.replace(",", "\u0000").replace(".", ",").replace("\u0000", ".")


def porcentaje(valor: float, decimales: int = 1) -> str:
    return f"{numero(valor, decimales)} %"


def millones(valor: float, decimales: int = 0) -> str:
    return numero(valor / 1e6, decimales)


def fecha_es(texto: str | None) -> str:
    if not texto:
        return "—"
    partes = str(texto)[:10].split("-")
    if len(partes) != 3:
        return str(texto)
    try:
        anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return str(texto)
    return f"{dia} de {MESES[mes - 1]} de {anio}"
