# Energías renovables en Colombia — informe para la Cancillería

Informe ejecutivo reproducible sobre el desarrollo de proyectos de energías
renovables en Colombia, elaborado por el Ministerio de Minas y Energía para el
Ministerio de Relaciones Exteriores. El encuadre es de **diplomacia energética**:
posicionamiento internacional, atracción de inversión y cooperación.

El entregable es un PDF de 20-30 páginas en español con resumen ejecutivo
también en inglés, KPIs, tablas, gráficas, tips, advertencias y conclusiones.

Cada una de las seis dimensiones abre con un panel de **marco regulatorio y
actualidad vigente**: las normas y políticas aplicables con su estado de
vigencia, y un párrafo con la actualidad verificada. Ninguna sección se publica
sin ese panel ni sin la fecha de verificación.

## Qué contiene

Seis dimensiones de análisis, todas trazadas a su fuente:

1. **Regulatoria** — marco y actualidad normativa (asistente CREG + UPME).
2. **Energética y técnica** — capacidad, generación, perfil horario y emisiones.
3. **Proyectos** — catálogo del SIN y frontera eólica.
4. **Financiera** — precios de bolsa y contratos, cargos y costo de capital.
5. **Socioambiental y territorial** — territorio, comunidades y ambiente.
6. **Riesgos** — red, hidrología, licenciamiento y riesgo cambiario.

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
- **Pruebas.** `pytest` cubre reglas, contenido y QA del PDF; `ruff` cubre
  estilo e importaciones.

## Estructura

```
content/   manifiesto y bloques narrativos (YAML)
sql/       consultas versionadas q01-q12 sobre elecdb
data/      caché CSV+SQL, catálogos YAML y evidencia regulatoria
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

## Límites declarados

- XM no publica capacidad efectiva neta para la flota eólica: se usa el pico
  horario observado como cota inferior.
- El año en curso está incompleto; las comparaciones usan períodos equivalentes.
- elecdb no trae columna de departamento ni proyectos en construcción: la lectura
  territorial es cualitativa y el pipeline se consulta en el registro de la UPME.
