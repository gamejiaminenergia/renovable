-- Puntos de referencia municipal (centroides DIVIPOLA) para georreferenciar
-- los proyectos renovables del informe.
-- Fuente: temporal.geo_municipios (DIVIPOLA, datos.gov.co dataset gdxc-w37w).
SELECT cod_mpio,
       cod_dpto,
       departamento,
       municipio,
       latitud,
       longitud,
       fuente
FROM temporal.geo_municipios
WHERE latitud IS NOT NULL
  AND longitud IS NOT NULL
ORDER BY cod_mpio;
