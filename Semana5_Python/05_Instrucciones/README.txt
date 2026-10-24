===============================================================================
FINSAFE SV: DIAGNÓSTICO Y MONITOREO DEL RIESGO CREDITICIO EN EL SALVADOR
ENTREGA 5: PYTHON Y APLICACIÓN INTERACTIVA
BOOTCAMP DATA ANALYST - COHORTE 2026
===============================================================================

1. DESCRIPCIÓN DEL PROYECTO
-------------------------------------------------------------------------------
FinSafe SV es una solución analítica integral diseñada para el diagnóstico,
monitoreo y gestión preventiva del riesgo crediticio de una cartera de 1,000
operaciones financieras en El Salvador, distribuida a lo largo de sus 14
departamentos y 4 zonas geográficas.

La entrega combina:
- Un pipeline de ingestión y consolidación relacional 3NF en Pandas.
- La implementación y justificación financiera de 3 transformaciones de datos.
- Un cuaderno autoejecutable en Google Colab con ipywidgets interactivos
  organizados en 3 pestañas (Gerencial, Operativo y Analítico).
- Una aplicación web reactiva en Streamlit (app.py) lista para despliegue local
  o en la nube (Streamlit Community Cloud), con la paleta de colores corporativa
  estricta de FinSafe SV.
- Un reporte ejecutivo en PDF (Reporte_Semana_5.pdf).


2. ESTRUCTURA DE LA ENTREGA
-------------------------------------------------------------------------------
Semana5_Python/
│
├── 01_Notebook/
│   └── Analisis_Interactivo_FinSafe_SV.ipynb
│       (Cuaderno Jupyter / Colab con Markdown explicativo, validación de KPIs,
│        análisis de las 5 preguntas del negocio y 3 pestañas con ipywidgets)
│
├── 02_Datos/
│   └── dataset_limpio.csv
│       (Consolidado de fact_prestamos + dim_clientes + cat_departamentos con
│        las 3 transformaciones calculadas: 1,000 filas × 29 columnas)
│
├── 03_Evidencias/
│   └── capturas_interaccion/
│       (Capturas y evidencias gráficas de la interactividad de la app y notebook)
│
├── 04_Reporte/
│   └── Reporte_Semana_5.pdf
│       (Reporte ejecutivo formal con resumen de KPIs, transformaciones y
│        recomendaciones de comités de crédito)
│
├── 05_Instrucciones/
│   └── README.txt
│       (Este archivo de instrucciones técnicas y guía de despliegue)
│
└── app.py
    (Aplicación Web interactiva en Streamlit con filtros reactivos, métricas
     dinámicas, visualizaciones Plotly y tabla filtrada descargable en CSV)


3. REQUISITOS DEL SISTEMA Y DEPENDENCIAS
-------------------------------------------------------------------------------
Entorno recomendado: Python 3.10, 3.11 o 3.12.

Librerías requeridas (instalar vía pip):
    pip install pandas numpy matplotlib seaborn plotly streamlit ipywidgets openpyxl reportlab


4. GUÍA DE EJECUCIÓN PASO A PASO
-------------------------------------------------------------------------------
A) EJECUCIÓN DEL CUADERNO EN GOOGLE COLAB / LOCAL:
   1. Subir el archivo 'Analisis_Interactivo_FinSafe_SV.ipynb' a Google Colab
      (o abrirlo en VSCode / JupyterLab local).
   2. Asegurarse de tener 'dataset_limpio.csv' o los 3 CSVs base en el mismo
      directorio de trabajo o en la raíz del entorno Colab.
   3. Ejecutar las celdas secuencialmente (Run All).
   4. En la celda 7, interactuar con el widget de 3 pestañas:
      - Pestaña 1: Visión Gerencial (filtro por Zona).
      - Pestaña 2: Control Operativo (slider de Días de Atraso).
      - Pestaña 3: Diagnóstico Analítico (selector múltiple de Tipo de Empleo).

B) EJECUCIÓN DE LA APLICACIÓN WEB STREAMLIT (LOCAL):
   1. Abrir una terminal o consola de comandos en la carpeta raíz del proyecto.
   2. Ejecutar:
          streamlit run app.py
   3. El navegador abrirá automáticamente la URL local:
          http://localhost:8501
   4. Utilizar la barra lateral (sidebar) para filtrar por Departamento, Zona,
      Tipo de Empleo, Estado de Crédito o Días de Atraso.
   5. Observar el recálculo instantáneo de las 5 tarjetas de KPI y los gráficos
      interactivos de Plotly.
   6. Descargar el subconjunto de datos filtrados mediante el botón inferior
      "Descargar Operaciones Filtradas (CSV)".

C) DESPLIEGUE EN STREAMLIT COMMUNITY CLOUD:
   1. Subir el repositorio a GitHub (ej. github.com/usuario/FinSafe_SV).
   2. Iniciar sesión en https://share.streamlit.io con cuenta de GitHub.
   3. Seleccionar el repositorio, rama 'main' y archivo principal 'app.py'.
   4. Presionar 'Deploy'. El dashboard quedará publicado con URL pública https.


5. PALETA CORPORATIVA OFICIAL UTILIZADA
-------------------------------------------------------------------------------
- Azul Marino:    #142D4E (Encabezados, títulos y estructura)
- Azul Principal: #287DB5 (Gráficos neutros y barras principales)
- Verde:          #23865B (Cartera Al día / Metas cumplidas)
- Ámbar:          #D99A24 (Mora Temprana / Alerta preventiva 1-90 días)
- Rojo:           #C43D42 (Mora Crítica NPL / Alerta severa >90 días)
- Gris Claro:     #F3F6FA (Fondo UI y tarjetas de métricas)
- Gris Texto:     #5E6B7A (Tipografía secundaria y líneas de cuadrícula)


6. RESUMEN DE LAS 3 TRANSFORMACIONES EN PANDAS
-------------------------------------------------------------------------------
1. 'categoria_mora':
   Segmentación regulatoria SSF en 4 tramos: Al día (0 d), Mora Temprana
   (1-30 d), Mora Media (31-90 d) y Mora Crítica NPL (>90 d).
2. 'cuota_sobre_ingreso_pct' y 'nivel_endeudamiento':
   Ratio de esfuerzo financiero (DTI) clasificado en Sostenible (<20%),
   Moderado (20-40%) y Crítico (>40%).
3. 'pct_amortizado' y 'ratio_saldo_expuesto':
   Porcentaje de capital recuperado y ratio de exposición al default (EAD)
   para cuantificar la severidad de pérdida (LGD).


7. CUADRATURA DE KPIS VALIDADOS CONTRA SQL / POWER BI
-------------------------------------------------------------------------------
- Monto Colocado Total:          $4,252,634.79 (~$4.25M)
- Monto Recuperado (Pagado):     $1,674,017.00 (~$1.67M)
- Saldo Vivo Total de Cartera:   $2,578,617.79 (~$2.58M)
- Tasa de Recuperación Global:   39.36%
- Saldo en Mora Crítica (NPL):   $255,530.17 (9.91% del saldo vivo)
- Saldo en Mora Temprana:        $479,624.03 (18.60% del saldo vivo)
- Saldo en Cartera Al Día:       $1,843,463.59 (71.49% del saldo vivo)
===============================================================================
FinSafe SV © 2026 · Diagnóstico y Monitoreo del Riesgo Crediticio · El Salvador
===============================================================================
