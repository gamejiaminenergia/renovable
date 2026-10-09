# Plan del informe ejecutivo de energías renovables para la Cancillería

**Entregable:** `output/Informe_Renovables_Cancilleria.pdf`
**Emisor:** Ministerio de Minas y Energía
**Destinatario:** Cancillería de Colombia (Ministerio de Relaciones Exteriores)
**Encuadre:** diplomacia energética — posicionamiento, inversión y cooperación
**Ventana de análisis:** 2020-2026, con corte en el último dato disponible de elecdb
**Versión del plan:** 1.0

> **Foco regulatorio transversal (v1.1).** Cada una de las seis dimensiones abre
> con un panel de *Marco regulatorio y actualidad vigente*: las normas y
> políticas aplicables con su estado de vigencia y un párrafo de actualidad
> verificada. El build falla si un bloque narrativo no trae ambos elementos.

---

## 1. Resumen

El proyecto produce un informe ejecutivo de ~30 páginas, reproducible y con
trazabilidad completa, sobre el desarrollo de proyectos de energías renovables
en Colombia. Se construye en seis dimensiones: regulatoria, energética y
técnica, de proyectos, financiera, socioambiental-territorial y de riesgos, más
un bloque de conclusiones y recomendaciones.

La regla editorial es estricta: **ninguna cifra se escribe a mano**. Todo dato
proviene de una consulta SQL versionada sobre la base del mercado mayorista
(XM/SIN en elecdb) o de evidencia normativa archivada del asistente de la CREG.
Si un dato falta, la construcción falla en lugar de publicar un valor incompleto.

**Fase regulatoria primero.** El capítulo regulatorio se levanta y se cierra
antes de redactar cualquier otro; sin él no se inicia la fase cuantitativa.

### Protocolo de verificación de vigencia

1. El asistente CREG responde 21 consultas temáticas (R01-R21) y cada respuesta
   se archiva en `data/regulatorio/R*.md` con sello de fecha en `_meta.json`.
2. Cada norma candidata se comprueba **una por una** contra el gestor normativo
   (Alejandría / CREG): se confirma el objeto oficial y la referencia de Diario
   Oficial. Las que no se pueden verificar no entran al informe.
3. Las normas verificadas se declaran una sola vez en
   `data/marco_regulatorio.yaml` con su alcance, vigencia, evidencia y enlace.
4. `python -m renovable vigencia` falla si la evidencia supera los 30 días;
   `build` falla si un bloque no cita marco regulatorio o actualidad.

---

## 2. Arquitectura

Patrón MVC literal con principios SOLID. La dependencia siempre apunta hacia el
modelo: `views -> models` y `controllers -> models`, nunca al revés.

```
src/renovable/
├── config/          Ajustes y rutas (pydantic-settings, prefijo RENOVABLE_)
├── models/
│   ├── entidades/   Bloque, Kpi, Figura, Tabla, Proyecto, Fuente
│   ├── puertos.py   Protocols: FuenteDatos, FuenteRegulatoria, FuenteWeb, Catalogo…
│   ├── reglas/      Cálculo de KPI, formato colombiano y validación editorial
│   └── servicios/   ServicioInforme: compone datos + catálogos -> bloques
├── repositories/    elecdb (SQL), regulatorio (CREG), catálogos YAML, web
├── views/           charts/ (Plotly), HtmlRenderer (Jinja2), PdfRenderer (WeasyPrint)
└── controllers/     composicion.py (composition root) y cli/ (comandos)
```

Cada librería externa vive detrás de una sola frontera: `plotly`/`kaleido` solo
en `views/charts/`, `jinja2` en `views/html_renderer.py`, `weasyprint` en
`views/pdf_renderer.py`, `psycopg` en `repositories/elecdb.py`, `yaml` en
`repositories/catalogos.py` y `requests` en `repositories/web.py`.

### Bus de datos

