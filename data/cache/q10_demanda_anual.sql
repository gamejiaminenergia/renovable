-- Demanda anual del SIN y potencia máxima (indicador de crecimiento del mercado).
-- Fuente: fact_daily_sistema (XM/SIN, elecdb).
SELECT extract(year FROM fecha)::int AS anio,
       round((sum("DemaSIN") / 1e6)::numeric, 1) AS demanda_gwh,
       round((max("DemaMaxPot") / 1000.0)::numeric, 0) AS demanda_max_mw
FROM fact_daily_sistema
GROUP BY 1
ORDER BY 1;
