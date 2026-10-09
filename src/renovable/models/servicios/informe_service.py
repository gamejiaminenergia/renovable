"""Servicio que compone el informe: datos -> KPI -> bloques trazables.

Es el único lugar donde se combinan las series de elecdb, la evidencia CREG y
los catálogos de contenido. El controlador solo orquesta.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from renovable.models.entidades import Bloque, Columna, Figura, Instrumento, Kpi, Tabla
from renovable.models.puertos import Catalogo, FuenteDatos, FuenteRegulatoria
from renovable.models.reglas.agentes import analizar_agentes_solar, nivel_concentracion
from renovable.models.reglas.formato import MESES, fecha_es, numero
from renovable.models.reglas.kpis import calcular_kpis
from renovable.models.reglas.validacion import numerar_paginas, validar_informe

Dibujante = Callable[[str, dict], str]


@dataclass
class Contexto:
    """Todo lo que necesitan las vistas para renderizar el informe."""

    meta: dict[str, Any] = field(default_factory=dict)
    bloques: list[Bloque] = field(default_factory=list)
    datos: dict[str, list[dict]] = field(default_factory=dict)
    valores: dict[str, float] = field(default_factory=dict)
    texto: dict[str, str] = field(default_factory=dict)
    fuentes: list[dict[str, str]] = field(default_factory=list)
    indice: list[dict[str, Any]] = field(default_factory=list)
    corte: str = ""
    errores: list[str] = field(default_factory=list)


class ServicioInforme:
    def __init__(
        self,
        catalogo: Catalogo,
        datos: FuenteDatos,
        regulatorio: FuenteRegulatoria,
        dibujante: Dibujante | None = None,
    ) -> None:
        self._catalogo = catalogo
        self._datos = datos
        self._regulatorio = regulatorio
        self._dibujante = dibujante

    # ------------------------------------------------------------------ público
    def componer(self, refrescar: bool = False, dibujar: bool = True) -> Contexto:
        series = (
            self._datos.extraer_todo(refrescar=refrescar)
            if hasattr(self._datos, "extraer_todo")
            else {c: self._datos.serie(c, refrescar) for c in self._datos.disponibles()}
        )
        valores = calcular_kpis(series)
        valores["eolica_parques"] = float(len(self._catalogo.pipeline()))
        series["geo_proyectos"] = self._georreferenciar(series)
        valores.update(self._kpis_geo(series["geo_proyectos"]))
        resumen_agentes = self._analizar_agentes(series, valores)
        series["agentes_solar"] = resumen_agentes["filas"]
        valores.update(self._kpis_agentes(resumen_agentes))
        catalogo_kpis = self._catalogo.kpis()
        self._verificado = self._catalogo.verificacion()
        texto = self._valores_como_texto(valores, catalogo_kpis)

        meta = self._catalogo.manifiesto().get("meta", {})
        meta = {**meta, **self._meta_dinamica(valores)}
        texto["anio_anterior"] = str(int(meta["anio_anterior"]))
        texto["anio_corte"] = str(int(meta["anio_corte"]))
        texto["verificado"] = self._fecha_verificacion()
        texto["nivel_hhi"] = nivel_concentracion(valores.get("hhi_solar", 0.0))
        contexto = Contexto(
            meta=meta,
            datos=series,
            valores=valores,
            texto=texto,
            fuentes=[self._fuente_a_dict(f) for f in self._catalogo.fuentes()],
            corte=self._corte(series),
        )

        bloques: list[Bloque] = []
        for crudo in self._catalogo.bloques():
            bloques.append(self._bloque(crudo, contexto, catalogo_kpis, dibujar))
        numerar_paginas(bloques)

        contexto.bloques = bloques
        contexto.indice = [
            {"id": b.id, "titulo": b.titulo, "pagina": b.pagina, "tipo": b.tipo}
            for b in bloques
            if b.tipo not in {"portada"}
        ]
        contexto.errores = validar_informe(bloques)
        return contexto

    def validar(self, contexto: Contexto) -> list[str]:
        errores = list(contexto.errores)
        faltantes = self._regulatorio.faltantes()
        if faltantes:
            errores.append(f"evidencia regulatoria incompleta: {', '.join(faltantes)}")
        return errores

    # ----------------------------------------------------------------- privado
    def _valores_como_texto(
        self, valores: dict[str, float], catalogo_kpis: dict[str, dict]
    ) -> dict[str, str]:
        texto: dict[str, str] = {}
        for clave, valor in valores.items():
            if clave.startswith("anio"):
                texto[clave] = str(int(valor))
                continue
            decimales = int(catalogo_kpis.get(clave, {}).get("decimales", 1))
            texto[clave] = numero(valor, decimales)
        return texto

    def _meta_dinamica(self, valores: dict[str, float]) -> dict[str, Any]:
        anio = int(valores.get("anio", 0))
        return {
            "anio_corte": anio,
            "anio_anterior": anio - 1,
        }

    def _georreferenciar(self, series: dict[str, list[dict]]) -> list[dict[str, Any]]:
        """Une el catálogo de proyectos con los centroides municipales DIVIPOLA."""

        municipios = {str(fila["cod_mpio"]): fila for fila in series.get("q13_geo_municipios", [])}
        catalogo = self._catalogo.geografia()
        puntos: list[dict[str, Any]] = []
        for entrada in [*catalogo.get("proyectos", []), *catalogo.get("eolicos", [])]:
            codigo = entrada.get("codigo_municipio")
            geo = municipios.get(str(codigo)) if codigo else None
            puntos.append(
                {
                    **entrada,
                    "lat": float(geo["latitud"]) if geo else None,
                    "lon": float(geo["longitud"]) if geo else None,
                    "localizado": geo is not None,
                    "municipio_divipola": geo["municipio"] if geo else None,
                    "capacidad_mw": float(entrada.get("capacidad_mw") or 0.0),
                }
            )
        return puntos

    @staticmethod
    def _kpis_geo(puntos: list[dict[str, Any]]) -> dict[str, float]:
        solares = [p for p in puntos if str(p.get("tecnologia", "")).startswith("Solar")]
        localizados = [p for p in solares if p["localizado"]]
        total_mw = sum(p["capacidad_mw"] for p in solares)
        mw_localizado = sum(p["capacidad_mw"] for p in localizados)
        return {
            "proyectos_georreferenciados": float(len(localizados)),
            "proyectos_sin_georreferenciar": float(len(solares) - len(localizados)),
            "cap_georreferenciada_pct": (mw_localizado / total_mw * 100) if total_mw else 0.0,
        }

    def _analizar_agentes(
        self, series: dict[str, list[dict]], valores: dict[str, float]
    ) -> dict[str, Any]:
        return analizar_agentes_solar(
            series.get("q14_agentes_solar_energetico", []),
            series.get("q15_agentes_solar_financiero", []),
            valores.get("precio_bolsa_cop_kwh", 0.0),
            valores.get("precio_contratos_cop_kwh", 0.0),
        )

    @staticmethod
    def _kpis_agentes(resumen: dict[str, Any]) -> dict[str, float]:
        millones = 1e9  # COP -> miles de millones
        return {
            "agentes_solar": float(resumen.get("agentes", 0.0)),
            "hhi_solar": float(resumen.get("hhi", 0.0)),
            "participacion_lider_pct": float(resumen.get("participacion_lider_pct", 0.0)),
            "participacion_top5_pct": float(resumen.get("participacion_top5_pct", 0.0)),
            "valor_solar_bolsa_mmm": float(resumen.get("valor_bolsa_cop", 0.0)) / millones,
            "valor_solar_contratos_mmm": float(resumen.get("valor_contratos_cop", 0.0)) / millones,
        }

    def _corte(self, series: dict[str, list[dict]]) -> str:
        fechas = [
            str(fila.get("mes", ""))[:10]
            for fila in series.get("q02_generacion_renovable_mensual", [])
        ]
        mes = max(fechas) if fechas else ""
        if not mes:
            return "último dato disponible"
        anio, numero_mes = mes.split("-")[:2]
        return f"{MESES[int(numero_mes) - 1]} de {anio}"

    @staticmethod
    def _fuente_a_dict(fuente) -> dict[str, str]:
        return {
            "id": fuente.id,
            "titulo": fuente.titulo,
            "url": fuente.url,
            "tipo": fuente.tipo,
            "fecha_consulta": fuente.fecha_consulta or "",
        }

    def _bloque(
        self,
        crudo: dict[str, Any],
        contexto: Contexto,
        catalogo_kpis: dict[str, dict],
        dibujar: bool,
    ) -> Bloque:
        formatear = lambda t: self._resolver_texto(t, contexto.texto)  # noqa: E731
        bloque = Bloque(
            id=crudo["id"],
            tipo=crudo.get("tipo", "seccion"),
            titulo=formatear(crudo.get("titulo", crudo["id"])),
            resumen=formatear(crudo.get("resumen", "")),
            parrafos=[formatear(p) for p in crudo.get("parrafos", [])],
            recomendaciones=[formatear(r) for r in crudo.get("recomendaciones", [])],
            conclusion=formatear(crudo.get("conclusion", "")),
            tip=formatear(crudo.get("tip", "")),
            advertencia=formatear(crudo.get("advertencia", "")),
            metodo=formatear(crudo.get("metodo", "")),
            fuentes=list(crudo.get("fuentes", [])),
            kpis=self._kpis_de(crudo.get("kpis", []), contexto, catalogo_kpis),
            tablas=self._tablas_de(crudo.get("tablas", []), contexto),
            actualidad=formatear(crudo.get("actualidad", "")),
            actualidad_verificada=self._fecha_verificacion(),
            marco_regulatorio=self._instrumentos_de(crudo.get("marco_regulatorio", [])),
        )
        if dibujar and self._dibujante:
            bloque.figuras = self._figuras_de(crudo.get("figuras", []), contexto)
        return bloque

    @staticmethod
    def _resolver_texto(texto: str, valores: dict[str, str]) -> str:
        if not texto:
            return ""
        try:
            return texto.format(**valores)
        except KeyError as exc:  # pragma: no cover - se cubre con los tests de contenido
            raise KeyError(f"marcador sin valor en el catálogo: {exc}") from exc

    def _kpis_de(
        self, ids: list[str], contexto: Contexto, catalogo_kpis: dict[str, dict]
    ) -> list[Kpi]:
        resultado: list[Kpi] = []
        for id_kpi in ids:
            if id_kpi not in catalogo_kpis:
                raise KeyError(f"KPI {id_kpi} no está en catalogo_kpis.yaml")
            if id_kpi not in contexto.valores:
                raise KeyError(f"KPI {id_kpi} no tiene valor calculado")
            definicion = catalogo_kpis[id_kpi]
            resultado.append(
                Kpi(
                    id=id_kpi,
                    etiqueta=self._resolver_texto(definicion["etiqueta"], contexto.texto),
                    valor=contexto.valores[id_kpi],
                    unidad=definicion.get("unidad", ""),
                    periodo=self._resolver_texto(
                        definicion.get("periodo", str(int(contexto.valores["anio"]))),
                        contexto.texto,
                    ),
                    fuente=definicion.get("fuente", ""),
                    metodo=definicion.get("metodo", ""),
                    decimales=int(definicion.get("decimales", 1)),
                    direccion=definicion.get("direccion", "up"),
                    umbral_alerta=definicion.get("umbral_alerta"),
                    nota=definicion.get("nota"),
                )
            )
        return resultado

    def _figuras_de(self, ids: list[str], contexto: Contexto) -> list[Figura]:
        catalogo_graficas = self._catalogo.graficas()
        figuras: list[Figura] = []
        for id_figura in ids:
            definicion = catalogo_graficas.get(id_figura, {})
            archivo = self._dibujante(id_figura, contexto.datos) if self._dibujante else ""
            figuras.append(
                Figura(
                    id=id_figura,
                    titulo=definicion.get("titulo", id_figura),
                    archivo=archivo,
                    leyenda=definicion.get("leyenda", ""),
                    fuente=definicion.get("fuente", ""),
                    pagina_completa=bool(definicion.get("pagina_completa", False)),
                )
            )
        return figuras

    def _instrumentos_de(self, referencias: list[Any]) -> list[Instrumento]:
        """Resuelve los instrumentos: acepta ids del registro o definiciones en línea."""

        registro = self._catalogo.instrumentos()
        instrumentos: list[Instrumento] = []
        for referencia in referencias:
            crudo = registro.get(referencia, {}) if isinstance(referencia, str) else referencia
            if not crudo:
                raise KeyError(f"instrumento regulatorio desconocido: {referencia}")
            instrumentos.append(
                Instrumento(
                    norma=str(crudo.get("norma", "")),
                    alcance=str(crudo.get("alcance", "")),
                    vigencia=str(crudo.get("vigencia", "Vigente")),
                    evidencia=str(crudo.get("evidencia", "")),
                    url=str(crudo.get("url", "")),
                )
            )
        return instrumentos

    def _fecha_verificacion(self) -> str:
        """Fecha de la evidencia regulatoria más reciente usada en el informe."""

        sello = getattr(self, "_verificado", "") or self._catalogo.verificacion()
        return fecha_es(sello[:10]) if sello else "fecha de corte"

    def _tablas_de(self, crudos: list[dict[str, Any]], contexto: Contexto) -> list[Tabla]:
        tablas: list[Tabla] = []
        for crudo in crudos:
            columnas = [
                Columna(
                    clave=c["clave"],
                    titulo=c["titulo"],
                    alineacion=c.get("alineacion", "right"),
                )
                for c in crudo.get("columnas", [])
            ]
            filas_crudas = self._filas(crudo, contexto)
            filas = [
                [self._celda(fila.get(c.clave), c, crudo) for c in columnas]
                for fila in filas_crudas
            ]
            tablas.append(
                Tabla(
                    titulo=self._resolver_texto(crudo.get("titulo", ""), contexto.texto),
                    columnas=columnas,
                    filas=filas,
                    fuente=crudo.get("fuente", ""),
                    metodo=crudo.get("metodo", ""),
                    nota=self._resolver_texto(crudo.get("nota", ""), contexto.texto),
                )
            )
        return tablas

    def _filas(self, crudo: dict[str, Any], contexto: Contexto) -> list[dict[str, Any]]:
        if crudo.get("origen") == "pipeline":
            filas = list(self._catalogo.pipeline())
        elif crudo.get("origen") == "geografia":
            filas = list(contexto.datos.get("geo_proyectos", []))
        elif crudo.get("origen") == "agentes":
            filas = list(contexto.datos.get("agentes_solar", []))
        elif crudo.get("origen") == "fijo":
            filas = list(crudo.get("filas", []))
        else:
            filas = list(contexto.datos.get(crudo.get("consulta", ""), []))
        orden = crudo.get("orden")
        if orden:
            inverso = bool(crudo.get("descendente", True))
            filas = sorted(filas, key=lambda f: _float(f.get(orden)), reverse=inverso)
        limite = crudo.get("limite")
        return filas[: int(limite)] if limite else filas

    @staticmethod
    def _celda(valor: Any, columna: Columna, crudo: dict[str, Any]) -> str:
        if valor in (None, "", "None"):
            return "—"
        formato = crudo.get("formatos", {}).get(columna.clave, "texto")
        if formato == "entero":
            return numero(_float(valor), 0)
        if formato == "decimal":
            return numero(_float(valor), 1)
        if formato == "mmm":
            return numero(_float(valor) / 1e9, 1)
        if formato == "fecha":
            return fecha_es(str(valor))
        return str(valor)


def _float(valor: Any) -> float:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0
