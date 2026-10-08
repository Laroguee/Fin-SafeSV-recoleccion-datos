-- =============================================================================
-- PROYECTO: FinSafe SV - Diagnóstico y Monitoreo del Riesgo Crediticio
-- ARCHIVO: 01_creacion_bd.sql
-- DESCRIPCIÓN: Definición de estructura física (DDL), PKs, FKs y restricciones CHECK
-- =============================================================================

-- 1. Limpieza preventiva en cascada
DROP TABLE IF EXISTS fact_prestamos CASCADE;
DROP TABLE IF EXISTS dim_clientes CASCADE;
DROP TABLE IF EXISTS cat_departamentos CASCADE;

-- 2. Creación de Tabla Catálogo: Departamentos
CREATE TABLE cat_departamentos (
    id_departamento INT PRIMARY KEY,
    nombre_departamento VARCHAR(50) NOT NULL UNIQUE,
    zona_geografica VARCHAR(30) NOT NULL
);

-- 3. Creación de Tabla Dimensión: Clientes
CREATE TABLE dim_clientes (
    id_cliente VARCHAR(15) PRIMARY KEY,
    id_departamento INT NOT NULL,
    edad_cliente INT NOT NULL CHECK (edad_cliente >= 18),
    tipo_empleo VARCHAR(30) NOT NULL CHECK (tipo_empleo IN ('Formal', 'Independiente', 'Jubilado')),
    ingreso_mensual NUMERIC(10,2) NOT NULL CHECK (ingreso_mensual > 0),
    CONSTRAINT fk_cliente_departamento 
        FOREIGN KEY (id_departamento) 
        REFERENCES cat_departamentos (id_departamento) 
        ON DELETE RESTRICT
);

-- 4. Creación de Tabla de Hechos: Préstamos
CREATE TABLE fact_prestamos (
    id_prestamo VARCHAR(15) PRIMARY KEY,
    id_cliente VARCHAR(15) NOT NULL,
    monto_otorgado NUMERIC(10,2) NOT NULL CHECK (monto_otorgado > 0),
    tasa_interes NUMERIC(5,2) NOT NULL CHECK (tasa_interes > 0),
    plazo_meses INT NOT NULL CHECK (plazo_meses > 0),
    cuota_programada NUMERIC(10,2) NOT NULL CHECK (cuota_programada > 0),
    monto_pagado NUMERIC(10,2) NOT NULL CHECK (monto_pagado >= 0),
    saldo_pendiente NUMERIC(10,2) NOT NULL CHECK (saldo_pendiente >= 0),
    dias_atraso INT NOT NULL DEFAULT 0 CHECK (dias_atraso >= 0),
    estado_credito VARCHAR(20) NOT NULL CHECK (estado_credito IN ('Al día', 'Atrasado', 'Vencido')),
    fecha_desembolso DATE NOT NULL,
    fecha_ultimo_pago DATE NOT NULL,
    num_atrasos_historicos INT NOT NULL DEFAULT 0 CHECK (num_atrasos_historicos >= 0),
    cuotas_amortizadas INT NOT NULL DEFAULT 0 CHECK (cuotas_amortizadas >= 0),
    CONSTRAINT fk_prestamo_cliente 
        FOREIGN KEY (id_cliente) 
        REFERENCES dim_clientes (id_cliente) 
        ON DELETE CASCADE,
    CONSTRAINT chk_fechas_cronologia 
        CHECK (fecha_ultimo_pago >= fecha_desembolso)
);