-- Catálogo de proyectos renovables del SIN con capacidad >= 50 MW.
-- Fuente: dim_recurso + fact_daily_recurso + fact_hourly_recurso (XM/SIN, elecdb).
WITH renov AS (
    SELECT recurso_code,
           name,
           upper(coalesce(ener_source, '')) AS fuente,
           oper_start_date,
           company_code
    FROM dim_recurso
    WHERE upper(coalesce(ener_source, '')) IN ('RAD SOLAR', 'VIENTO')
),
diario AS (
    SELECT dr.recurso_code,
           max(dr."CapEfecNeta") AS cap_kw,
           avg(dr."ENFICC") AS enficc_kwh,
           avg(dr."ObligEnerFirme") AS oef_kwh,
           min(dr.fecha) AS primera_fecha
    FROM fact_daily_recurso dr
    GROUP BY dr.recurso_code
),
horario AS (
    SELECT hr.recurso_code,
           sum(hr."Gene") FILTER (WHERE hr.fecha_hora >= '2025-01-01' AND hr.fecha_hora < '2026-01-01') AS gen_2025,
           sum(hr."Gene") FILTER (WHERE hr.fecha_hora >= '2026-01-01') AS gen_2026
    FROM fact_hourly_recurso hr
    WHERE hr.fecha_hora >= '2025-01-01'
    GROUP BY hr.recurso_code
)
SELECT renov.name AS proyecto,
       renov.fuente,
       renov.company_code AS agente,
       renov.oper_start_date AS fecha_operacion,
       round((diario.cap_kw / 1000.0)::numeric, 1) AS capacidad_mw,
       round((coalesce(horario.gen_2025, 0) / 1e6)::numeric, 1) AS gen_2025_gwh,
       round((coalesce(horario.gen_2026, 0) / 1e6)::numeric, 1) AS gen_2026_gwh,
       round(diario.enficc_kwh::numeric, 0) AS enficc_kwh,
       round(diario.oef_kwh::numeric, 0) AS oef_kwh,
       diario.primera_fecha
FROM renov
JOIN diario ON diario.recurso_code = renov.recurso_code
LEFT JOIN horario ON horario.recurso_code = renov.recurso_code
WHERE diario.cap_kw >= 50000
ORDER BY capacidad_mw DESC;
