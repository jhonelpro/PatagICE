import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import re

# Configuración de página con tema patagónico
st.set_page_config(
    page_title="Patag-ICE - Explorador Patagónico",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏔️"
)

# CSS personalizado inspirado en la Patagonia
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(180deg, 
            #e8f4fd 0%, #f0f8ff 30%, #f8f9fa 70%, #e3f2fd 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
        border-right: 3px solid #0ea5e9;
    }

    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.4);
        margin: 15px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }

    .status-verde {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .status-amarillo {
        background: linear-gradient(135deg, #d97706 0%, #f59e0b 50%, #fbbf24 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(217, 119, 6, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .status-rojo {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 50%, #f87171 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(220, 38, 38, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .patagonia-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #475569 75%, #64748b 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 25px;
        margin-bottom: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .patagonia-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: aurora 3s infinite;
    }

    @keyframes aurora {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .patagonia-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    .patagonia-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }

    .js-plotly-plot {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .patagonia-footer {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-top: 40px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .floating-icon {
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .highlight-text {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="patagonia-header">
    <h1><span class="floating-icon">🏔️</span> Patag-ICE: Explorador Patagónico</h1>
    <p>Tu guía inteligente para el <span class="highlight-text">Parque Nacional Laguna San Rafael</span></p>
    <p style="font-size: 0.9rem; margin-top: 15px; opacity: 0.8;">
         🛰️ Tecnología satelital • 🔬 Análisis predictivo
    </p>
</div>
""", unsafe_allow_html=True)

# Function definitions in correct order
def cargar_datos():
    try:
        # Cargar datos de icebergs
        iceberg_df = pd.read_csv("predicciones_icebergs_ridge.csv")[['Fecha', 'Area_Predicha_km2']]
        iceberg_df = iceberg_df.rename(columns={'Area_Predicha_km2': 'Area_km2'})
        iceberg_df['Fecha'] = pd.to_datetime(iceberg_df['Fecha']).dt.date
        iceberg_df = iceberg_df[iceberg_df['Fecha'] >= pd.to_datetime('2025-06-07').date()]

        # Cargar datos de agua
        water_df = pd.read_csv("water_regression_results_jun_jul_2025.csv")[['Fecha', 'Area_km2']]
        water_df['Fecha'] = pd.to_datetime(water_df['Fecha']).dt.date
        water_df = water_df[water_df['Fecha'] >= pd.to_datetime('2025-06-07').date()]

        return iceberg_df, water_df
    except FileNotFoundError as e:
        st.error(f"❌ Error: No se encontraron los archivos de datos ({e})")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error inesperado al cargar datos: {e}")
        st.stop()

def obtener_valor_actual(df, fecha_actual, columna):
    valores = df[df['Fecha'] <= fecha_actual]
    if not valores.empty:
        return valores.iloc[-1][columna]
    else:
        return df.iloc[-1][columna] if not df.empty else 0  # Fallback to most recent

def obtener_prediccion_diaria(df, columna, valor_default):
    fecha_hoy = datetime.now().date()
    resultado = df.loc[df['Fecha'] == fecha_hoy, columna]
    return resultado.iloc[0] if not resultado.empty else valor_default

def calcular_estado_semaforo(area_iceberg, area_agua, tipo_usuario):
    if "Turista" in tipo_usuario:
        if area_iceberg < 0.4 and 105 <= area_agua <= 120:
            return "verde", "🟢 CONDICIONES PERFECTAS", "¡Los icebergs y la laguna están en su máximo esplendor!"
        elif area_iceberg < 0.3 or (100 <= area_agua <= 125):
            return "amarillo", "🟡 BUENAS CONDICIONES", "Buen momento para explorar con precauciones."
        else:
            return "rojo", "🔴 CONDICIONES VARIABLES", "Consulta con guías locales antes de tu aventura."

    elif "Local" in tipo_usuario:
        if 0.30 <= area_iceberg <= 0.45 and 105 <= area_agua <= 120:
            return "verde", "🟢 OPERACIONES ÓPTIMAS", "Condiciones ideales para operaciones."
        elif 0.3 <= area_iceberg <= 0.5 or 100 <= area_agua <= 125:
            return "amarillo", "🟡 PRECAUCIÓN OPERATIVA", "Monitoreo continuo recomendado."
        else:
            return "rojo", "🔴 ALERTA OPERACIONAL", "Condiciones fuera de rango - precaución extrema."

    else:  # Investigador
        return "verde", "🟢 DATOS CIENTÍFICOS DISPONIBLES", "Condiciones óptimas para análisis de datos."

def procesar_pregunta(pregunta, iceberg_df, water_df, tipo_usuario):
    pregunta = pregunta.lower().strip()
    fecha_hoy = datetime.now().date()
    # Mapear días de la semana en inglés a español
    dias_es = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    # Obtener el día de la semana en español
    dia_semana = dias_es.get(datetime.now().strftime('%A'), 'Desconocido')

    # Obtener valores actuales
    area_iceberg_hoy = obtener_prediccion_diaria(iceberg_df, 'Area_km2', 0.35)
    area_agua_hoy = obtener_prediccion_diaria(water_df, 'Area_km2', 110.0)

    # Respuestas predefinidas basadas en palabras clave
    if any(palabra in pregunta for palabra in ['área icebergs', 'area iceberg', 'iceberg hoy', 'área de icebergs hoy']):
        return f"❄️ El área de los icebergs hoy ({fecha_hoy}) es de **{area_iceberg_hoy:.3f} km²**."

    elif any(palabra in pregunta for palabra in ['área laguna', 'area laguna', 'lago hoy', 'área de laguna hoy']):
        return f"🌊 El área de la laguna hoy ({fecha_hoy}) es de **{area_agua_hoy:.2f} km²**."

    elif any(palabra in pregunta for palabra in ['condiciones hoy', 'estado hoy']):
        estado_color, estado_titulo, estado_descripcion = calcular_estado_semaforo(
            area_iceberg_hoy, area_agua_hoy, tipo_usuario
        )
        return f"📊 **{estado_titulo}**: {estado_descripcion}"

    elif 'consejos' in pregunta or 'recomendaciones' in pregunta:
        consejos = {
            "Investigador Científico": {
                "Lunes": "📡 Revisa los datos satelitales de Sentinel-2 para calibrar tus modelos.",
                "Martes": "🔬 Analiza las tendencias de deshielo con los datos históricos.",
                "Miércoles": "📊 Compara las predicciones con observaciones in situ.",
                "Jueves": "🖥️ Actualiza tus modelos con los datos más recientes.",
                "Viernes": "📝 Prepara tu informe semanal con los datos de Patag-ICE.",
                "Sábado": "🌐 Comparte tus hallazgos en foros científicos.",
                "Domingo": "📚 Revisa literatura reciente sobre glaciares patagónicos."
            },
            "Turista Aventurero": {
                "Lunes": "📸 Lleva tu cámara para capturar los icebergs al amanecer.",
                "Martes": "⛵ Reserva una navegación para explorar la laguna.",
                "Miércoles": "🧥 Prepárate para el frío con ropa térmica.",
                "Jueves": "👀 Consulta el clima antes de tu excursión.",
                "Viernes": "🌄 Disfruta de las vistas al atardecer en la laguna.",
                "Sábado": "🏞️ Explora los senderos cercanos con un guía local.",
                "Domingo": "📷 Comparte tus fotos de la aventura en redes sociales."
            },
            "Comunidad Local": {
                "Lunes": "⚙️ Verifica el estado de las embarcaciones para la semana.",
                "Martes": "📡 Monitorea las condiciones de la laguna cada hora.",
                "Miércoles": "🚨 Revisa los protocolos de emergencia.",
                "Jueves": "📅 Planifica las rutas de navegación según el área de la laguna.",
                "Viernes": "📊 Evalúa las tendencias de área para el fin de semana.",
                "Sábado": "👷 Capacita al personal en seguridad operativa.",
                "Domingo": "📋 Prepara el reporte semanal de operaciones."
            }
        }
        # Normalizar tipo_usuario para coincidir con las claves del diccionario
        tipos_validos = ["Investigador Científico", "Turista Aventurero", "Operador Local"]
        tipo_normalizado = next((t for t in tipos_validos if t in tipo_usuario), None)

        if tipo_normalizado and dia_semana in consejos.get(tipo_normalizado, {}):
            consejo = consejos[tipo_normalizado][dia_semana]
        else:
            consejo = "📌 No hay consejos específicos para hoy. Asegúrate de que el tipo de usuario sea válido."

        return f"🗣️ **Consejo para hoy ({dia_semana})**: {consejo}"

    elif re.search(r'\d{4}-\d{2}-\d{2}', pregunta):  # Detectar fechas en formato YYYY-MM-DD
        fecha_preguntada = re.search(r'\d{4}-\d{2}-\d{2}', pregunta).group()
        try:
            fecha_preguntada = pd.to_datetime(fecha_preguntada).date()
            area_iceberg_fecha = iceberg_df.loc[iceberg_df['Fecha'] == fecha_preguntada, 'Area_km2']
            area_agua_fecha = water_df.loc[water_df['Fecha'] == fecha_preguntada, 'Area_km2']

            respuesta = f"📅 Para la fecha **{fecha_preguntada}**:\n"
            if not area_iceberg_fecha.empty:
                respuesta += f"❄️ Área de icebergs: **{area_iceberg_fecha.iloc[0]:.3f} km²**\n"
            else:
                respuesta += "❄️ No hay datos de icebergs para esa fecha.\n"
            if not area_agua_fecha.empty:
                respuesta += f"🌊 Área de laguna: **{area_agua_fecha.iloc[0]:.2f} km²**"
            else:
                respuesta += "🌊 No hay datos de laguna para esa fecha."
            return respuesta
        except ValueError:
            return "❌ Formato de fecha inválido. Usa YYYY-MM-DD (por ejemplo: 2025-06-16)."

    else:
        return "🤔 No entendí tu pregunta. Prueba con:\n- 'Área de iceberg hoy'\n- 'Área de laguna hoy'\n- 'Condiciones hoy'\n- 'Consejos'\n- 'Área para YYYY-MM-DD'"
def crear_prevision_operacional(proxima_semana, siguiente_semana, water_filtrado):
    if proxima_semana > 120.0:
        proxima_estado = "🔴 Área alta - Precaución extrema"
    elif proxima_semana < 110.0:
        proxima_estado = "🟡 Área baja - Monitoreo continuo"
    else:
        proxima_estado = "🟢 Condiciones estables"

    html_content = f"""
    <div class="metric-card">
        <h4>📅 Previsión Operacional</h4>
        <p><strong>Próxima semana:</strong> {proxima_estado}</p>
    """

    if len(water_filtrado) >= 14:
        if siguiente_semana > 120.0:
            semana2_estado = "🔴 Tendencia al alza - Preparar protocolos"
        elif siguiente_semana < 110.0:
            semana2_estado = "🟡 Tendencia a la baja - Evaluar restricciones"
        else:
            semana2_estado = "🟢 Estabilidad esperada"
        html_content += f"<p><strong>Semana 2:</strong> {semana2_estado}</p>"

    html_content += "</div>"
    return html_content

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://www.chiledesarrollosustentable.cl/wp-content/uploads/2015/02/laguna-san-rafael-15.jpg" 
             style="width: 100%; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
        <p style="color: white; margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
            📍 Parque Nacional Laguna San Rafael, Región de Aysén
        </p>
    </div>
    """, unsafe_allow_html=True)

    tipo_usuario = st.selectbox(
        "👤 ¿Cuál es tu perfil?",
        ["🔬 Investigador Científico", "🎒 Turista Aventurero", "🏠 Comunidad Local"],
        help="Selecciona tu perfil para personalizar la información"
    )

    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent, white, transparent); 
                margin: 20px 0; border-radius: 1px;"></div>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 **Configuración Temporal**")
    fecha_inicio = st.date_input(
        "🗓️ Fecha de inicio del análisis",
        value=datetime.now(),
        help="Selecciona desde cuándo iniciar las predicciones"
    )

    dias_prediccion = st.slider(
        "📊 Horizonte de predicción (días)",
        min_value=7,
        max_value=60,
        value=30,
        help="Rango temporal para visualizar las predicciones"
    )

    # Carga de datos
    @st.cache_data(ttl=3600)
    def cargar_datos_cached():
        return cargar_datos()

    iceberg_df, water_df = cargar_datos_cached()

    current_date = datetime.now().date()
    area_iceberg_actual = obtener_valor_actual(iceberg_df, current_date, 'Area_km2')
    area_agua_actual = obtener_valor_actual(water_df, current_date, 'Area_km2')

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; 
                margin-top: 20px; border: 1px solid rgba(255,255,255,0.2);">
        <h4 style="color: white; margin-bottom: 10px;">📊 Estado del Parque Nacional Laguna San Rafael</h4>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 5px 0;">
            📅 Fecha: <strong>{current_date}</strong><br>
            ❄️ Área Iceberg: <strong>{area_iceberg_actual:.3f} km²</strong><br>
            🌊 Área Laguna: <strong>{area_agua_actual:.2f} km²</strong><br>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Chatbot
    st.markdown("### 🤖 **Asistente Patagónico**")
    st.markdown("Pregúntame sobre el área de icebergs, la laguna, condiciones o pide consejos para hoy.")
    pregunta_usuario = st.text_input("Escribe tu pregunta:", placeholder="Ejemplo: ¿Cuál es el área de los icebergs hoy?")
    if pregunta_usuario:
        respuesta = procesar_pregunta(pregunta_usuario, iceberg_df, water_df, tipo_usuario)
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>🗣️ Pregunta:</strong> {pregunta_usuario}</p>
            <p><strong>🤖 Respuesta:</strong> {respuesta}</p>
        </div>
        """, unsafe_allow_html=True)

# Filtrar datos con fallback
fecha_fin = fecha_inicio + timedelta(days=dias_prediccion)
iceberg_filtrado = iceberg_df[
    (iceberg_df['Fecha'] >= fecha_inicio) & 
    (iceberg_df['Fecha'] <= fecha_fin)
]
water_filtrado = water_df[
    (water_df['Fecha'] >= fecha_inicio) & 
    (water_df['Fecha'] <= fecha_fin)
]

# Fallback: Si los DataFrames están vacíos, usar los datos más recientes
if iceberg_filtrado.empty:
    st.warning("⚠️ No hay datos de icebergs para el rango de fechas seleccionado. Mostrando los datos más recientes disponibles.")
    iceberg_filtrado = iceberg_df.iloc[-dias_prediccion:] if len(iceberg_df) >= dias_prediccion else iceberg_df
if water_filtrado.empty:
    st.warning("⚠️ No hay datos de área de laguna para el rango de fechas seleccionado. Mostrando los datos más recientes disponibles.")
    water_filtrado = water_df.iloc[-dias_prediccion:] if len(water_df) >= dias_prediccion else water_df

# Obtener predicción diaria
area_iceberg_actual = obtener_prediccion_diaria(iceberg_df, 'Area_km2', 0.35)
area_agua_actual = obtener_prediccion_diaria(water_df, 'Area_km2', 110.0)

# Mostrar semáforo
estado_color, estado_titulo, estado_descripcion = calcular_estado_semaforo(
    area_iceberg_actual, area_agua_actual, tipo_usuario
)
st.markdown(f"""
<div class="status-{estado_color}">
    <h2 style="margin-bottom: 10px;">{estado_titulo}</h2>
    <p style="font-size: 1.1rem; margin-bottom: 5px;">{estado_descripcion}</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">
        📊 Análisis basado en datos satelitales • 🕐 Último update: {datetime.now().strftime('%H:%M hrs')}
    </p>
</div>
""", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([2.5, 1])

if "Investigador" in tipo_usuario:
    with col1:
        st.markdown("### 📊 **Análisis Científico Avanzado**")
        tab1, tab2 = st.tabs(["❄️ Área Total de Icebergs", "🌊 Área de Laguna San Rafael"])

        with tab1:
            fig_iceberg = go.Figure()
            fig_iceberg.add_trace(go.Scatter(
                x=iceberg_filtrado['Fecha'], 
                y=iceberg_filtrado['Area_km2'],
                mode='lines+markers',
                name='Área Predicha',
                line=dict(color='#2563eb', width=3),
                marker=dict(size=8, color='#2563eb')
            ))
            fig_iceberg.update_layout(
                title="Predicción del Área Total de Icebergs - Modelo Ridge",
                xaxis_title="Fecha",
                yaxis_title="Área (km²)",
                height=450,
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0)',
                font=dict(family="Inter, sans-serif")
            )
            st.plotly_chart(fig_iceberg, use_container_width=True)

        with tab2:
            fig_water = go.Figure()
            fig_water.add_trace(go.Scatter(
                x=water_filtrado['Fecha'], 
                y=water_filtrado['Area_km2'],
                mode='lines+markers',
                name='Área Predicha',
                line=dict(color='#059669', width=3),
                marker=dict(size=8, color='#059669'),
                fill='tonexty',
                fillcolor='rgba(5, 150, 105, 0.1)'
            ))
            fig_water.update_layout(
                title="Predicción del Área de la Laguna - Modelo Regresión",
                xaxis_title="Fecha",
                yaxis_title="Área (km²)",
                height=450,
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0)',
                font=dict(family="Inter, sans-serif")
            )
            st.plotly_chart(fig_water, use_container_width=True)

    with col2:
        st.markdown("### 🔬 **Panel Científico**")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            delta_iceberg = (iceberg_filtrado['Area_km2'].iloc[-1] - iceberg_filtrado['Area_km2'].iloc[0] 
                             if len(iceberg_filtrado) > 1 else 0)
            st.metric(
                "📈 Área Iceberg Promedio", 
                f"{iceberg_filtrado['Area_km2'].mean():.3f} km²",
                f"{delta_iceberg:.3f}"
            )
        with col_m2:
            delta_area = (water_filtrado['Area_km2'].iloc[-1] - water_filtrado['Area_km2'].iloc[0] 
                          if len(water_filtrado) > 1 else 0)
            st.metric(
                "🌊 Área Laguna Promedio", 
                f"{water_filtrado['Area_km2'].mean():.2f} km²",
                f"{delta_area:.2f}"
            )
        st.markdown("""
        <div class="metric-card">
            <h4>🛰️ Especificaciones Técnicas</h4>
            <p><strong>Fuente de Datos:</strong> Sentinel-2 </p>
            <p><strong>Resolución:</strong> 10m/píxel</p>
            <p><strong>Modelo:</strong> Ridge Regression</p>
            <p><strong>Actualización:</strong> Diaria</p>
        </div>
        """, unsafe_allow_html=True)

elif "Turista" in tipo_usuario:
    with col1:
        st.markdown("### 🏔️ **Tu Aventura Patagónica**")
        fig_iceberg_tur = go.Figure()
        # Rectángulo para condiciones variables (>3.3)
        fig_iceberg_tur.add_hrect(
            y0=3.3, y1=5.0, 
            fillcolor="rgba(239, 68, 68, 0.2)",
            annotation_text="⚠️ Condiciones variables", 
            annotation_position="top left",
            annotation=dict(font=dict(color="black")),
            line_width=0
        )

        # Rectángulo para buenas condiciones (1.6 a 3.3)
        fig_iceberg_tur.add_hrect(
            y0=1.6, y1=3.3, 
            fillcolor="rgba(245, 158, 11, 0.2)", 
            annotation_text="✨ Buenas condiciones", 
            annotation_position="top left",
            annotation=dict(font=dict(color="black")),
            line_width=0
        )

        # Rectángulo para condiciones ideales (0 a 1.5)
        fig_iceberg_tur.add_hrect(
            y0=0.0, y1=1.5, 
            fillcolor="rgba(34, 197, 94, 0.2)", 
            annotation_text="🎉 Condiciones ideales", 
            annotation_position="top left",
            annotation=dict(font=dict(color="black")),
            line_width=0
        )
        fig_iceberg_tur.add_trace(go.Scatter(
            x=iceberg_filtrado['Fecha'], 
            y=iceberg_filtrado['Area_km2'],
            mode='lines+markers', 
            name='Estado de Icebergs',
            line=dict(color='#1e88e5', width=4),
            marker=dict(size=12, color='#1e88e5', symbol='diamond')
        ))
        fig_iceberg_tur.update_layout(
            title=dict(
                text="🌨️ Estado del Área Total de los Icebergs para tu Visita",
                font=dict(family="Inter", size=12, color="black")
            ),
            xaxis=dict(
                title="📅 Fechas de tu Aventura",
                title_font=dict(family="Inter, sans-serif", size=12, color="black")
            ),
            yaxis=dict(
                title="❄️ Área de Icebergs (km²)",
                title_font=dict(family="Inter, sans-serif", size=12, color="black")
            ),
            height=450,
            plot_bgcolor='rgba(255,255,255,0.8)',  # Reducir opacidad para mejor contraste
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family="Inter, sans-serif", size=12, color="black")  # Fallback para otros textos
        )
        st.plotly_chart(fig_iceberg_tur, use_container_width=True)

        if area_iceberg_actual > 0.4:
            st.success("🎉 **¡Momento perfecto!** Los icebergs están en condiciones excepcionales. Prepara tu cámara.")
        elif area_iceberg_actual > 0.3:
            st.info("✨ **Excelentes condiciones** para tu aventura. Los icebergs muestran su belleza natural.")
        else:
            st.warning("⚠️ **Condiciones variables** - Consulta con guías locales para una experiencia segura.")

    with col2:
        st.markdown("### 🎒 **Guía del Aventurero**")
        delta_iceberg = (iceberg_filtrado['Area_km2'].iloc[-1] - area_iceberg_actual 
                         if len(iceberg_filtrado) > 1 else 0)
        st.metric(
            "🏔️ Estado de Área Total de los Icebergs", 
            f"{area_iceberg_actual:.3f} km²",
            f"{delta_iceberg:.3f} km²"
        )
        st.markdown("""
        <div class="metric-card">
            <h4>🌟 Consejos para tu Aventura</h4>
            <p><strong>🧥 Vestimenta:</strong> Abrigo impermeable, guantes</p>
            <p><strong>⛵ Navegación:</strong> Confirmar meteorología</p>
        </div>
        """, unsafe_allow_html=True)
        if area_iceberg_actual > 0.2:
            st.markdown("""
            <div class="metric-card" style="background: rgba(34, 197, 94, 0.1);">
                <h4>📸 Oportunidad Única</h4>
                <p>Condiciones perfectas para:</p>
                <p>• Fotografía de icebergs</p>
                <p>• Navegación por la laguna</p>
            </div>
            """, unsafe_allow_html=True)


elif "Local" in tipo_usuario:
    with col1:
        st.markdown("### 📈 **Panel de Operaciones Locales**")
        fig_water_loc = go.Figure()
        zonas = [
            (100.0, 105.0, "rgba(220, 38, 38, 0.3)", "🔴 Área Crítica Baja"),
            (105.0, 110.0, "rgba(245, 158, 11, 0.3)", "🟡 Precaución"),
            (110.0, 120.0, "rgba(34, 197, 94, 0.3)", "🟢 Operación Óptima"),
            (120.0, 125.0, "rgba(245, 158, 11, 0.3)", "🟡 Área Alta"),
            (125.0, 130.0, "rgba(220, 38, 38, 0.3)", "🔴 Área Crítica Alta")
        ]
        for y0, y1, color, text in zonas:
            fig_water_loc.add_hrect(
                y0=y0, y1=y1, 
                fillcolor=color, 
                annotation_text=text, 
                annotation_position="top left",
                annotation=dict(font=dict(color="black")),  # Texto negro para anotaciones
                line_width=0
            )
        fig_water_loc.add_trace(go.Scatter(
            x=water_filtrado['Fecha'], 
            y=water_filtrado['Area_km2'],
            mode='lines+markers', 
            name='Área de Agua',
            line=dict(color='#2e7d32', width=4),
            marker=dict(size=10, color='#2e7d32')
        ))
        fig_water_loc.update_layout(
            title=dict(
                text="🌊 Área de Laguna San Rafael - Monitoreo Operacional",
                font=dict(family="Inter, sans-serif", size=12, color="black")  # Título en negro
            ),
            xaxis=dict(
                title="📅 Fecha",
                title_font=dict(family="Inter, sans-serif", size=12, color="black")  # Eje X en negro
            ),
            yaxis=dict(
                title="💧 Área (km²)",
                title_font=dict(family="Inter, sans-serif", size=12, color="black")  # Eje Y en negro
            ),
            height=450,
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0)',
            font=dict(family="Inter, sans-serif", size=12, color="black")  # Fallback para otros textos
        )
        st.plotly_chart(fig_water_loc, use_container_width=True)

        area_promedio = water_filtrado['Area_km2'].mean() if not water_filtrado.empty else area_agua_actual
        area_tendencia = (water_filtrado['Area_km2'].iloc[-1] - water_filtrado['Area_km2'].iloc[0] 
                          if len(water_filtrado) > 1 else 0)

        if area_promedio < 105.0:
            st.error("🚨 **ALERTA CRÍTICA**: Área de la laguna muy baja - Suspender navegación.")
        elif area_promedio > 125.0:
            st.error("🚨 **ALERTA CRÍTICA**: Área de la laguna muy alta - Riesgo de inundación.")
        elif area_promedio < 110.0 or area_promedio > 120.0:
            st.warning("⚠️ **PRECAUCIÓN OPERATIVA**: Área fuera del rango óptimo - Monitoreo intensivo.")
        else:
            st.success("✅ **CONDICIONES ÓPTIMAS**: Área de Laguna en rango normal para operaciones.")

        if abs(area_tendencia) > 5.0:
            if area_tendencia > 0:
                st.info(f"📈 **TENDENCIA ASCENDENTE**: El área está subiendo {area_tendencia:.2f} km².")
            else:
                st.info(f"📉 **TENDENCIA DESCENDENTE**: El área está bajando {abs(area_tendencia):.2f} km².")

    with col2:
        st.markdown("### 🏠 **Centro de Control Local**")
        col_op1, col_op2 = st.columns(2)
        with col_op1:
            delta_area = (water_filtrado['Area_km2'].iloc[-1] - area_agua_actual 
                          if len(water_filtrado) > 1 else None)
            st.metric(
                "🌊 Área Actual", 
                f"{area_agua_actual:.2f} km²",
                f"{delta_area:.2f} km²" if delta_area is not None else None
            )
        with col_op2:
            promedio_7_dias = water_filtrado.head(7)['Area_km2'].mean() if len(water_filtrado) >= 7 else area_agua_actual
            st.metric(
                "📊 Promedio 7 días", 
                f"{promedio_7_dias:.2f} km²"
            )
        st.markdown("""
        <div class="metric-card">
            <h4>⚙️ Parámetros Operacionales</h4>
            <p><strong>🟢 Navegación segura:</strong> 110.0 - 130.0 km²</p>
            <p><strong>🟡 Precaución:</strong> 105.0 - 110.0 km² / 130.0 - 135.0 km²</p>
            <p><strong>🔴 Alerta crítica:</strong> <105.0 km²/     >135.0 km²</p>
            <p><strong>⚡ Monitoreo:</strong> Cada hora</p>
        </div>
        """, unsafe_allow_html=True)

        proxima_semana = water_filtrado.head(7)['Area_km2'].mean() if len(water_filtrado) >= 7 else area_agua_actual
        siguiente_semana = (water_filtrado.iloc[7:14]['Area_km2'].mean() 
                           if len(water_filtrado) >= 14 else proxima_semana)

        html_prevision = crear_prevision_operacional(proxima_semana, siguiente_semana, water_filtrado)
        st.markdown(html_prevision, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <h4>🚨 Contactos de Emergencia</h4>
            <p><strong>CONAF:</strong> 130</p>
            <p><strong>SAMU:</strong> 131</p>
            <p><strong>Bomberos:</strong> 132</p>
            <p><strong>Carabineros:</strong> 133</p>
            <p><strong>PDI:</strong> 134</p>
            <p><strong>Autoridad Marítima:</strong> 137</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 📜 Aviso legal sobre uso de librerías de terceros
#
# Esta aplicación utiliza las siguientes bibliotecas de software de código abierto,
# cada una sujeta a sus respectivas licencias:
#
# - Streamlit: Copyright (c) 2018-2025 Streamlit Inc. Licencia Apache 2.0.
#   Ver: https://github.com/streamlit/streamlit/blob/develop/LICENSE
#
# - Pandas: Copyright (c) 2008-2022 Pandas Development Team. Licencia BSD 3-Clause.
#   Ver: https://github.com/pandas-dev/pandas/blob/main/LICENSE
#
# - Plotly: Copyright (c) 2016-2025 Plotly, Inc. Licencia MIT.
#   Ver: https://github.com/plotly/plotly.py/blob/master/LICENSE.txt
#
# - NumPy: Copyright (c) 2005-2025 NumPy Developers. Licencia BSD 3-Clause.
#   Ver: https://github.com/numpy/numpy/blob/main/LICENSE.txt
#
# - datetime y re: Módulos de la biblioteca estándar de Python.
#   Copyright (c) 2001-2025 Python Software Foundation. Licencia PSF.
#   Ver: https://docs.python.org/3/license.html
#
# Estas herramientas se utilizan con fines científicos, educativos y de divulgación,
# respetando los términos de sus licencias. Todos los derechos pertenecen a sus
# respectivos autores y comunidades de desarrollo.
#
# Este código se proporciona "tal cual", sin garantías de ningún tipo, expresas o
# implícitas, incluyendo pero no limitado a garantías de comerciabilidad, idoneidad
# para un propósito particular o no infracción.
# ------------------------------------------------------------------------------
