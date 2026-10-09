-- Factor de emisión del SIN y emisiones totales por año.
-- Fuente: vista v_emisiones_trimestrales_sin (XM/SIN, elecdb).
SELECT extract(year FROM trimestre)::int AS anio,
       round(sum(generacion_total_gwh)::numeric, 0) AS generacion_gwh,
       round(sum(emisiones_totales_tonco2e)::numeric, 0) AS emisiones_ton_co2e,
       round((sum(emisiones_totales_tonco2e) * 1000.0 / nullif(sum(generacion_total_gwh) * 1000.0, 0))::numeric, 1)
           AS factor_emision_gco2e_kwh
FROM v_emisiones_trimestrales_sin
GROUP BY 1
ORDER BY 1;
