-- Entrada en operación de proyectos renovables por año (número y MW).
-- Fuente: dim_recurso (XM/SIN, elecdb).
SELECT extract(year FROM oper_start_date)::int AS anio,
       count(*) AS proyectos,
       upper(coalesce(ener_source, '')) AS fuente
FROM dim_recurso
WHERE upper(coalesce(ener_source, '')) IN ('RAD SOLAR', 'VIENTO')
  AND oper_start_date IS NOT NULL
GROUP BY 1, 3
ORDER BY 1, 3;
