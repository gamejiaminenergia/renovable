-- Mezcla de generación anual del SIN por tecnología (GWh).
-- Fuente: fact_hourly_recurso + dim_recurso (XM/SIN, elecdb).
WITH base AS (
    SELECT extract(year FROM hr.fecha_hora)::int AS anio,
           upper(coalesce(r.ener_source, '')) AS fuente,
           hr."Gene" AS gene
    FROM fact_hourly_recurso hr
    JOIN dim_recurso r ON r.recurso_code = hr.recurso_code
)
SELECT anio,
       round((coalesce(sum(gene) FILTER (WHERE fuente = 'AGUA'), 0) / 1e6)::numeric, 1) AS hidro_gwh,
       round((coalesce(sum(gene) FILTER (WHERE fuente IN ('GAS', 'CARBON', 'ACPM', 'COMBUSTOLEO', 'GLP', 'JET-A1')), 0) / 1e6)::numeric, 1) AS termica_gwh,
       round((coalesce(sum(gene) FILTER (WHERE fuente = 'RAD SOLAR'), 0) / 1e6)::numeric, 1) AS solar_gwh,
       round((coalesce(sum(gene) FILTER (WHERE fuente = 'VIENTO'), 0) / 1e6)::numeric, 1) AS eolica_gwh,
       round((coalesce(sum(gene) FILTER (WHERE fuente IN ('BAGAZO', 'BIOMASA', 'BIOGAS')), 0) / 1e6)::numeric, 1) AS biomasa_gwh
FROM base
GROUP BY anio
ORDER BY anio;
