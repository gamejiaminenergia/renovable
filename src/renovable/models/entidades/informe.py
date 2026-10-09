"""Entidades inmutables que describen el informe.

El informe es una lista de bloques (uno por pagina o grupo de paginas). Cada
bloque debe estar trazado a una fuente y explicar su metodo, su conclusion, un
tip y una advertencia: esa es la regla de calidad que valida `reglas.validacion`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from renovable.models.reglas.formato import fecha_es, numero


@dataclass(frozen=True)
class Fuente:
    """Origen verificable de un dato o una afirmacion."""

    id: str
    titulo: str
    url: str
    tipo: str = "oficial"
    fecha_consulta: str | None = None

    @property
    def enlace(self) -> str:
        return self.url or "(sin enlace)"


@dataclass(frozen=True)
class Kpi:
    """Indicador con su trazabilidad completa."""

    id: str
    etiqueta: str
    valor: float
    unidad: str
    periodo: str
    fuente: str
    metodo: str = ""
    decimales: int = 1
    direccion: str = "up"
    umbral_alerta: float | None = None
    nota: str | None = None

    @property
    def texto(self) -> str:
        return numero(self.valor, self.decimales)

    @property
    def en_alerta(self) -> bool:
        if self.umbral_alerta is None:
            return False
        if self.direccion == "up":
            return self.valor < self.umbral_alerta
        return self.valor > self.umbral_alerta


@dataclass(frozen=True)
class Figura:
    """Grafica generada como imagen lista para incrustar en el PDF."""

    id: str
    titulo: str
    archivo: str
    leyenda: str = ""
    fuente: str = ""
    pagina_completa: bool = False


@dataclass(frozen=True)
class Columna:
    clave: str
    titulo: str
    alineacion: str = "right"


@dataclass(frozen=True)
class Tabla:
    """Tabla del informe; las filas son listas de valores ya formateados."""

    titulo: str
    columnas: list[Columna]
    filas: list[list[str]]
    fuente: str = ""
    metodo: str = ""
    nota: str = ""


@dataclass(frozen=True)
class Proyecto:
    """Proyecto de generacion renovable (operativo o en pipeline)."""

    nombre: str
    tecnologia: str
    capacidad_mw: float
    estado: str
    departamento: str
    fecha_operacion: str | None = None
    agente: str | None = None
    generacion_gwh: float | None = None
    fuente: str = "elecdb"

    @property
    def fecha_legible(self) -> str:
        return fecha_es(self.fecha_operacion)


@dataclass(frozen=True)
class Instrumento:
    """Norma o política vigente aplicable a una dimensión del informe."""

    norma: str
    alcance: str
    vigencia: str = "Vigente"
    evidencia: str = ""
    url: str = ""

    @property
    def es_alerta(self) -> bool:
        return self.vigencia.lower() not in {"vigente", "vigente con modificaciones"}


@dataclass
class Bloque:
    """Unidad narrativa del informe con su trazabilidad."""

    id: str
    tipo: str
    titulo: str
    resumen: str = ""
    parrafos: list[str] = field(default_factory=list)
    kpis: list[Kpi] = field(default_factory=list)
    figuras: list[Figura] = field(default_factory=list)
    tablas: list[Tabla] = field(default_factory=list)
    conclusion: str = ""
    tip: str = ""
    advertencia: str = ""
    fuentes: list[str] = field(default_factory=list)
    recomendaciones: list[str] = field(default_factory=list)
    marco_regulatorio: list[Instrumento] = field(default_factory=list)
    actualidad: str = ""
    actualidad_verificada: str = ""
    metodo: str = ""
    pagina: int = 0

    @property
    def exige_trazabilidad(self) -> bool:
        return self.tipo not in {"portada", "indice", "fuentes", "glosario"}
