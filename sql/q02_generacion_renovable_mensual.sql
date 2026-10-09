-- Generación mensual solar y eólica (GWh) desde 2020.
-- Fuente: fact_hourly_recurso + dim_recurso (XM/SIN, elecdb).
SELECT date_trunc('month', hr.fecha_hora)::date AS mes,
       round((coalesce(sum(hr."Gene") FILTER (WHERE upper(coalesce(r.ener_source, '')) = 'RAD SOLAR'), 0) / 1e6)::numeric, 2)
           AS solar_gwh,
       round((coalesce(sum(hr."Gene") FILTER (WHERE upper(coalesce(r.ener_source, '')) = 'VIENTO'), 0) / 1e6)::numeric, 2)
           AS eolica_gwh
FROM fact_hourly_recurso hr
JOIN dim_recurso r ON r.recurso_code = hr.recurso_code
WHERE hr.fecha_hora >= '2020-01-01'
  AND upper(coalesce(r.ener_source, '')) IN ('RAD SOLAR', 'VIENTO')
GROUP BY 1
ORDER BY 1;
