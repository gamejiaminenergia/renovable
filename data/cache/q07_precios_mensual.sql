-- Precios mensuales del MEM: bolsa, contratos, escasez y nivel de embalses.
-- Fuente: fact_daily_sistema (XM/SIN, elecdb).
SELECT to_char(date_trunc('month', fecha), 'YYYY-MM') AS mes,
       round(avg("PPPrecBolsNaci")::numeric, 1) AS bolsa_cop_kwh,
       round(avg("PrecPromCont")::numeric, 1) AS contratos_cop_kwh,
       round(avg("PrecEsca")::numeric, 1) AS escasez_cop_kwh,
       round((avg("PorcVoluUtilDiar") * 100)::numeric, 1) AS embalses_pct,
       round((avg("DemaSIN") / 1e6)::numeric, 2) AS demanda_prom_gwh_dia
FROM fact_daily_sistema
WHERE fecha >= '2020-01-01'
GROUP BY 1
ORDER BY 1;
