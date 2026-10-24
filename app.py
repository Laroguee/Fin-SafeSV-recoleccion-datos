"""
=============================================================================
FinSafe SV: Diagnóstico y Monitoreo del Riesgo Crediticio en El Salvador
Entrega 5: Aplicación Web Interactiva en Streamlit (app.py)
=============================================================================
Paleta Oficial Corporativa FinSafe SV:
- Azul Marino:    #142D4E (Estructura y encabezados)
- Azul Principal: #287DB5 (Gráficos neutros y barras primarias)
- Verde Meta:     #23865B (Al día / Cumplimiento / Cartera sana)
- Ámbar Alerta:   #D99A24 (Mora temprana 1-90 días)
- Rojo Crítico:   #C43D42 (Mora crítica >90 días / NPL)
- Gris Claro:     #F3F6FA (Fondo UI / Tarjetas)
- Gris Texto:     #5E6B7A (Tipografía secundaria y ejes)
=============================================================================
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FinSafe SV · Diagnóstico y Monitoreo de Riesgo Crediticio",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #142D4E;
    }
    
    /* Fondo principal y estructura */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Header principal */
    .brand-header {
        background: linear-gradient(135deg, #142D4E 0%, #1e4575 100%);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(20, 45, 78, 0.12);
    }
    .brand-header h1 {
        margin: 0;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
    }
    .brand-header p {
        margin: 0.35rem 0 0 0;
        font-size: 0.95rem;
        color: #E2E8F0;
        font-weight: 500;
    }
    .header-badges {
        margin-top: 0.8rem;
        display: flex;
        gap: 0.7rem;
        flex-wrap: wrap;
    }
    .kpi-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
    }
    
    /* Tarjetas de KPI */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 2px 10px rgba(20, 45, 78, 0.05);
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(20, 45, 78, 0.09);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .card-blue::before { background-color: #287DB5; }
    .card-green::before { background-color: #23865B; }
    .card-amber::before { background-color: #D99A24; }
    .card-red::before { background-color: #C43D42; }

    .metric-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #5E6B7A;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #142D4E;
        line-height: 1.2;
    }
    .metric-subtext {
        font-size: 0.80rem;
        font-weight: 600;
        margin-top: 0.45rem;
    }
    .text-green { color: #23865B; }
    .text-amber { color: #D99A24; }
    .text-red { color: #C43D42; }
    .text-blue { color: #287DB5; }
    
    /* Tarjetas explicativas para cada gráfico */
    .chart-explain-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #287DB5;
        border-radius: 8px;
        padding: 0.9rem 1.15rem;
        margin-top: 0.75rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(20, 45, 78, 0.03);
    }
    .explain-header {
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #142D4E;
        margin-bottom: 0.35rem;
    }
    .explain-body {
        font-size: 0.84rem;
        color: #334155;
        line-height: 1.45;
    }
    .explain-insight {
        font-size: 0.84rem;
        color: #142D4E;
        line-height: 1.45;
        margin-top: 0.45rem;
        padding-top: 0.45rem;
        border-top: 1px dashed #CBD5E1;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F3F6FA;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #142D4E;
        margin-bottom: 0.5rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CARGA Y CACHÉ DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_datos():
    dir_actual = os.getcwd()
    dir_script = os.path.dirname(os.path.abspath(__file__))
    
    rutas_candidatas = [
        os.path.join(dir_script, "02_Datos", "dataset_limpio.csv"),
        os.path.join(dir_script, "..", "Semana5_Python", "02_Datos", "dataset_limpio.csv"),
        os.path.join(dir_script, "Semana5_Python", "02_Datos", "dataset_limpio.csv"),
        os.path.join(dir_actual, "Semana5_Python", "02_Datos", "dataset_limpio.csv"),
        os.path.join(dir_actual, "02_Datos", "dataset_limpio.csv"),
        os.path.join(dir_script, "dataset_limpio.csv"),
        os.path.join(dir_actual, "dataset_limpio.csv"),
        "dataset_limpio.csv"
    ]
    
    df = None
    for r in rutas_candidatas:
        if os.path.exists(r):
            try:
                df = pd.read_csv(r)
                break
            except Exception:
                pass
            
    if df is None:
        # Búsqueda dinámica de las tablas fuente para reconstruir al vuelo si fuera necesario
        def buscar_archivo(nombre):
            posibles = [
                os.path.join(dir_script, nombre),
                os.path.join(dir_actual, nombre),
                os.path.join(dir_script, "..", nombre),
                os.path.join(dir_script, "02_Datos", nombre),
                os.path.join(dir_actual, "Semana5_Python", "02_Datos", nombre),
                os.path.join(dir_actual, "Semana5_Python", nombre),
                nombre
            ]
            for p in posibles:
                if os.path.exists(p):
                    return p
            return nombre
            
        df_deptos = pd.read_csv(buscar_archivo('cat_departamentos.csv'))
        df_clientes = pd.read_csv(buscar_archivo('dim_clientes.csv'))
        df_prestamos = pd.read_csv(buscar_archivo('fact_prestamos.csv'))
        
        df = df_prestamos.merge(df_clientes, on='id_cliente').merge(df_deptos, on='id_departamento')
        
        # Transformación 1: Categoría de mora
        def asignar_categoria(dias):
            if dias == 0: return 'Al día'
            elif dias <= 30: return 'Mora Temprana (1-30 d)'
            elif dias <= 90: return 'Mora Media (31-90 d)'
            else: return 'Mora Crítica NPL (>90 d)'
            
        df['categoria_mora'] = df['dias_atraso'].apply(asignar_categoria)
        df['es_npl'] = (df['dias_atraso'] > 90).astype(int)
        df['es_mora_temprana'] = ((df['dias_atraso'] >= 1) & (df['dias_atraso'] <= 90)).astype(int)
        
        # Transformación 2: Ratio Cuota/Ingreso
        df['cuota_sobre_ingreso_pct'] = ((df['cuota_programada'] / df['ingreso_mensual']) * 100).round(2)
        def clasif_dti(d):
            if d < 20: return 'Sostenible (<20%)'
            elif d <= 40: return 'Moderado (20-40%)'
            else: return 'Crítico / Sobreendeudado (>40%)'
        df['nivel_endeudamiento'] = df['cuota_sobre_ingreso_pct'].apply(clasif_dti)
        
        # Transformación 3: Amortización y Exposición
        df['pct_amortizado'] = ((df['monto_pagado'] / df['monto_otorgado']) * 100).round(2)
        df['ratio_saldo_expuesto'] = (df['saldo_pendiente'] / df['monto_otorgado']).round(4)
        
    df['fecha_desembolso'] = pd.to_datetime(df['fecha_desembolso'], errors='coerce')
    df['fecha_ultimo_pago'] = pd.to_datetime(df['fecha_ultimo_pago'], errors='coerce')
    
    return df

df_full = cargar_datos()

# -----------------------------------------------------------------------------
# 3. SIDEBAR DE FILTROS REACTIVOS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛡️ FinSafe SV · Filtros</div>', unsafe_allow_html=True)
    st.caption("Ajusta los parámetros para recalcular dinámicamente los KPIs y la analítica.")
    
    # Filtro Zona Geográfica
    zonas_disponibles = ['Todas'] + sorted(df_full['zona_geografica'].unique().tolist())
    zona_sel = st.selectbox("Zona Geográfica:", zonas_disponibles, index=0)
    
    # Filtrar departamentos dependientes de la zona
    if zona_sel != 'Todas':
        deptos_filtrados = sorted(df_full[df_full['zona_geografica'] == zona_sel]['nombre_departamento'].unique().tolist())
    else:
        deptos_filtrados = sorted(df_full['nombre_departamento'].unique().tolist())
        
    deptos_sel = st.multiselect(
        "Departamento(s):",
        options=deptos_filtrados,
        default=deptos_filtrados,
        help="Selecciona uno o más departamentos salvadoreños."
    )
    
    # Filtro Tipo de Empleo
    empleos_unicos = sorted(df_full['tipo_empleo'].unique().tolist())
    empleo_sel = st.multiselect(
        "Tipo de Empleo:",
        options=empleos_unicos,
        default=empleos_unicos
    )
    
    # Filtro Estado de Crédito / Categoría
    estados_unicos = ['Al día', 'Atrasado', 'Vencido']
    estado_sel = st.multiselect(
        "Estado del Crédito:",
        options=estados_unicos,
        default=estados_unicos
    )
    
    # Filtro Días de Atraso (Slider)
    max_dias = int(df_full['dias_atraso'].max())
    dias_rango = st.slider(
        "Rango de Días de Atraso:",
        min_value=0,
        max_value=max_dias,
        value=(0, max_dias),
        step=1
    )
    
    # Filtro Rango de Monto Otorgado
    min_monto = float(df_full['monto_otorgado'].min())
    max_monto = float(df_full['monto_otorgado'].max())
    monto_rango = st.slider(
        "Monto Otorgado ($):",
        min_value=round(min_monto, -2),
        max_value=round(max_monto, -2),
        value=(round(min_monto, -2), round(max_monto, -2)),
        step=200.0
    )
    
    st.markdown("---")
    st.caption("FinSafe SV © 2026 · El Salvador\nSistemas de Alerta Temprana de Crédito.")

# -----------------------------------------------------------------------------
# 4. APLICACIÓN DE FILTROS AL DATAFRAME
# -----------------------------------------------------------------------------
df_filtrado = df_full[
    (df_full['nombre_departamento'].isin(deptos_sel)) &
    (df_full['tipo_empleo'].isin(empleo_sel)) &
    (df_full['estado_credito'].isin(estado_sel)) &
    (df_full['dias_atraso'] >= dias_rango[0]) &
    (df_full['dias_atraso'] <= dias_rango[1]) &
    (df_full['monto_otorgado'] >= monto_rango[0]) &
    (df_full['monto_otorgado'] <= monto_rango[1])
]

# -----------------------------------------------------------------------------
# 5. HEADER PRINCIPAL Y HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <h1>FinSafe SV · Monitoreo y Diagnóstico del Riesgo Crediticio</h1>
    <p>Cuadro de Mando Ejecutivo e Inteligencia Analítica de Cartera en El Salvador (Supervisión SSF / Basilea)</p>
    <div class="header-badges">
        <span class="kpi-badge">Modelo Relacional 3NF</span>
        <span class="kpi-badge">NPL Benchmark < 5.0%</span>
        <span class="kpi-badge">Corte: Agosto 2026</span>
        <span class="kpi-badge">14 Departamentos</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. CÁLCULO DE KPIS DINÁMICOS
# -----------------------------------------------------------------------------
total_ops = len(df_filtrado)
monto_colocado = df_filtrado['monto_otorgado'].sum() if total_ops > 0 else 0
monto_pagado = df_filtrado['monto_pagado'].sum() if total_ops > 0 else 0
saldo_vivo = df_filtrado['saldo_pendiente'].sum() if total_ops > 0 else 0

saldo_npl = df_filtrado[df_filtrado['dias_atraso'] > 90]['saldo_pendiente'].sum() if total_ops > 0 else 0
saldo_mora_temprana = df_filtrado[(df_filtrado['dias_atraso'] >= 1) & (df_filtrado['dias_atraso'] <= 90)]['saldo_pendiente'].sum() if total_ops > 0 else 0
saldo_al_dia = df_filtrado[df_filtrado['dias_atraso'] == 0]['saldo_pendiente'].sum() if total_ops > 0 else 0

npl_ratio = (saldo_npl / saldo_vivo * 100) if saldo_vivo > 0 else 0.0
mora_temprana_ratio = (saldo_mora_temprana / saldo_vivo * 100) if saldo_vivo > 0 else 0.0
recuperacion_ratio = (monto_pagado / monto_colocado * 100) if monto_colocado > 0 else 0.0

# -----------------------------------------------------------------------------
# 7. FILA DE TARJETAS DE KPIS
# -----------------------------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div class="metric-card card-blue">
        <div class="metric-title">Saldo Vivo Cartera</div>
        <div class="metric-value">${saldo_vivo/1e6:.2f}M</div>
        <div class="metric-subtext text-blue">{total_ops:,} operaciones activas</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    npl_color = "text-red" if npl_ratio > 5.0 else "text-green"
    st.markdown(f"""
    <div class="metric-card card-red">
        <div class="metric-title">NPL Ratio (>90 días)</div>
        <div class="metric-value {npl_color}">{npl_ratio:.2f}%</div>
        <div class="metric-subtext text-red">${saldo_npl:,.2f} en riesgo</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="metric-card card-amber">
        <div class="metric-title">Mora Temprana (1-90 d)</div>
        <div class="metric-value text-amber">{mora_temprana_ratio:.2f}%</div>
        <div class="metric-subtext text-amber">${saldo_mora_temprana:,.2f} observación</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="metric-card card-green">
        <div class="metric-title">Tasa Recuperación</div>
        <div class="metric-value text-green">{recuperacion_ratio:.2f}%</div>
        <div class="metric-subtext text-green">${monto_pagado/1e6:.2f}M recuperado</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    pct_cartera_sana = (saldo_al_dia / saldo_vivo * 100) if saldo_vivo > 0 else 0.0
    st.markdown(f"""
    <div class="metric-card card-green">
        <div class="metric-title">Cartera Al Día</div>
        <div class="metric-value text-green">{pct_cartera_sana:.1f}%</div>
        <div class="metric-subtext text-green">${saldo_al_dia/1e6:.2f}M sin mora</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if npl_ratio > 5.0:
    st.warning(
        f"⚠️ **Alerta de Riesgo Crediticio (NPL = {npl_ratio:.2f}%)**: El ratio de morosidad crítica sobrepasa "
        f"el umbral prudencial de referencia del 5.0% fijado por los estándares bancarios y la SSF. "
        f"Se recomienda intensificar las gestiones sobre los tramos de mora temprana para contener la migración a pérdida.",
        icon="🚨"
    )

# -----------------------------------------------------------------------------
# 8. PESTAÑAS ANALÍTICAS CON VISUALIZACIONES RICAS Y TEXTO EXPLICATIVO
# -----------------------------------------------------------------------------
tab_p1, tab_geo, tab_socio, tab_plazos, tab_datos = st.tabs([
    "📊 1. Estado General de Cartera (P1)",
    "📍 2. Diagnóstico Geográfico & Departamental (P2)",
    "👥 3. Perfil Sociodemográfico & Empleo (P3)",
    "⏳ 4. Plazos, Amortización & Curva de Recuperación (P4 & P5)",
    "📋 5. Tabla de Operaciones Sincronizada"
])

# Paleta corporativa para Plotly
COLOR_NAVY = "#142D4E"
COLOR_BLUE = "#287DB5"
COLOR_GREEN = "#23865B"
COLOR_AMBER = "#D99A24"
COLOR_RED = "#C43D42"
COLOR_GRAY_LIGHT = "#F3F6FA"
COLOR_GRAY_TEXT = "#5E6B7A"

# -----------------------------------------------------------------------------
# TAB 1: ESTADO GENERAL DE CARTERA (PREGUNTA 1)
# -----------------------------------------------------------------------------
with tab_p1:
    if total_ops == 0:
        st.info("No hay registros que coincidan con los filtros seleccionados.")
    else:
        st.markdown("### Diagnóstico Macro del Portafolio: Saldo y Operaciones por Estado")
        st.caption("Análisis exhaustivo de la composición de la cartera en riesgo según la norma prudencial SSF / Basilea.")
        
        col_p1_1, col_p1_2 = st.columns(2)
        
        # Gráfico 1.1: Distribución del Saldo Vivo por Estado
        with col_p1_1:
            st.markdown("#### Distribución del Saldo Vivo por Estado de Mora")
            
            saldo_estado_df = pd.DataFrame([
                {"Estado": "Al día (0 d)", "Saldo": saldo_al_dia, "Color": COLOR_GREEN},
                {"Estado": "Mora Temprana (1-90 d)", "Saldo": saldo_mora_temprana, "Color": COLOR_AMBER},
                {"Estado": "Mora Crítica NPL (>90 d)", "Saldo": saldo_npl, "Color": COLOR_RED}
            ])
            # Filtrar si no hay saldo en algún tramo
            saldo_estado_df = saldo_estado_df[saldo_estado_df['Saldo'] > 0]
            
            fig_p1_donut = px.pie(
                saldo_estado_df,
                names='Estado',
                values='Saldo',
                hole=0.55,
                color='Estado',
                color_discrete_map={
                    'Al día (0 d)': COLOR_GREEN,
                    'Mora Temprana (1-90 d)': COLOR_AMBER,
                    'Mora Crítica NPL (>90 d)': COLOR_RED
                }
            )
            fig_p1_donut.update_traces(
                textinfo='percent+label',
                hoverinfo='label+value+percent',
                textfont=dict(size=11, color='#FFFFFF', family='Plus Jakarta Sans'),
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_p1_donut.update_layout(
                annotations=[dict(text=f"<b>Saldo Vivo</b><br>${saldo_vivo/1e6:.2f}M", x=0.5, y=0.5, font_size=14, showarrow=False)],
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
                height=420,
                margin=dict(l=10, r=10, t=30, b=40),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_p1_donut, use_container_width=True)
            
            # Texto explicativo Gráfico 1.1
            st.markdown(f"""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Muestra la partición monetaria y porcentual del <b>Saldo Vivo Total (${saldo_vivo:,.2f})</b> en 
                    los tres estados crediticios fundamentales: <b>Cartera Sana al día</b> (0 días de atraso), 
                    <b>Mora Temprana</b> (1 a 90 días, en alerta y observación) y <b>Mora Crítica NPL</b> (>90 días, deterioro severo).
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> La cartera al día representa el <b>{pct_cartera_sana:.1f}%</b> (${saldo_al_dia:,.2f}). 
                    El capital en riesgo asciende a <b>${(saldo_mora_temprana + saldo_npl):,.2f} ({(mora_temprana_ratio + npl_ratio):.2f}%)</b>, 
                    donde la Mora Temprana (${saldo_mora_temprana:,.2f}) casi duplica a los créditos NPL (${saldo_npl:,.2f}), confirmando 
                    que la ventana óptima de recuperación preventiva se sitúa antes de los 90 días.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Gráfico 1.2: Conteo de Operaciones Crediticias
        with col_p1_2:
            st.markdown("#### Volumen de Operaciones Crediticias por Estado")
            
            conteo_ops = df_filtrado['estado_credito'].value_counts().reset_index()
            conteo_ops.columns = ['estado_credito', 'operaciones']
            conteo_ops['porcentaje'] = (conteo_ops['operaciones'] / total_ops * 100).round(1)
            
            orden_estados = ['Al día', 'Atrasado', 'Vencido']
            conteo_ops['orden'] = conteo_ops['estado_credito'].map(lambda x: orden_estados.index(x) if x in orden_estados else 99)
            conteo_ops = conteo_ops.sort_values(by='orden')
            
            fig_p1_bar = px.bar(
                conteo_ops,
                x='estado_credito',
                y='operaciones',
                color='estado_credito',
                color_discrete_map={
                    'Al día': COLOR_GREEN,
                    'Atrasado': COLOR_AMBER,
                    'Vencido': COLOR_RED
                },
                text=conteo_ops.apply(lambda r: f"{r['operaciones']} ops<br>({r['porcentaje']}%)", axis=1)
            )
            fig_p1_bar.update_traces(
                textposition='outside',
                cliponaxis=False,
                marker_line_color='#FFFFFF',
                marker_line_width=1.5
            )
            fig_p1_bar.update_layout(
                xaxis=dict(title="Estado Contractual del Crédito", color=COLOR_NAVY),
                yaxis=dict(title="Número de Operaciones", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0'),
                showlegend=False,
                height=420,
                margin=dict(l=10, r=10, t=30, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_p1_bar, use_container_width=True)
            
            # Texto explicativo Gráfico 1.2
            st.markdown(f"""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Cuantifica el número absoluto de <b>contratos de crédito activos ({total_ops:,} operaciones)</b> 
                    y su proporción relativa (%) según su condición operativa: <i>Al día</i>, <i>Atrasado</i> (mora preventiva) 
                    y <i>Vencido</i> (morosidad judicial o castigo).
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> De las {total_ops:,} operaciones analizadas, 
                    <b>{conteo_ops[conteo_ops['estado_credito']=='Al día']['operaciones'].sum() if 'Al día' in conteo_ops['estado_credito'].values else 0} créditos ({conteo_ops[conteo_ops['estado_credito']=='Al día']['porcentaje'].sum() if 'Al día' in conteo_ops['estado_credito'].values else 0}%)</b> 
                    están al corriente, mientras que <b>{conteo_ops[conteo_ops['estado_credito']!='Al día']['operaciones'].sum()} clientes</b> 
                    requieren acción de cobranza (gestión telefónica para los atrasados y recuperación especializada para los vencidos).
                </div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: DIAGNÓSTICO GEOGRÁFICO & DEPARTAMENTAL (PREGUNTA 2)
# -----------------------------------------------------------------------------
with tab_geo:
    if total_ops == 0:
        st.info("No hay registros que coincidan con los filtros seleccionados.")
    else:
        st.markdown("### Distribución Territorial y Concentración de Riesgo por Departamento")
        st.caption("Evaluación de la dispersión de cartera en las 4 zonas y 14 departamentos salvadoreños.")
        
        col_g1, col_g2 = st.columns([1.6, 1.4])
        
        depto_agg = df_filtrado.groupby(['nombre_departamento', 'zona_geografica']).agg(
            saldo_total=('saldo_pendiente', 'sum'),
            saldo_npl=('saldo_pendiente', lambda x: x[df_filtrado.loc[x.index, 'dias_atraso'] > 90].sum()),
            creditos=('id_prestamo', 'count')
        ).reset_index()
        
        depto_agg['npl_ratio'] = (depto_agg['saldo_npl'] / depto_agg['saldo_total'] * 100).fillna(0)
        depto_agg = depto_agg.sort_values(by='saldo_total', ascending=True)
        
        with col_g1:
            st.markdown("#### Saldo Vivo y NPL Ratio por Departamento")
            fig_depto = go.Figure()
            
            fig_depto.add_trace(go.Bar(
                y=depto_agg['nombre_departamento'],
                x=depto_agg['saldo_total'],
                name='Saldo Vivo ($)',
                orientation='h',
                marker=dict(color=COLOR_BLUE, opacity=0.9),
                text=[f"${v/1e3:,.1f}K" for v in depto_agg['saldo_total']],
                textposition='auto',
                hovertemplate="<b>%{y}</b><br>Saldo Vivo: $%{x:,.2f}<extra></extra>"
            ))
            
            fig_depto.add_trace(go.Scatter(
                y=depto_agg['nombre_departamento'],
                x=depto_agg['npl_ratio'],
                name='NPL Ratio (%)',
                xaxis='x2',
                mode='lines+markers',
                marker=dict(color=COLOR_RED, size=9, symbol='diamond'),
                line=dict(color=COLOR_RED, width=2.5, dash='dot'),
                hovertemplate="<b>%{y}</b><br>NPL Ratio: %{x:.2f}%<extra></extra>"
            ))
            
            fig_depto.update_layout(
                xaxis=dict(title="Saldo Vivo Pendiente ($)", color=COLOR_GRAY_TEXT, showgrid=True, gridcolor='#E2E8F0'),
                xaxis2=dict(
                    title="NPL Ratio (%)",
                    overlaying='x',
                    side='top',
                    color=COLOR_RED,
                    showgrid=False,
                    ticksuffix="%"
                ),
                yaxis=dict(color=COLOR_NAVY, automargin=True),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                height=480,
                margin=dict(l=10, r=10, t=40, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_depto, use_container_width=True)
            
            # Texto explicativo Gráfico 2.1
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Cruza el <b>volumen de capital expuesto</b> (barras azules en $) con el 
                    <b>ratio de morosidad crítica NPL</b> (línea roja discontinua con rombos en %) para cada 
                    departamento, permitiendo identificar plazas de alto volumen y aquellas de alto riesgo relativo.
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> <b>San Salvador</b> ($801.5K, NPL 11.60%) y <b>La Libertad</b> ($528.9K, NPL 11.33%) 
                    concentran más del 51% del saldo nacional con ratios de morosidad que superan ampliamente el límite prudencial del 5.0%. 
                    En contraste, <b>Santa Ana</b> ($289.6K) presenta un perfil defensivo con un NPL de solo 6.43%.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_g2:
            st.markdown("#### Concentración del Saldo Vivo por Zona")
            zona_agg = df_filtrado.groupby('zona_geografica').agg(
                saldo_total=('saldo_pendiente', 'sum'),
                saldo_npl=('saldo_pendiente', lambda x: x[df_filtrado.loc[x.index, 'dias_atraso'] > 90].sum()),
                creditos=('id_prestamo', 'count')
            ).reset_index()
            zona_agg['npl_ratio'] = (zona_agg['saldo_npl'] / zona_agg['saldo_total'] * 100).fillna(0)
            
            fig_zona = px.pie(
                zona_agg,
                names='zona_geografica',
                values='saldo_total',
                hole=0.55,
                color='zona_geografica',
                color_discrete_map={
                    'Central': COLOR_NAVY,
                    'Occidental': COLOR_BLUE,
                    'Oriental': COLOR_AMBER,
                    'Paracentral': COLOR_RED
                }
            )
            fig_zona.update_traces(
                textinfo='percent+label',
                hoverinfo='label+value+percent',
                textfont=dict(size=12, color='#FFFFFF', family='Plus Jakarta Sans'),
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_zona.update_layout(
                annotations=[dict(text=f"<b>Total</b><br>${saldo_vivo/1e6:.2f}M", x=0.5, y=0.5, font_size=15, showarrow=False)],
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                height=480,
                margin=dict(l=10, r=10, t=40, b=50),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_zona, use_container_width=True)
            
            # Texto explicativo Gráfico 2.2
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Muestra la distribución macro-regional del saldo vivo nacional entre las 4 zonas geográficas de El Salvador 
                    (Central, Occidental, Oriental y Paracentral) para evaluar la diversificación territorial de FinSafe SV.
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> La <b>Zona Central</b> absorbe el <b>58.3%</b> de la cartera nacional ($1.50M). 
                    Sin embargo, la <b>Zona Paracentral</b> exhibe el ratio NPL más crítico del país (12.11%), demandando un 
                    ajuste en los criterios de aprobación crediticia en dicha región.
                </div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: PERFIL SOCIODEMOGRÁFICO & EMPLEO (PREGUNTA 3)
# -----------------------------------------------------------------------------
with tab_socio:
    if total_ops == 0:
        st.info("No hay registros que coincidan con los filtros seleccionados.")
    else:
        st.markdown("### Perfil Laboral, Capacidad de Pago y Vulnerabilidad de Crédito")
        st.caption("Análisis de la estabilidad del deudor, carga financiera (DTI) y capacidad predictiva del historial.")
        
        col_s1, col_s2 = st.columns([1.5, 1.5])
        
        with col_s1:
            st.markdown("#### Matriz: Tipo de Empleo vs. Nivel de Endeudamiento (DTI)")
            
            crosstab_saldo = df_filtrado.pivot_table(
                index='tipo_empleo',
                columns='nivel_endeudamiento',
                values='saldo_pendiente',
                aggfunc='sum',
                fill_value=0
            )
            orden_cols = ['Sostenible (<20%)', 'Moderado (20-40%)', 'Crítico / Sobreendeudado (>40%)']
            cols_presentes = [c for c in orden_cols if c in crosstab_saldo.columns]
            crosstab_saldo = crosstab_saldo[cols_presentes]
            
            fig_bar_emp = go.Figure()
            colores_endeudamiento = {
                'Sostenible (<20%)': COLOR_GREEN,
                'Moderado (20-40%)': COLOR_AMBER,
                'Crítico / Sobreendeudado (>40%)': COLOR_RED
            }
            
            for col in cols_presentes:
                fig_bar_emp.add_trace(go.Bar(
                    name=col,
                    x=crosstab_saldo.index,
                    y=crosstab_saldo[col],
                    marker_color=colores_endeudamiento.get(col, COLOR_BLUE),
                    text=[f"${v/1e3:,.1f}K" if v > 0 else "" for v in crosstab_saldo[col]],
                    textposition='inside'
                ))
                
            fig_bar_emp.update_layout(
                barmode='stack',
                xaxis=dict(title="Tipo de Empleo", color=COLOR_NAVY),
                yaxis=dict(title="Saldo Pendiente Acumulado ($)", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0'),
                legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
                height=450,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar_emp, use_container_width=True)
            
            # Texto explicativo Gráfico 3.1
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Distribuye el saldo vivo por <b>tipo de empleo</b> (Formal, Independiente, Jubilado) apilado según el 
                    <b>ratio de endeudamiento DTI (Cuota / Ingreso)</b> en tres rangos: Sostenible (<20%), Moderado (20-40%) y Crítico (>40%).
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> Los clientes <b>Formales</b> concentran la mayor masa monetaria ($1.72M), pero 
                    los <b>Independientes</b> registran la mayor propensión a mora temprana (20.20%) debido a ingresos variables. 
                    Los <b>Jubilados</b> exhiben el menor riesgo relativo (NPL 8.97%) y cuotas contenidas dentro de rangos sostenibles.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            st.markdown("#### Predictibilidad: Atrasos Históricos Previos vs. Estado Actual")
            
            fig_box = px.box(
                df_filtrado,
                x='estado_credito',
                y='num_atrasos_historicos',
                color='estado_credito',
                color_discrete_map={
                    'Al día': COLOR_GREEN,
                    'Atrasado': COLOR_AMBER,
                    'Vencido': COLOR_RED
                },
                points='all',
                category_orders={'estado_credito': ['Al día', 'Atrasado', 'Vencido']}
            )
            fig_box.update_layout(
                xaxis=dict(title="Estado Actual del Crédito", color=COLOR_NAVY),
                yaxis=dict(title="Número de Atrasos Históricos Previos", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0'),
                showlegend=False,
                height=450,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
            # Texto explicativo Gráfico 3.2
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Evalúa la capacidad predictiva de la variable <code>num_atrasos_historicos</code> sobre el desenlace del crédito. 
                    Muestra los cuartiles, medianas y puntos individuales de dispersión para cada estado de la cartera.
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> La reincidencia es el mejor indicador de alerta temprana: los clientes <b>Vencidos</b> 
                    promedian <b>3.39 atrasos históricos previos</b> (con un máximo de 5), frente a solo <b>0.15</b> en cartera sana 
                    al día. Tener 2 o más atrasos previos multiplica por 4.8 la probabilidad de impago final.
                </div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 4: PLAZOS, AMORTIZACIÓN & RECUPERACIÓN (PREGUNTA 4 & 5)
# -----------------------------------------------------------------------------
with tab_plazos:
    if total_ops == 0:
        st.info("No hay registros que coincidan con los filtros seleccionados.")
    else:
        st.markdown("### Dinámica Temporal de Cartera: Plazos, Recuperación y Capacidad de Pago")
        st.caption("Comportamiento del flujo de caja, amortización acumulada y detección de sobreendeudamiento.")
        
        col_p1, col_p2 = st.columns([1.5, 1.5])
        
        with col_p1:
            st.markdown("#### Recuperación de Capital (%) vs. NPL Ratio (%) por Plazo")
            plazo_agg = df_filtrado.groupby('plazo_meses').agg(
                monto_otorgado=('monto_otorgado', 'sum'),
                monto_pagado=('monto_pagado', 'sum'),
                saldo_pendiente=('saldo_pendiente', 'sum'),
                saldo_npl=('saldo_pendiente', lambda x: x[df_filtrado.loc[x.index, 'dias_atraso'] > 90].sum())
            ).reset_index()
            
            plazo_agg['recuperacion_pct'] = (plazo_agg['monto_pagado'] / plazo_agg['monto_otorgado'] * 100).fillna(0)
            plazo_agg['npl_ratio_pct'] = (plazo_agg['saldo_npl'] / plazo_agg['saldo_pendiente'] * 100).fillna(0)
            plazo_agg = plazo_agg.sort_values(by='plazo_meses')
            
            fig_plazo = go.Figure()
            
            fig_plazo.add_trace(go.Bar(
                x=[f"{p}m" for p in plazo_agg['plazo_meses']],
                y=plazo_agg['recuperacion_pct'],
                name='Recuperación (%)',
                marker_color=COLOR_GREEN,
                text=[f"{v:.1f}%" for v in plazo_agg['recuperacion_pct']],
                textposition='auto',
                hovertemplate="Plazo: %{x}<br>Recuperación: %{y:.2f}%<extra></extra>"
            ))
            
            fig_plazo.add_trace(go.Scatter(
                x=[f"{p}m" for p in plazo_agg['plazo_meses']],
                y=plazo_agg['npl_ratio_pct'],
                name='NPL Ratio (%)',
                mode='lines+markers',
                marker=dict(color=COLOR_RED, size=9),
                line=dict(color=COLOR_RED, width=3),
                hovertemplate="Plazo: %{x}<br>NPL Ratio: %{y:.2f}%<extra></extra>"
            ))
            
            fig_plazo.update_layout(
                xaxis=dict(title="Plazo Original de la Operación (Meses)", color=COLOR_NAVY),
                yaxis=dict(title="Porcentaje (%)", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0', ticksuffix="%"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                height=450,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_plazo, use_container_width=True)
            
            # Texto explicativo Gráfico 4.1
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Contrasta la <b>Tasa de Recuperación de Capital</b> (barras verdes, % amortizado del monto colocado) frente 
                    al <b>NPL Ratio</b> (línea roja, % de saldo vencido) a lo largo de cada uno de los plazos crediticios (6 a 84 meses).
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> Los plazos cortos (6 a 18 meses) exhiben un alto deterioro NPL (13.7% - 14.4%) 
                    debido a cuotas mensuales muy elevadas. La <i>"zona dorada"</i> se ubica entre <b>24 y 48 meses</b>, con los 
                    menores niveles de morosidad (4.5% - 6.5%). Plazos superiores a 72 meses mejoran la amortización acumulada pero sufren fatiga de pago (NPL 12.3%).
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("#### Dispersión: Cuota Programada vs. Ingreso Mensual")
            fig_scatter = px.scatter(
                df_filtrado,
                x='ingreso_mensual',
                y='cuota_programada',
                color='categoria_mora',
                size='saldo_pendiente',
                color_discrete_map={
                    'Al día': COLOR_GREEN,
                    'Mora Temprana (1-30 d)': COLOR_BLUE,
                    'Mora Media (31-90 d)': COLOR_AMBER,
                    'Mora Crítica NPL (>90 d)': COLOR_RED
                },
                hover_data=['id_prestamo', 'id_cliente', 'dias_atraso', 'nombre_departamento'],
                labels={
                    'ingreso_mensual': 'Ingreso Mensual ($)',
                    'cuota_programada': 'Cuota Programada ($)',
                    'categoria_mora': 'Categoría de Mora'
                }
            )
            fig_scatter.update_layout(
                xaxis=dict(title="Ingreso Mensual del Cliente ($)", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0'),
                yaxis=dict(title="Cuota Programada ($)", color=COLOR_GRAY_TEXT, gridcolor='#E2E8F0'),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                height=450,
                margin=dict(l=10, r=10, t=30, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Texto explicativo Gráfico 4.2
            st.markdown("""
            <div class="chart-explain-card">
                <div class="explain-header">🎯 ¿Qué busca representar este gráfico?</div>
                <div class="explain-body">
                    Plotea a cada prestatario individual en el plano <b>Ingreso Mensual vs. Cuota Programada</b>, 
                    coloreado por su <b>Categoría Regulatoria de Mora</b> y con tamaño de burbuja proporcional a su saldo pendiente.
                </div>
                <div class="explain-insight">
                    💡 <b>Hallazgo Clave:</b> Permite visualizar el sobreendeudamiento estructural: los clientes con cuotas 
                    que superan el 40% de su ingreso mensual presentan una concentración significativamente mayor de puntos rojos 
                    (NPL) y ámbar (mora temprana), lo que justifica implementar un tope rígido de DTI en las políticas de originación.
                </div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 5: TABLA DE OPERACIONES SINCRONIZADA
# -----------------------------------------------------------------------------
with tab_datos:
    st.markdown("### Registro Detallado de Operaciones Filtradas")
    st.caption("Esta tabla refleja en tiempo real las operaciones filtradas en la barra lateral.")
    
    busqueda = st.text_input("🔍 Buscar por ID Préstamo o ID Cliente:", placeholder="Ej: PREST-00013 o CLI-00022")
    
    df_tabla = df_filtrado.copy()
    if busqueda:
        df_tabla = df_tabla[
            df_tabla['id_prestamo'].str.contains(busqueda, case=False, na=False) |
            df_tabla['id_cliente'].str.contains(busqueda, case=False, na=False)
        ]
        
    columnas_mostrar = [
        'id_prestamo', 'id_cliente', 'nombre_departamento', 'zona_geografica',
        'tipo_empleo', 'ingreso_mensual', 'monto_otorgado', 'saldo_pendiente',
        'cuota_programada', 'plazo_meses', 'dias_atraso', 'estado_credito',
        'categoria_mora', 'cuota_sobre_ingreso_pct', 'pct_amortizado'
    ]
    
    df_presentacion = df_tabla[columnas_mostrar].copy()
    df_presentacion.columns = [
        'ID Préstamo', 'ID Cliente', 'Departamento', 'Zona',
        'Empleo', 'Ingreso ($)', 'Otorgado ($)', 'Saldo Pendiente ($)',
        'Cuota ($)', 'Plazo (m)', 'Días Atraso', 'Estado',
        'Categoría Mora', 'DTI (%)', 'Amortizado (%)'
    ]
    
    st.dataframe(
        df_presentacion.style.format({
            'Ingreso ($)': '${:,.2f}',
            'Otorgado ($)': '${:,.2f}',
            'Saldo Pendiente ($)': '${:,.2f}',
            'Cuota ($)': '${:,.2f}',
            'DTI (%)': '{:.1f}%',
            'Amortizado (%)': '{:.1f}%'
        }),
        height=380,
        use_container_width=True
    )
    
    csv_bytes = df_tabla.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Operaciones Filtradas (CSV)",
        data=csv_bytes,
        file_name="FinSafe_SV_Operaciones_Filtradas.csv",
        mime="text/csv"
    )
