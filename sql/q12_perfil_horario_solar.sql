-- Perfil horario promedio de la generación solar del SIN (MW promedio por hora).
-- Fuente: fact_hourly_recurso + dim_recurso (XM/SIN, elecdb).
SELECT extract(hour FROM hr.fecha_hora)::int AS hora,
       round((sum(hr."Gene") / (count(DISTINCT hr.fecha_hora::date) * 1000.0))::numeric, 0)
           AS solar_promedio_mw
FROM fact_hourly_recurso hr
JOIN dim_recurso r ON r.recurso_code = hr.recurso_code
WHERE upper(coalesce(r.ener_source, '')) = 'RAD SOLAR'
  AND hr.fecha_hora >= '2026-01-01'
GROUP BY 1
ORDER BY 1;
