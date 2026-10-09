-- Componentes de cargos y contribuciones mensuales del sistema.
-- Fuente: fact_monthly_sistema (XM/SIN, elecdb).
SELECT to_char(fecha, 'YYYY-MM') AS mes,
       "CEE" AS cee,
       "CERE" AS cere,
       "MC" AS mc,
       "CargoUsoSTN" AS cargo_uso_stn,
       "CargoUsoSTR" AS cargo_uso_str,
       "PrecFAZNI" AS prec_fazni,
       "FAER" AS faer
FROM fact_monthly_sistema
WHERE fecha >= '2025-01-01'
ORDER BY fecha;
