# Datos del informe

Este directorio contiene todo lo que el informe usa como insumo, separado por
naturaleza y con su política de actualización.

## Qué hay aquí

| Ruta | Contenido | ¿Se versiona? |
|---|---|---|
| `cache/q*.csv` y `cache/q*.sql` | Resultado de cada consulta SQL y el SQL exacto que lo produjo | Sí |
| `cache/web/` | Caché HTML de la investigación de internet | No (se regenera) |
| `regulatorio/R*.md` | Respuestas del asistente normativo de la CREG | Sí |
| `regulatorio/_meta.json` | Fecha de obtención de cada consulta regulatoria | Sí |
| `fuentes/meta_fncer.json` | Registro oficial de proyectos FNCER (datos.gov.co `vy9n-w6hc`) | Sí |
| `geografia_proyectos.yaml` | Municipio y código DIVIPOLA de cada proyecto del informe | Sí |
| `marco_regulatorio.yaml` | Normas y políticas verificadas, con su vigencia y evidencia | Sí |
| `catalogo_*.yaml` | Presentación de KPI, gráficas, fuentes y preguntas regulatorias | Sí |
| `preguntas_creg.yaml` | Las 21 consultas temáticas al asistente de la CREG | Sí |

## Por qué se versiona la caché

`data/cache/` guarda el resultado de las consultas y **una copia del SQL que lo
produjo**. Eso permite tres cosas:

1. Cualquier cifra del informe es rastreable a su consulta exacta.
2. El informe se reconstruye sin base de datos y sin red (`renovable build`).
3. La integración continua puede generar el PDF como artefacto.

Los datos primarios no se redistribuyen: la caché contiene **agregaciones y
cálculos propios** sobre información pública del mercado. Ver `../NOTICE.md`.

## Cómo refrescar

```bash
# 1. Evidencia regulatoria (requiere el servidor de la skill CREG en localhost:3000)
python3 tools/fetch_regulatorio.py --forzar
uv run renovable vigencia          # falla si la evidencia supera 30 días

# 2. Series del mercado (requiere acceso de lectura a elecdb)
uv run renovable extract --refrescar

# 3. Reconstruir el informe con los datos nuevos
uv run renovable build
```

Después de refrescar, revisá el `git diff` de `data/cache/`: un cambio de cifras
sin cambio de SQL es la señal de que la base se actualizó, y conviene anotarlo en
`CHANGELOG.md`.

## Variables de entorno

| Variable | Para qué | Valor por defecto |
|---|---|---|
| `RENOVABLE_ELECDB_DSN` | Conexión a la base del mercado (XM/SIN) | `postgresql://postgres:postgres@localhost:5432/postgres` |
| `RENOVABLE_CREG_API` | Servidor del asistente normativo de la CREG | `http://localhost:3000/api/ask` |
| `RENOVABLE_CREG_TIMEOUT_S` | Tiempo máximo por consulta regulatoria | `300` |