| Etapa | Artefacto | Responsable |
|---|---|---|
| Evidencia regulatoria | `data/regulatorio/R01…R12.md` | `tools/fetch_regulatorio.py` |
| Series del mercado | `data/cache/qNN.csv` + `qNN.sql` | `repositories/elecdb.py` |
| Cálculo de indicadores | `dict[str, float]` | `models/reglas/kpis.py` |
| Composición narrativa | `list[Bloque]` | `models/servicios/informe_service.py` |
| Gráficas | `build/figuras/*.png` | `views/charts/renderer.py` |
| HTML | `build/informe.html` | `views/html_renderer.py` |
| PDF | `output/Informe_Renovables_Cancilleria.pdf` | `views/pdf_renderer.py` |

---

## 3. Contenido del informe

| # | Bloque | Contenido | Figuras | Tablas |
|---|---|---|---|---|
| 1 | Portada | Identidad MinMinas, destinatario, corte y versión | — | — |
| 2 | Resumen ejecutivo (ES) | Mensaje central, 7 KPI, hallazgos | Participación renovable | — |
| 3 | Executive summary (EN) | Misma narrativa en inglés para contrapartes | — | — |
| 4 | Metodología | Fuentes, fase regulatoria primero, límites | — | — |
| 5 | Regulatorio | Marco y actualidad, incentivos, barreras | — | Instrumentos normativos |
| 6 | Energético | Capacidad, generación, perfil horario, emisiones | 6 | Mix anual |
| 7 | Proyectos | Catálogo del SIN y frontera eólica | 2 | Top 13 y parques eólicos |
| 8 | Financiero | Precios, contratos, cargos, costo de capital | 2 | Últimos 12 meses |
| 9 | Socioambiental y territorial | Territorio, comunidades, ambiente | — | Lectura territorial |
| 10 | Riesgos | Red, hidrología, licenciamiento, cambiario | — | Mapa de riesgos |
| 11 | Conclusiones | Cinco conclusiones y cinco recomendaciones | — | — |
| 12 | Fuentes | Índice de fuentes con enlace y tipo | — | — |

Cada bloque narrativo exige **fuente, método, conclusión, tip y advertencia**;
**marco regulatorio y actualidad regulatoria**; `models/reglas/validacion.py`
rechaza el informe si falta cualquiera.

### Marco regulatorio por dimensión

| Dimensión | Instrumentos principales citados |
|---|---|
| Regulatoria | Leyes 1715/2014 y 2099/2021, Ley 2294/2023 (art. 233), CONPES 4075/2022, CREG 030/2018, 174/2021, 024/2015, 075/2021, 101 104/2026, 701 126/2026, 101 113/2026, 701 091/2025 |
| Energética | CREG 060/2019, 148/2021, 101 011/2022, 101 104/2026, 701 126/2026; UPME 749/2025 |
| Proyectos | UPME 749/2025; CREG 075/2021, 101 094/2025, 701 133/2026, 701 091/2025 |
| Financiera | MME 40208/2026, CREG 701 125/2026, Decreto 1223/2025, CREG 075/2021, MME 40311/2020 |
| Socioambiental y territorial | Decreto 1186/2025 (LAEólica), Decreto 1540/2024, MADS 418/2026, CREG 174/2021, CREG 701 091/2025 |
| Riesgos | CREG 101 094/2025, 701 133/2026, 075/2021, 101 113/2026; Decreto 1186/2025 |

### Indicadores publicados

`anio`, `cap_solar_mw`, `cap_eolica_mw`, `cap_renovable_mw`, `cap_plantas`,
`gen_solar_gwh`, `gen_eolica_gwh`, `gen_renovable_gwh`, `gen_total_gwh`,
`gen_renovable_pct`, `gen_solar_pct`, `gen_renovable_2025_gwh`,
`gen_renovable_pct_2025`, `crecimiento_renovable_pct`, `proyectos_operando`,
`proyectos_mayores_50mw`, `eolica_parques`, `precio_bolsa_cop_kwh`,
`precio_contratos_cop_kwh`, `prima_bolsa_contratos_pct`, `embalses_pct`,
`factor_emision_gco2e_kwh`, `emisiones_evitadas_ton`, `demanda_gwh`,
`demanda_max_mw`.

