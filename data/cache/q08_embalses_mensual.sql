-- Nivel agregado de embalses y aportes hídricos por mes (contexto de confiabilidad).
-- Fuente: fact_daily_sistema (XM/SIN, elecdb).
SELECT to_char(date_trunc('month', fecha), 'YYYY-MM') AS mes,
       round((avg("PorcVoluUtilDiar") * 100)::numeric, 1) AS embalses_pct,
       round((sum("AporEner") / 1e6)::numeric, 1) AS aportes_gwh,
       round((avg("AporEner") / nullif(avg("AporEnerMediHist"), 0) * 100)::numeric, 1) AS aportes_vs_media_pct,
       round((sum("VertEner") / 1e6)::numeric, 1) AS vertimientos_gwh
FROM fact_daily_sistema
WHERE fecha >= '2020-01-01'
GROUP BY 1
ORDER BY 1;
