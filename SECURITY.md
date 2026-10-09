# Política de seguridad

## Alcance

Este repositorio produce un informe de análisis a partir de fuentes públicas. No
presta un servicio en línea ni almacena datos personales.

## Credenciales y datos sensibles

- La conexión a la base del mercado se define por variables de entorno con el
  prefijo `RENOVABLE_` (ver `.env.example`). **No** se versionan archivos `.env`.
- Los valores por defecto del repositorio apuntan a una base local de desarrollo;
  no contienen credenciales productivas.
- El informe no incluye datos personales: las cifras se publican por agente
  (persona jurídica) y por municipio, a partir de información pública del mercado.

## Cómo reportar

Si encontrás una vulnerabilidad, un dato sensible expuesto o una cifra mal
atribuida, abrí un reporte privado al equipo mantenedor o un issue marcado como
`seguridad`. Incluí el archivo, la línea y una descripción del impacto.

Respondemos con un acuse de recibo y, si el hallazgo afecta el informe ya
publicado, se corrige y se regenera el PDF con una nueva versión.

## Buenas prácticas para contribuir

- No incluyas credenciales, tokens ni rutas locales en el código o los catálogos.
- No agregues datos que no sean de fuente pública o abierta, y registra siempre
  su origen en `NOTICE.md`.
- Si agregás una dependencia nueva, justificala en el pull request.
