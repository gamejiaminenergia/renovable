# Energías renovables en Colombia — informe para la Cancillería

[![CI](https://github.com/gamejiaminenergia/renovable/actions/workflows/ci.yml/badge.svg)](https://github.com/gamejiaminenergia/renovable/actions/workflows/ci.yml)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](pyproject.toml)

Informe ejecutivo reproducible sobre el desarrollo de proyectos de energías
renovables en Colombia, elaborado por el Ministerio de Minas y Energía para el
Ministerio de Relaciones Exteriores. El encuadre es de **diplomacia energética**:
posicionamiento internacional, atracción de inversión y cooperación.

La elaboración está a cargo de la **Oficina de Asuntos Regulatorios y
Empresariales (OARE)** del Ministerio de Minas y Energía.

El entregable es un PDF de ~35 páginas **enteramente en español**, con resumen
ejecutivo, ficha país, glosario, KPIs, tablas, gráficas, tips, advertencias y
conclusiones. Todas las imágenes son **SVG vectorial**: pesan menos que un PNG y
se ven nítidas a cualquier zoom.

Cada una de las seis dimensiones abre con un panel de **marco regulatorio y
actualidad vigente**: las normas y políticas aplicables con su estado de
vigencia, y un párrafo con la actualidad verificada. Ninguna sección se publica
sin ese panel ni sin la fecha de verificación.

El informe incluye además un **mapa de georreferenciación**: cada proyecto solar
de más de 50 MW se ubica en el municipio donde opera y el departamento se colorea
según su capacidad solar. La ubicación se toma del registro oficial de proyectos
del Ministerio de Minas y Energía y las coordenadas del DIVIPOLA.

## Qué contiene

Seis dimensiones de análisis, todas trazadas a su fuente:

1. **Regulatoria** — marco y actualidad normativa (asistente CREG + UPME).
2. **Energética y técnica** — capacidad, generación, perfil horario y emisiones.
3. **Proyectos** — catálogo del SIN y frontera eólica.
4. **Empresarial** — quién participa en el negocio solar: capacidad, generación,
   concentración de mercado y posición financiera de cada agente.
5. **Financiera** — precios de bolsa y contratos, cargos y costo de capital.
6. **Socioambiental y territorial** — territorio, comunidades y ambiente.
7. **Riesgos** — red, hidrología, licenciamiento y riesgo cambiario.

Más dos páginas de orientación: la **ficha país** con los cinco mensajes para la
conversación internacional y el **glosario** con los términos que un lector no
especializado necesita para tener conciencia situacional.

## Requisitos

- Python 3.12 y `uv`.
- Acceso de lectura a la base del mercado mayorista (elecdb / XM-SIN) en
  `postgresql://postgres:postgres@localhost:5432/postgres`.
- Servidor de la skill CREG en `http://localhost:3000` para refrescar la
  evidencia regulatoria (opcional: la evidencia ya está archivada).
- Librerías del sistema de WeasyPrint (Pango/Cairo).

## Puesta en marcha

```bash
uv pip install --python .venv/bin/python -r requirements.txt

python -m renovable regulatorio        # fase 1: estado de la evidencia CREG
python -m renovable extract --refrescar # ejecuta sql/ contra elecdb
python -m renovable build              # genera el PDF
```

El PDF queda en `output/Informe_Renovables_Cancilleria.pdf`.

## Comandos

| Comando | Qué hace |
|---|---|
| `python -m renovable regulatorio` | Lista las doce consultas regulatorias y su estado |
| `python -m renovable vigencia [--dias 30]` | Verifica que la evidencia CREG sea la más reciente y falla si supera el umbral |
| `python -m renovable extract [--refrescar]` | Ejecuta el SQL y puebla `data/cache/` |
| `python -m renovable verificar` | Valida reglas editoriales sin exportar |
| `python -m renovable build [--refrescar]` | Figuras + HTML + PDF |

También están los atajos `make build`, `make verificar`, `make test` y
`make lint`.

Para regenerar la capa departamental del mapa:

```bash
python3 tools/simplificar_geojson.py
```

## Cómo se garantiza la calidad

- **Nada escrito a mano.** Cada cifra vive en un catálogo YAML como marcador
  (`{cap_solar_mw}`) que el servicio resuelve; si un marcador no tiene valor, la
  construcción falla.
- **Trazabilidad.** Toda serie cuantitativa sale de `sql/qNN_*.sql` sobre
  elecdb; la evidencia normativa se archiva en `data/regulatorio/`.
- **Vigencia regulatoria.** Cada norma citada se verifica contra el gestor
  normativo (objeto oficial y Diario Oficial) y queda en
  `data/marco_regulatorio.yaml`; el comando `vigencia` alerta si la evidencia
  supera los treinta días.
- **Regla editorial.** Cada bloque requiere fuente, método, conclusión, tip y
  advertencia, más marco regulatorio y actualidad; cada figura requiere leyenda
  y fuente.
- **Georreferenciación.** Cada proyecto se ubica en el centroide del municipio
  que reporta el registro oficial FNCER y se valida contra la capacidad que
  publica XM; los pendientes quedan declarados como tales en lugar de inventarse.
- **Pruebas.** `pytest` cubre reglas, contenido y QA del PDF; `ruff` cubre
  estilo e importaciones.

## Estructura

```
content/   manifiesto y bloques narrativos (YAML)
sql/       consultas versionadas q01-q13 sobre elecdb
data/      caché CSV+SQL, catálogos YAML y evidencia regulatoria
assets/    capa departamental de Colombia para el mapa
templates/ plantilla Jinja2 y CSS de impresión
src/       código MVC (config, models, repositories, views, controllers)
tests/     pruebas con dobles, sin base de datos ni red
docs/      PLAN.md, el plan detallado del informe
output/    PDF final
```

## Actualización

```bash
python3 tools/fetch_regulatorio.py       # refresca la evidencia CREG
python -m renovable vigencia             # comprueba que sea la más reciente
python -m renovable extract --refrescar  # refresca las series
python -m renovable build                # reconstruye el PDF
pytest -q && ruff check .
```

Cadencia sugerida: semestral, justo antes de cada presentación oficial.

## Publicar en GitHub

El repositorio ya está listo para subirse: incluye licencia, aviso de terceros,
guía de contribución, política de seguridad, código de conducta, historial de
cambios, integración continua y plantillas de issues y pull requests.

```bash
# 1. Creá el repositorio vacío en GitHub (sin README ni licencia)
gh repo create gamejiaminenergia/renovable --public \
  --description "Informe ejecutivo de energías renovables en Colombia (MinMinas - OARE)"

# 2. Conectá el remoto y publicá
git remote add origin https://github.com/gamejiaminenergia/renovable.git
git push -u origin main
```

Sugerencias para la configuración del repositorio en GitHub:

> Si el repositorio se publica con otro nombre u organización, actualizá las URLs
> del escudo de CI de la cabecera y del enlace de
> `.github/ISSUE_TEMPLATE/config.yml`.

| Opción | Valor recomendado | Por qué |
|---|---|---|
| Topics | `energias-renovables`, `colombia`, `creg`, `xm`, `informe`, `minenergia` | Facilita que otros equipos del sector lo encuentren |
| Descripción | Informe ejecutivo de energías renovables en Colombia (MinMinas — OARE) | Es lo primero que se ve |
| Sitio publicado | Publicar `output/Informe_Renovables_Cancilleria.pdf` como release | El PDF es el entregable |
| Rama protegida | `main` con CI obligatoria | Evita publicar un informe que no compila |
| Releases | Una por corte semestral, etiquetada `v1.4.0` | Permite citar la versión exacta |
| Issues | Plantillas de error y de propuesta ya incluidas | Ordena los aportes |

La integración continua corre lint, formato y pruebas, y además **construye el
PDF** y lo deja como artefacto descargable en cada push a `main`. No necesita base
de datos ni red: el repositorio versiona la caché de consultas.

## Documentación del repositorio

| Archivo | Para qué sirve |
|---|---|
| [README.md](README.md) | Qué es el proyecto y cómo se usa |
| [docs/PLAN.md](docs/PLAN.md) | Plan detallado y decisiones de diseño del informe |
| [AGENTS.md](AGENTS.md) | Reglas de arquitectura, contenido y datos |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Cómo aportar y cómo agregar contenido |
| [data/README.md](data/README.md) | Fuentes de datos, caché y variables de entorno |
| [assets/geo/README.md](assets/geo/README.md) | Procedencia de la capa cartográfica |
| [NOTICE.md](NOTICE.md) | Datos y documentos de terceros y sus titulares |
| [SECURITY.md](SECURITY.md) | Cómo reportar un problema |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Acuerdos de convivencia |
| [CHANGELOG.md](CHANGELOG.md) | Qué cambió en cada versión |
| [CITATION.cff](CITATION.cff) | Cómo citar el informe y el código |

## Límites declarados

- XM no publica capacidad efectiva neta para la flota eólica: se usa el pico
  horario observado como cota inferior.
- Las coordenadas del mapa son el centroide municipal del DIVIPOLA, no la
  ubicación exacta de cada planta; esa está en el registro de la UPME.
- El año en curso está incompleto; las comparaciones usan períodos equivalentes.
- elecdb no trae columna de departamento ni proyectos en construcción: la lectura
  territorial es cualitativa y el pipeline se consulta en el registro de la UPME.
