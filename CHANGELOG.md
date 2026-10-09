# Historial de cambios

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
proyecto usa versionado semántico.

## [1.4.0] — 2026-10-09

### Agregado

- Documentos de repositorio: `LICENSE`, `NOTICE.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, `CITATION.cff`,
  `.editorconfig`, `.gitattributes` y las plantillas de `.github/`.
- Integración continua: lint, formato y pruebas en cada push, más la
  construcción del informe como artefacto descargable.
- Caché de consultas (`data/cache/*.csv` y `*.sql`) versionada para que el
  informe se reconstruya sin base de datos ni red.
- `uv.lock` para instalaciones reproducibles.

### Cambiado

- Se retiró el correo de contacto del informe: la portada con la dependencia
  responsable y el enlace a su ficha institucional es suficiente.

## [1.3.0] — 2026-10-09

### Agregado

- Dimensión empresarial: participación energética y financiera de los agentes
  solares, con concentración de mercado (HHI), curva de participación acumulada y
  ventas en contratos y bolsa.

### Cambiado

- La gráfica de capacidad y generación por agente pasó de dispersor de burbujas a
  barras emparejadas en dos paneles, para eliminar el traslape de etiquetas.
- El factor de planta se calcula solo sobre recursos con capacidad reportada.
- La propiedad de cada planta se toma de `dim_recurso.company_code`, no de la
  tabla N:N `dim_agente_recurso`.

## [1.2.0] — 2026-10-09

### Agregado

- Portada con la dependencia responsable: Oficina de Asuntos Regulatorios y
  Empresariales (OARE).

### Corregido

- Consistencia de las cifras metodológicas: 21 consultas regulatorias y 13
  consultas SQL.

## [1.1.0] — 2026-10-09

### Agregado

- Panel de **marco regulatorio y actualidad vigente** en cada sección, con estado
  de vigencia verificado contra el gestor normativo.
- Evidencia regulatoria ampliada a 21 consultas y sello de fecha en
  `data/regulatorio/_meta.json`.
- Comando `renovable vigencia`, que falla si la evidencia supera 30 días.
- Registro `data/marco_regulatorio.yaml` con 26 normas verificadas.

## [1.0.0] — 2026-10-09

### Agregado

- Proyecto MVC/SOLID en Python con SQL versionado sobre la base del mercado
  mayorista (XM/SIN en elecdb).
- Seis dimensiones de análisis: regulatoria, energética, de proyectos,
  financiera, socioambiental-territorial y de riesgos.
- KPIs, tablas, gráficas, tips, advertencias y conclusiones trazables.
- Render Jinja2 + Plotly/Kaleido + WeasyPrint y pruebas con pytest y ruff.
- Mapa de georreferenciación de los proyectos solares.
- Glosario y ficha país; informe íntegramente en español y en SVG.
