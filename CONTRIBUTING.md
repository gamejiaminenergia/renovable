# Cómo contribuir

Gracias por aportar al informe de energías renovables. Antes de escribir código
o contenido, leé [`AGENTS.md`](AGENTS.md): ahí están las reglas de arquitectura,
de estilo y de trazabilidad que este repositorio exige.

## Puesta en marcha

```bash
git clone <url-del-repositorio>
cd renovable
uv sync                       # crea el entorno e instala dependencias
cp .env.example .env          # ajusta la conexión a elecdb si vas a refrescar datos

uv run pytest -q              # debe quedar en verde sin base de datos ni red
uv run ruff check .
uv run renovable verificar    # valida el informe compuesto
uv run renovable build        # reconstruye el PDF desde la caché
```

Las pruebas y el `build` funcionan **sin base de datos y sin red** porque el
repositorio incluye la caché de resultados (`data/cache/`) y la evidencia
regulatoria (`data/regulatorio/`).

Solo necesitás conexión a elecdb si vas a refrescar las series con
`uv run renovable extract --refrescar`, y al servidor de la skill CREG si vas a
levantar nueva evidencia normativa con `python3 tools/fetch_regulatorio.py`.

## Flujo de trabajo

1. Creá una rama desde `main` con un nombre descriptivo (`nueva-seccion-agentes`,
   `fix-mapa-svg`, `actualiza-evidencia-creg`).
2. Hacé el cambio en el menor alcance posible.
3. Corré `uv run pytest -q`, `uv run ruff check . && uv run ruff format .` y
   `uv run renovable build` si tocaste contenido o gráficas.
4. Abrí el pull request con la plantilla del repositorio.

## Reglas que no se negocian

- **Nada de cifras escritas a mano.** Todo número vive como marcador en
  `content/bloques/*.yaml` y se resuelve desde `data/catalogo_kpis.yaml`.
- **Todo en español.** No se admiten títulos, leyendas ni párrafos en otro idioma.
- **Todo en SVG.** Las gráficas se exportan con `format="svg"`; no se reintroducen
  PNG.
- **Trazabilidad obligatoria.** Cada bloque requiere fuente, método, conclusión,
  tip y advertencia, más marco regulatorio y actualidad verificada.
- **Sin datos inventados.** Si un dato no existe en la fuente, se declara la
  limitación en la advertencia del bloque.

## Cómo agregar contenido

| Querés… | Editá |
|---|---|
| Agregar una sección | `content/informe.yaml` (manifiesto) + `content/bloques/<id>.yaml` |
| Agregar un indicador | `data/catalogo_kpis.yaml` y `src/renovable/models/reglas/kpis.py` |
| Agregar una gráfica | `data/catalogo_graficas.yaml` + `src/renovable/views/charts/figuras.py` |
| Agregar una norma al marco | `data/marco_regulatorio.yaml` y referenciala por id en el bloque |
| Agregar una consulta | `sql/qNN_descripcion.sql`; el repositorio la recoge sola |

## Commits y pull requests

Mensajes en español, en imperativo y sin prefijos (`feat:`, `fix:`):
*"Agrega la dimensión empresarial"*. Cuerpo con viñetas cuando haga falta
detalle. En el PR indicá qué secciones cambian, que `pytest` y `ruff` pasan y que
el PDF se reconstruyó.
