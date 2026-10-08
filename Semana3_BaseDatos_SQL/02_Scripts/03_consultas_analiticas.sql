-- 1. Validación de Volumen Total de Registros (Comprueba los 1,000 registros del proyecto)
SELECT 
    (SELECT COUNT(*) FROM cat_departamentos) AS total_departamentos,
    (SELECT COUNT(*) FROM dim_clientes)      AS total_clientes,
    (SELECT COUNT(*) FROM fact_prestamos)     AS total_prestamos;

-- 2. Inspección preliminar de los primeros registros cargados
SELECT * FROM cat_departamentos;
SELECT * FROM dim_clientes LIMIT 5;
SELECT * FROM fact_prestamos LIMIT 5;

-- 3. Validación de consistencia: Verificar que no existan préstamos huérfanos sin cliente
SELECT COUNT(*) AS prestamos_sin_cliente
FROM fact_prestamos p
LEFT JOIN dim_clientes c ON p.id_cliente = c.id_cliente
WHERE c.id_cliente IS NULL;

-- =============================================================================
-- PROYECTO: FinSafe SV - Diagnóstico y Monitoreo del Riesgo Crediticio
-- ARCHIVO: 03_consultas_analiticas.sql
-- DESCRIPCIÓN: Consultas analíticas alineadas a las preguntas del proyecto
-- REQUISITOS: SELECT, WHERE, ORDER BY, GROUP BY, Agregaciones y JOINs
-- =============================================================================

-- -----------------------------------------------------------------------------
-- CONSULTA 1 (Pregunta Analítica 1: Riesgo Global y Ratio NPL Real)
-- Subsanación feedback: Se calcula el NPL sobre saldo_pendiente en riesgo (>90 días)
-- Técnicas: Agregaciones (SUM, COUNT), CASE WHEN condicional, redondeo.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_creditos,
    SUM(monto_otorgado) AS cartera_total_colocada,
    SUM(saldo_pendiente) AS saldo_total_pendiente,
    SUM(CASE WHEN dias_atraso = 0 THEN saldo_pendiente ELSE 0 END) AS saldo_al_dia,
    SUM(CASE WHEN dias_atraso BETWEEN 1 AND 90 THEN saldo_pendiente ELSE 0 END) AS saldo_atrasado_temprano,
    SUM(CASE WHEN dias_atraso > 90 THEN saldo_pendiente ELSE 0 END) AS saldo_vencido_npl,
    ROUND((SUM(CASE WHEN dias_atraso > 90 THEN saldo_pendiente ELSE 0 END) / SUM(saldo_pendiente)) * 100, 2) AS npl_ratio_porcentaje
FROM fact_prestamos;


-- -----------------------------------------------------------------------------
-- CONSULTA 2 (Pregunta Analítica 2: Segmentación Laboral y Propensión a Mora > 30 días)
-- Subsanación feedback: Medición exacta de atrasos > 30 días cruzando con clientes
-- Técnicas: INNER JOIN (dim_clientes + fact_prestamos), GROUP BY, ORDER BY.
-- -----------------------------------------------------------------------------
SELECT 
    c.tipo_empleo,
    COUNT(p.id_prestamo) AS total_operaciones,
    ROUND(AVG(c.ingreso_mensual), 2) AS ingreso_promedio,
    ROUND(AVG(p.saldo_pendiente), 2) AS saldo_promedio,
    SUM(CASE WHEN p.dias_atraso > 30 THEN 1 ELSE 0 END) AS creditos_mora_critica,
    ROUND((SUM(CASE WHEN p.dias_atraso > 30 THEN 1 ELSE 0 END)::NUMERIC / COUNT(p.id_prestamo)) * 100, 2) AS tasa_propension_mora_pct
FROM dim_clientes c
INNER JOIN fact_prestamos p ON c.id_cliente = p.id_cliente
GROUP BY c.tipo_empleo
ORDER BY tasa_propension_mora_pct DESC;


-- -----------------------------------------------------------------------------
-- CONSULTA 3 (Pregunta Analítica 3: Concentración Territorial de Deuda Vencida)
-- Subsanación feedback: Deuda vencida cuantificada en dólares y no solo por conteo
-- Técnicas: Relación triple (JOIN cat_departamentos + dim_clientes + fact_prestamos),
--            GROUP BY, ORDER BY con límite.
-- -----------------------------------------------------------------------------
SELECT 
    d.nombre_departamento,
    d.zona_geografica,
    COUNT(p.id_prestamo) AS total_prestamos,
    ROUND(SUM(p.saldo_pendiente), 2) AS saldo_total_depto,
    ROUND(SUM(CASE WHEN p.dias_atraso > 0 THEN p.saldo_pendiente ELSE 0 END), 2) AS saldo_deuda_en_mora,
    ROUND(
        (SUM(CASE WHEN p.dias_atraso > 0 THEN p.saldo_pendiente ELSE 0 END) / 
        NULLIF(SUM(p.saldo_pendiente), 0)) * 100, 2
    ) AS pct_morosidad_departamental
FROM cat_departamentos d
INNER JOIN dim_clientes c ON d.id_departamento = c.id_departamento
INNER JOIN fact_prestamos p ON c.id_cliente = p.id_cliente
GROUP BY d.nombre_departamento, d.zona_geografica
ORDER BY saldo_deuda_en_mora DESC;


-- -----------------------------------------------------------------------------
-- CONSULTA 4 (Pregunta Analítica 4: Tasa de Cumplimiento y Efectividad de Pago)
-- Subsanación feedback: Se evalúa el porcentaje global recuperado y cuotas cubiertas
-- Técnicas: Agregaciones (SUM, AVG), operadores aritméticos, filtros WHERE.
-- -----------------------------------------------------------------------------
SELECT 
    p.plazo_meses,
    COUNT(p.id_prestamo) AS operaciones,
    ROUND(SUM(p.monto_otorgado), 2) AS capital_colocado,
    ROUND(SUM(p.monto_pagado), 2) AS total_recuperado,
    ROUND((SUM(p.monto_pagado) / SUM(p.monto_otorgado)) * 100, 2) AS tasa_recuperacion_capital_pct,
    ROUND(AVG(p.cuotas_amortizadas), 1) AS promedio_cuotas_pagadas,
    ROUND(AVG(p.cuota_programada), 2) AS cuota_promedio
FROM fact_prestamos p
GROUP BY p.plazo_meses
ORDER BY p.plazo_meses ASC;


-- -----------------------------------------------------------------------------
-- CONSULTA 5 (Pregunta Analítica 5: Estructura Contractual y Reincidencia de Impago)
-- Subsanación feedback: Uso de num_atrasos_historicos cruzado con tasa y plazo
-- Técnicas: CASE WHEN para rangos de tasa, AVG de atrasos históricos, GROUP BY.
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN p.tasa_interes < 15.0 THEN 'Tasa Baja (< 15%)'
        WHEN p.tasa_interes BETWEEN 15.0 AND 25.0 THEN 'Tasa Media (15% - 25%)'
        ELSE 'Tasa Alta (> 25%)'
    END AS rango_tasa_interes,
    COUNT(p.id_prestamo) AS cantidad_creditos,
    ROUND(AVG(p.dias_atraso), 1) AS dias_atraso_promedio,
    ROUND(AVG(p.num_atrasos_historicos), 2) AS media_reincidencias_historicas,
    SUM(CASE WHEN p.num_atrasos_historicos >= 3 THEN 1 ELSE 0 END) AS clientes_altamente_reincidentes
FROM fact_prestamos p
GROUP BY rango_tasa_interes
ORDER BY media_reincidencias_historicas DESC;