-- Capacidad renovable al cierre de cada año (MW).
--   solar_mw  : capacidad efectiva neta (CapEfecNeta) al último dato del año.
--   eolica_mw : máximo horario observado del año. En esta carga de elecdb la
--               flota eólica no reporta "CapEfecNeta", por lo que se usa el pico
--               horario como cota inferior de la capacidad instalada.
-- Fuente: fact_daily_recurso + fact_hourly_recurso + dim_recurso (XM/SIN).
WITH solar_base AS (
    SELECT dr.recurso_code, dr.fecha, dr."CapEfecNeta" AS cap_kw
    FROM fact_daily_recurso dr
    JOIN dim_recurso r ON r.recurso_code = dr.recurso_code
    WHERE upper(coalesce(r.ener_source, '')) = 'RAD SOLAR'
      AND dr."CapEfecNeta" IS NOT NULL
),
solar_cierre AS (
    SELECT DISTINCT ON (recurso_code, extract(year FROM fecha))
           recurso_code,
           extract(year FROM fecha)::int AS anio,
           cap_kw
    FROM solar_base
    ORDER BY recurso_code, extract(year FROM fecha), fecha DESC
),
solar AS (
    SELECT anio,
           sum(cap_kw) / 1000.0 AS solar_mw,
           count(*) FILTER (WHERE cap_kw > 0) AS plantas_con_capacidad
    FROM solar_cierre
    GROUP BY anio
),
eolica AS (
    SELECT anio, sum(pico_mw) AS eolica_mw
    FROM (
        SELECT extract(year FROM hr.fecha_hora)::int AS anio,
               hr.recurso_code,
               max(hr."Gene") / 1000.0 AS pico_mw
        FROM fact_hourly_recurso hr
        JOIN dim_recurso r ON r.recurso_code = hr.recurso_code
        WHERE upper(coalesce(r.ener_source, '')) = 'VIENTO'
        GROUP BY 1, 2
    ) picos
    GROUP BY anio
)
SELECT s.anio,
       round(s.solar_mw::numeric, 1) AS solar_mw,
       round(coalesce(e.eolica_mw, 0)::numeric, 1) AS eolica_mw,
       s.plantas_con_capacidad
FROM solar s
LEFT JOIN eolica e USING (anio)
ORDER BY s.anio;
