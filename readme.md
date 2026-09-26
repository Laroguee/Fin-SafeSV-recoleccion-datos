# FinSafe SV: Diagnóstico y Monitoreo del Riesgo Crediticio en El Salvador

**Bootcamp Data Analyst | Reto Integrador - Semana 1**

Repositorio oficial del proyecto integrador enfocado en el análisis descriptivo, diagnóstico y gestión preventiva de la cartera de crédito de consumo en El Salvador.

---

## Equipo de Trabajo e Integrantes
* **Luis Alejandro Ramos Ordoñez** - *Coordinación técnica, modelado relacional y consultas SQL*
* **Sara Elizabeth Panameño Calderon** - *Instrumentación, integración de Google Apps Script/Sheets y ETL inicial*
* **Manuel Enrique Romero Sánchez** - *Modelado dimensional en estrella, DAX y arquitectura en Power BI*
* **Elías Yoel Romero Sánchez** - *Análisis exploratorio de datos, scripts analíticos en Python y documentación*

---

## Instrumento de Recolección y Evidencia (Semana 1)
Para garantizar la captura estandarizada de variables y respetar la confidencialidad bancaria nacional, el instrumento se diseñó en dos niveles:

1. **Formulario Web Interactivo (Google Apps Script + Google Sheets):**
   * Aplicación web responsiva conectada en tiempo real mediante API a Google Sheets.
   * [Enlace al Formulario Web Activo](https://script.google.com/macros/s/AKfycbzPxTH7Y2RCx6EIV-7vGWFtoaA5L_9gXSczKpcRsLXrbEyEteBkmI5Ler-tE-YOYChziA/exec)
   * [Enlace a la Hoja de Cálculo en Google Sheets](https://docs.google.com/spreadsheets/d/1lPf5RWjdLP5lMhvUbIkL6PfCvJEhTliqGngXL5h8SbI/edit?usp=sharing)
2. **Conjunto de Datos Tabular (`/data`):**
   * Base de datos estructurada con 1,000 registros individuales que cubren 14 variables de control socioeconómico, contractual y de mora dentro de los 14 departamentos de El Salvador.
   * [Ver archivo crudo CSV](./data/FinSafe_SV_Datos_Credito-crudo.xlsx)

---

## Diccionario de Variables
| Variable | Tipo de Dato | Propósito Analítico |
| :--- | :--- | :--- |
| `id_prestamo` | Cualitativa Nominal | Identificador único del crédito (Clave) |
| `departamento` | Cualitativa Nominal | Distribución geográfica (14 departamentos de El Salvador) |
| `edad_cliente` | Cuantitativa Discreta | Segmentación etaria (18 a 75 años) |
| `tipo_empleo` | Cualitativa Nominal | Estabilidad de ingresos (Formal, Independiente, Jubilado) |
| `ingreso_mensual` | Cuantitativa Continua | Capacidad financiera del cliente (USD) |
| `monto_otorgado` | Cuantitativa Continua | Colocación crediticia pactada (USD) |
| `tasa_interes` | Cuantitativa Continua | Tasa anual activa aplicada (%) |
| `plazo_meses` | Cuantitativa Discreta | Plazo de amortización acordado (12 a 84 meses) |
| `cuota_programada`| Cuantitativa Continua | Valor de cuota mensual esperada (USD) |
| `monto_pagado` | Cuantitativa Continua | Amortización real acumulada a la fecha (USD) |
| `dias_atraso` | Cuantitativa Discreta | Días transcurridos sin pago registrado |
| `estado_credito` | Cualitativa Ordinal | Estatus de riesgo: *Al día*, *Atrasado*, *Vencido* |
| `fecha_desembolso`| Temporal | Fecha de origen del crédito (`AAAA-MM-DD`) |
| `fecha_ultimo_pago`| Temporal | Última amortización registrada (`AAAA-MM-DD`) |

---

## Cronograma de Ejecución (6 Semanas)
* **Semana 1 (21/09 - 27/09):** Definición metodológica, preguntas, variables e instrumento de recolección.
* **Semana 2 (28/09 - 04/10):** Recolección, curación y validación del dataset final (mínimo 1,000 registros).
* **Semana 3 (05/10 - 11/10):** Modelado DDL/DML, normalización y consultas analíticas en PostgreSQL.
* **Semana 4 (12/10 - 18/10):** Diseño del esquema en estrella, métricas analíticas y DAX en Power BI.
* **Semana 5 (19/10 - 25/10):** Dashboard interactivo de KPIs y prototipo analítico en Python.
* **Semana 6 (26/10 - 01/11):** Matriz de trazabilidad, hallazgos prescriptivos y sustentación final.