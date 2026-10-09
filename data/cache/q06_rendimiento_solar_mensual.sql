-- Rendimiento técnico de la flota solar: irradiación y temperaturas (G16).
-- Fuente: fact_daily_recurso + dim_recurso (XM/SIN, elecdb).
SELECT to_char(date_trunc('month', dr.fecha), 'YYYY-MM') AS mes,
       round(avg(dr."IrrGlobal")::numeric, 1) AS irr_global_wh_m2,
       round(avg(dr."TempAmbSolar")::numeric, 1) AS temp_ambiente_c,
       round(avg(dr."TempPanel")::numeric, 1) AS temp_panel_c,
       count(*) AS registros
FROM fact_daily_recurso dr
JOIN dim_recurso r ON r.recurso_code = dr.recurso_code
WHERE upper(coalesce(r.ener_source, '')) = 'RAD SOLAR'
  AND dr.fecha >= '2025-01-01'
  AND dr."IrrGlobal" IS NOT NULL
GROUP BY 1
ORDER BY 1;
