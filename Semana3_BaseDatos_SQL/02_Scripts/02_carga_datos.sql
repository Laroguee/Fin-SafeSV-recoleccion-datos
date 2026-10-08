-- =============================================================================
-- PROYECTO: FinSafe SV
-- ARCHIVO: 02_carga_datos.sql
-- DESCRIPCIÓN: Ingesta de datos limpios desde archivos CSV
-- =============================================================================

-- 1. Carga de Catálogo de Departamentos
\copy cat_departamentos(id_departamento, nombre_departamento, zona_geografica) FROM 'C:/ruta_de_tu_proyecto/03_Datos_Carga/cat_departamentos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- 2. Carga de Dimensión Clientes
\copy dim_clientes(id_cliente, id_departamento, edad_cliente, tipo_empleo, ingreso_mensual) FROM 'C:/ruta_de_tu_proyecto/03_Datos_Carga/dim_clientes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- 3. Carga de Hechos Préstamos
\copy fact_prestamos(id_prestamo, id_cliente, monto_otorgado, tasa_interes, plazo_meses, cuota_programada, monto_pagado, saldo_pendiente, dias_atraso, estado_credito, fecha_desembolso, fecha_ultimo_pago, num_atrasos_historicos, cuotas_amortizadas) FROM 'C:/ruta_de_tu_proyecto/03_Datos_Carga/fact_prestamos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');