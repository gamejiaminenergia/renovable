"""Reglas de calidad del informe.

Cada bloque narrativo debe estar trazado a una fuente, explicar su método y
cerrar con conclusión, tip y advertencia. El build falla si falta cualquiera de
estos elementos: es la misma disciplina editorial que usan los informes
previos del despacho.
"""

from __future__ import annotations

from renovable.models.entidades import Bloque


def validar_bloque(bloque: Bloque) -> list[str]:
    """Devuelve la lista de incumplimientos de un bloque (vacía si está bien)."""

    if not bloque.exige_trazabilidad:
        return []
    errores: list[str] = []
    if not bloque.fuentes:
        errores.append(f"{bloque.id}: sin fuente")
    if not bloque.metodo:
        errores.append(f"{bloque.id}: sin método")
    if not bloque.conclusion:
        errores.append(f"{bloque.id}: sin conclusión")
    if not bloque.tip:
        errores.append(f"{bloque.id}: sin tip")
    if not bloque.advertencia:
        errores.append(f"{bloque.id}: sin advertencia")
    if not bloque.actualidad:
        errores.append(f"{bloque.id}: sin actualidad regulatoria")
    if not bloque.marco_regulatorio:
        errores.append(f"{bloque.id}: sin marco regulatorio")
    for instrumento in bloque.marco_regulatorio:
        if not instrumento.norma or not instrumento.alcance:
            errores.append(f"{bloque.id}: instrumento regulatorio incompleto")
    if not bloque.parrafos and not bloque.tablas and not bloque.kpis and not bloque.figuras:
        errores.append(f"{bloque.id}: sin contenido")
    for figura in bloque.figuras:
        if not figura.leyenda:
            errores.append(f"{bloque.id}: figura {figura.id} sin leyenda")
        if not figura.fuente:
            errores.append(f"{bloque.id}: figura {figura.id} sin fuente")
    for tabla in bloque.tablas:
        if not tabla.fuente:
            errores.append(f"{bloque.id}: tabla {tabla.titulo} sin fuente")
    return errores


def validar_informe(bloques: list[Bloque]) -> list[str]:
    """Valida todos los bloques y la coherencia global del informe."""

    errores: list[str] = []
    ids: set[str] = set()
    for bloque in bloques:
        if bloque.id in ids:
            errores.append(f"{bloque.id}: identificador duplicado")
        ids.add(bloque.id)
        errores.extend(validar_bloque(bloque))
    if not any(b.tipo == "portada" for b in bloques):
        errores.append("informe: falta portada")
    if not any(b.tipo == "conclusiones" for b in bloques):
        errores.append("informe: faltan conclusiones")
    return errores


def numerar_paginas(bloques: list[Bloque]) -> list[Bloque]:
    """Asigna un número de página consecutivo y contiguo a cada bloque."""

    for i, bloque in enumerate(bloques, start=1):
        bloque.pagina = i
    return bloques
