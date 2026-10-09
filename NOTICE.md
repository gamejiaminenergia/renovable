# Aviso sobre datos y documentos de terceros

La licencia MIT de este repositorio aplica al **código fuente, las plantillas,
los catálogos de contenido, las gráficas generadas y el informe** que produce el
proyecto.

**No aplica** a los siguientes contenidos, que se incluyen únicamente como
evidencia o insumo y conservan los derechos de sus respectivas entidades:

| Contenido | Ubicación | Titular |
|---|---|---|
| Datos del Mercado de Energía Mayorista (generación, precios, embalses, agentes) | `data/cache/q*.csv` (derivados) | XM S.A. E.S.P., administrador del Sistema Interconectado Nacional y del MEM |
| Respuestas del asistente regulatorio de la CREG | `data/regulatorio/R*.md` | Comisión de Regulación de Energía y Gas (CREG) |
| Textos y referencias normativas | `data/marco_regulatorio.yaml` | CREG, Ministerio de Minas y Energía, UPME, MADS y Congreso de la República |
| Registro oficial de proyectos de generación FNCER ("Meta FNCER", dataset `vy9n-w6hc`) | `data/fuentes/meta_fncer.json` | Ministerio de Minas y Energía, publicado en datos.gov.co |
| División política y centroides municipales (DIVIPOLA, dataset `gdxc-w37w`) | `data/cache/q13_geo_municipios.csv` (derivado) | Departamento Administrativo Nacional de Estadística (DANE), publicado en datos.gov.co |
|Capas de límites departamentales de Colombia | `assets/geo/colombia_departamentos.geo.json` | Elaboración derivada de cartografía pública de uso referencial; ver `assets/geo/README.md` |
| Artículos de referencia usados para contrastar ubicaciones | `data/geografia_proyectos.yaml` | Wikipedia, con licencia CC BY-SA |
| Series internacionales de costos y capacidad | citadas en el informe | IRENA |

Los archivos de `data/cache/` son **agregaciones y cálculos propios** sobre
información pública del mercado; los datos primarios no se redistribuyen. Las
respuestas de la CREG se archivan como evidencia de la consulta y se citan con su
fecha de obtención.

Al reutilizar este repositorio, cite las fuentes oficiales indicadas en el
informe y respete las condiciones de uso de cada entidad.
