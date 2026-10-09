# Repository Guidelines

## Project Structure & Module Organization

`src/renovable/` es **MVC literal**. `config/` guarda ajustes y rutas
(`pydantic-settings`, prefijo `RENOVABLE_`). `models/` es el Modelo: `entidades/`
(`Bloque`, `Kpi`, `Figura`, `Tabla`, `Proyecto`, `Fuente`), `puertos.py`
(Protocols) y `reglas/` (cálculo de KPI, formato y validación editorial) y
`servicios/` (composición del informe). `repositories/` son los adaptadores:
`elecdb.py` (SQL sobre XM/SIN), `regulatorio.py` (evidencia CREG), `catalogos.py`
(YAML de contenido) y `web.py` (caché de internet). `views/` es la Vista:
`charts/` (Plotly), `html_renderer.py` (Jinja2) y `pdf_renderer.py`
(WeasyPrint). `controllers/` es el Controlador: `composicion.py` es el único
*composition root* y `cli/` expone los comandos. La dependencia va siempre de
`views`/`controllers` hacia `models`, nunca al revés.

## Build, Test, and Development Commands

```bash
uv pip install --python .venv/bin/python -r requirements.txt
python -m renovable regulatorio          # estado de la evidencia CREG
python -m renovable extract --refrescar  # ejecuta sql/ y puebla data/cache/
python -m renovable verificar            # valida el informe sin exportar
python -m renovable build                # figuras + HTML + PDF
pytest -q && ruff check . && ruff format --check .
```

Entregable único: `output/Informe_Renovables_Cancilleria.pdf`.

## Coding Style & Naming Conventions

Python 3.12, indentación de 4 espacios, anotaciones de tipo, `snake_case` para
funciones y `CamelCase` para clases. Los módulos y los identificadores se
nombran en español; los comentarios explican el porqué, no el qué. Consultas
`qNN_*`, evidencia `RNN_*`, pruebas `test_*`.

## Testing Guidelines

`pytest`, sin base de datos ni red: se inyectan los dobles de `tests/dobles.py`.
`test_contenido.py` compone el informe real con series sintéticas y verifica que
ninguna cifra quede sin resolver, que cada sección traiga marco regulatorio y
actualidad, y que el registro de instrumentos resuelva todos los ids citados;
`test_qa_pdf.py` comprueba que el HTML y el PDF traigan todas las secciones.
Usar `pytest.approx` en cifras.

## Content Rules

Ningún texto ni cifra se escribe en plantillas o código: todo vive en
`content/informe.yaml` (manifiesto) y en `content/bloques/*.yaml`, con las cifras
entre llaves (`{cap_solar_mw}`) que el servicio resuelve desde `data/catalogo_kpis.yaml`.
El build falla si un bloque queda sin fuente, sin método, sin conclusión, sin tip
o sin advertencia, **sin marco regulatorio o sin actualidad regulatoria**, o si
una figura queda sin leyenda o sin fuente. Las gráficas se declaran en
`data/catalogo_graficas.yaml` y su dibujo en `views/charts/figuras.py`. Las
normas y políticas se declaran una sola vez en `data/marco_regulatorio.yaml` y
los bloques las referencian por id (`marco_regulatorio: [ley_1715_2014, ...]`).

## Data Rules

Toda cifra cuantitativa proviene de `sql/qNN_*.sql` (elecdb, XM/SIN) y se cachea
como CSV junto a su SQL en `data/cache/`. La evidencia regulatoria proviene de
`tools/fetch_regulatorio.py` contra el asistente CREG (hoy 21 consultas
temáticas) y se archiva en `data/regulatorio/` con su sello de fecha en
`_meta.json`; `python -m renovable vigencia` falla si esa evidencia supera los
treinta días. Toda norma citada debe verificarse contra el gestor normativo
(objeto oficial y Diario Oficial) antes de entrar al registro. No se inventan
cifras: si un dato no existe en la fuente, se declara la limitación en la
advertencia del bloque.

## Commit & Pull Request Guidelines

Mensajes en español, en imperativo y sin prefijos (`feat:`, `fix:`):
*"Agrega la dimensión de riesgos"*. En el PR: qué bloques cambian, que `pytest`
y `ruff` pasan y que el PDF se reconstruyó.
