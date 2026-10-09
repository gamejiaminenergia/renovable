# Capa departamental para el mapa

`colombia_departamentos.geo.json` es la capa de límites departamentales que usa
la figura `fig_mapa_proyectos`. Tiene 33 departamentos con las propiedades
`codigo` (DIVIPOLA de dos dígitos) y `nombre`, y las coordenadas están redondeadas
a tres decimales para que el SVG del mapa pese poco y WeasyPrint lo renderice
rápido.

## Procedencia

La geometría es una **elaboración derivada de cartografía pública de uso
referencial** de los límites departamentales de Colombia, preparada para los
informes del despacho. Es un insumo de representación gráfica: no tiene validez
catastral ni oficial para delimitar jurisdicciones.

Las coordenadas de los proyectos **no** vienen de esta capa: se toman del
centroide municipal del DIVIPOLA (`temporal.geo_municipios` en elecdb, consulta
`q13_geo_municipios`) y el municipio se toma del registro oficial FNCER. La
ubicación exacta de cada planta está en el registro de proyectos de la UPME.

## Cómo se regenera

```bash
python3 tools/simplificar_geojson.py [ruta_al_geojson_de_origen]
```

Si no se indica ruta, la herramienta usa la capa disponible en el equipo de
trabajo. El resultado siempre se escribe en este directorio.
