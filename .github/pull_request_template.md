## Qué cambia

<!-- Describí el cambio en una o dos frases. -->

## Tipo de cambio

- [ ] Contenido del informe (secciones, KPIs, tablas, gráficas)
- [ ] Marco regulatorio o evidencia CREG
- [ ] Datos o consultas SQL
- [ ] Código o infraestructura

## Secciones afectadas

<!-- Listá los bloques de content/bloques/ que cambian, o "ninguna". -->

## Verificación

- [ ] `uv run pytest -q` en verde
- [ ] `uv run ruff check . && uv run ruff format --check .` en verde
- [ ] `uv run renovable verificar` sin errores
- [ ] `uv run renovable vigencia` sin evidencia vencida
- [ ] El PDF se reconstruyó con `uv run renovable build`

## Toma de datos

<!-- Si cambian cifras: indicá la consulta sql/qNN que las produce y si la base
se refrescó. Si cambia el marco regulatorio: indicá la norma y su Diario Oficial. -->

## Capturas

<!-- Si cambia el diseño, adjuntá la página renderizada. -->