Su presentación y trazabilidad viven en `data/catalogo_kpis.yaml`; los umbrales
de alerta marcan en rojo los indicadores que incumplen la meta.

---

## 4. Interfaces públicas

```bash
python -m renovable regulatorio      # estado de la evidencia CREG (fase 1)
python -m renovable vigencia         # verifica que la evidencia sea la más reciente
python -m renovable extract          # ejecuta sql/ y puebla data/cache/
python -m renovable extract --refrescar
python -m renovable verificar        # valida el informe sin exportar
python -m renovable build            # dibuja figuras y exporta el PDF
python -m renovable build --refrescar
```

Variables de entorno (prefijo `RENOVABLE_`): `ELECDB_DSN`, `CREG_API`,
`CREG_TIMEOUT_S`. Valores por defecto en `src/renovable/config/settings.py`.

Agregar contenido = agregar un bloque YAML en `content/bloques/` y una línea al
manifiesto `content/informe.yaml`. No se edita código ni plantillas.

---

## 5. Plan de pruebas

| Prueba | Qué garantiza |
|---|---|
| `tests/test_reglas.py` | Formato colombiano, cálculo de KPI, semáforos, validación editorial, numeración contigua |
| `tests/test_contenido.py` | El contenido real compone sin marcadores huérfanos; las cifras aterrizan en el texto; las tablas se llenan |
| `tests/test_qa_pdf.py` | El HTML trae todas las secciones y cajas; el PDF supera diez páginas; los marcadores inexistentes fallan |
| `ruff check` + `ruff format --check` | Estilo y orden de importaciones |

Criterios de aceptación:

1. `python -m renovable build` termina con salida 0 y produce el PDF.
2. `python -m renovable verificar` no reporta errores y `vigencia` no reporta
   evidencia vencida.
3. Una segunda ejecución sin `--refrescar` reconstruye el mismo PDF desde caché.
4. Toda cifra del informe es rastreable a un archivo `qNN.sql` o a una respuesta
   `R*.md`.
5. `pytest` y `ruff` pasan en verde.

---

## 6. Supuestos y límites declarados

- **Capacidad eólica:** XM no publica `CapEfecNeta` para la flota eólica en esta
  carga. Se usa el pico horario observado sumado por parque como cota inferior y
  se declara en el informe.
- **Año en curso incompleto:** el corte es septiembre de 2026; las comparaciones
  usan períodos equivalentes (enero-septiembre) y no totales anuales.
- **Nivel de embalses:** `PorcVoluUtilDiar` viene en fracción (0-1) en esta
  carga; se multiplica por 100 para expresarlo en porcentaje.
- **Territorio:** elecdb no lleva columna de departamento; la lectura territorial
  es cualitativa y se apoya en la ubicación conocida de los proyectos.
- **Pipeline:** elecdb registra recursos habilitados, no proyectos en
  construcción; el pipeline en prefactibilidad y factibilidad se consulta en el
  registro de la UPME (Resolución UPME 749 de 2025).
- **Accesos:** ANLA e IRENA bloquean peticiones directas; su contenido se cita
  mediante fuentes secundarias o espejos.
- **Identidad:** el membrete es una reconstrucción tipográfica y cromática; no se
  usan logos de terceros.
- **Vigencia:** la fecha de verificación es la del sello de `_meta.json`; toda
  norma citada fue comprobada contra el gestor normativo en esa fecha.

---

## 7. Mantenimiento

1. Revisar la actualidad regulatoria: `python -m renovable regulatorio` y
   `python -m renovable vigencia`; si algo está vencido,
   `python3 tools/fetch_regulatorio.py --forzar`.
2. Revalidar contra el gestor normativo las normas nuevas y agregarlas a
   `data/marco_regulatorio.yaml`.
3. Refrescar las series: `python -m renovable extract --refrescar`.
4. Reconstruir: `python -m renovable build` (usa la caché y no vuelve a la base).
5. Verificar: `python -m renovable verificar` y `pytest`.

Cadencia sugerida: semestral, antes de cada presentación oficial. Como base del
mercado se corrige de forma retroactiva, se recomienda refrescar justo antes de
la publicación.
