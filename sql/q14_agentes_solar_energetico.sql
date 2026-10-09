-- Participación energética de los agentes en la generación solar del SIN.
-- El dueño del recurso se toma de dim_recurso.company_code (XM no publica la
-- propiedad en la tabla N:N dim_agente_recurso, que está incompleta).
-- Fuente: dim_recurso + fact_daily_recurso + fact_hourly_recurso (XM/SIN).
WITH horas AS (
    SELECT count(DISTINCT fecha_hora)::numeric AS n
    FROM fact_hourly_recurso
    WHERE fecha_hora >= '2026-01-01'
),
solar AS (
    SELECT recurso_code, company_code
    FROM dim_recurso
    WHERE upper(coalesce(ener_source, '')) = 'RAD SOLAR'
),
cap AS (
    SELECT recurso_code,
           max("CapEfecNeta") AS cap_kw,
           avg("ENFICC") AS enficc_kwh,
           avg("ObligEnerFirme") AS oef_kwh
    FROM fact_daily_recurso
    WHERE fecha >= '2026-01-01'
      AND "CapEfecNeta" IS NOT NULL
    GROUP BY recurso_code
),
gen AS (
    SELECT recurso_code, sum("Gene") AS gene_kwh
    FROM fact_hourly_recurso
    WHERE fecha_hora >= '2026-01-01'
    GROUP BY recurso_code
),
-- Generación solo de los recursos que reportan capacidad efectiva neta: es la
-- base correcta para el factor de planta (los AGPE no reportan CapEfecNeta).
gen_capacitada AS (
    SELECT g.recurso_code, g.gene_kwh
    FROM gen g
    JOIN cap ON cap.recurso_code = g.recurso_code
)
SELECT a.agente_code,
       a.name AS agente,
       count(DISTINCT s.recurso_code) AS plantas,
       count(DISTINCT cap.recurso_code) AS plantas_con_capacidad,
       round((coalesce(sum(cap.cap_kw), 0) / 1000.0)::numeric, 1) AS capacidad_mw,
       round((coalesce(sum(gen.gene_kwh), 0) / 1e6)::numeric, 1) AS generacion_gwh,
       round((coalesce(sum(genc.gene_kwh), 0) / 1e6)::numeric, 1) AS generacion_capacitada_gwh,
       round((coalesce(sum(cap.cap_kw), 0) * (SELECT n FROM horas))::numeric, 0) AS capacidad_kwh_periodo,
       round(sum(cap.enficc_kwh)::numeric, 0) AS enficc_kwh,
       round(sum(cap.oef_kwh)::numeric, 0) AS oef_kwh
FROM solar s
JOIN dim_agente a ON a.agente_code = s.company_code
LEFT JOIN cap ON cap.recurso_code = s.recurso_code
LEFT JOIN gen ON gen.recurso_code = s.recurso_code
LEFT JOIN gen_capacitada genc ON genc.recurso_code = s.recurso_code
GROUP BY a.agente_code, a.name
HAVING coalesce(sum(cap.cap_kw), 0) > 0
ORDER BY capacidad_mw DESC;
