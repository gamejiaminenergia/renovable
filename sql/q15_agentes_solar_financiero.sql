-- Participación financiera de los agentes en el mercado mayorista.
-- Las ventas se reportan a nivel de agente (todas sus tecnologías), porque XM
-- no publica transacciones desagregadas por fuente de generación.
-- Fuente: fact_hourly_agente + dim_agente (XM/SIN).
SELECT a.agente_code,
       a.name AS agente,
       a.activity AS actividad,
       round((coalesce(sum(ha."VentContEner"), 0) / 1e6)::numeric, 1) AS ventas_contratos_gwh,
       round((coalesce(sum(ha."VentBolsNaciEner"), 0) / 1e6)::numeric, 1) AS ventas_bolsa_gwh,
       round((coalesce(sum(ha."CompContEner"), 0) / 1e6)::numeric, 1) AS compras_contratos_gwh,
       round((coalesce(sum(ha."CompBolsNaciEner"), 0) / 1e6)::numeric, 1) AS compras_bolsa_gwh,
       round(
           (coalesce(sum(ha."VentContEner"), 0) /
            nullif(coalesce(sum(ha."VentContEner"), 0) + coalesce(sum(ha."VentBolsNaciEner"), 0), 0)
            * 100)::numeric, 1) AS pct_ventas_contratos
FROM fact_hourly_agente ha
JOIN dim_agente a ON a.agente_code = ha.agente_code
WHERE ha.fecha_hora >= '2026-01-01'
GROUP BY a.agente_code, a.name, a.activity
ORDER BY ventas_contratos_gwh DESC;
