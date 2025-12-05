import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image

# ==========================
# GENERACIÓN DE DATOS DE EJEMPLO
# ==========================

CIUDADES = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga"]
TIPOS_RESIDUO = ["Electrónicos", "Vidrio", "Papel", "Plástico", "Metálico", "Baterías", "Orgánico"]

def generar_datos():
    # ---- Clientes ----
    clientes_data = [
        ["C001", "Empresa", "EcoAndes Reciclaje S.A.S.", "901234567-1", "310 555 1234", "contacto@ecoandes.com",
         "Bogotá", "Calle 80 #15-30"],
        ["C002", "Empresa", "BioTechNova S.A.S.", "901987654-2", "300 222 3344", "ambiental@biotechnova.com",
         "Medellín", "Carrera 45 #10-22"],
        ["C003", "Empresa", "Logística Verde Colombia S.A.S.", "900345678-3", "320 999 8877",
         "info@logisticaverde.co", "Cali", "Avenida 6N #34-50"],
        ["C004", "Persona Natural", "Paola Rodríguez", "1.023.456.789", "315 666 7788", "paola.rodri@example.com",
         "Bogotá", "Calle 134 #19-70"],
        ["C005", "Persona Natural", "Juan Pérez", "1.008.765.432", "301 444 5566", "juan.perez@example.com",
         "Barranquilla", "Carrera 51B #82-130"],
    ]
    clientes_cols = ["id_cliente", "tipo_cliente", "nombre_cliente", "identificacion",
                     "telefono", "correo", "ciudad", "direccion"]
    clientes_df = pd.DataFrame(clientes_data, columns=clientes_cols)

    # ---- Personal ----
    personal_data = [
        ["P001", "Carlos Gómez", "Conductor", "Bogotá", True, True, "S001", 1, 5, "Conductor con alto compromiso"],
        ["P002", "Andrea López", "Conductor", "Medellín", True, False, None, 0, 3,
         "Apoya rutas de contingencia"],
        ["P003", "Luis Martínez", "Supervisor", "Bogotá", True, False, None, 0, 10,
         "Responsable de la operación en Bogotá"],
        ["P004", "María Fernanda Rivera", "Operador de Plataforma", "Cali", True, False, None, 0, 0,
         "Gestiona solicitudes y certificaciones"],
    ]
    personal_cols = ["id_personal", "nombre", "rol", "ciudad_base", "activo",
                     "en_servicio_ahora", "solicitud_actual", "quejas_recibidas",
                     "incidencias_resueltas", "comentarios_internos"]
    personal_df = pd.DataFrame(personal_data, columns=personal_cols)

    # ---- Vehículos ----
    vehiculos_data = [
        ["V001", "ABC123", "Camión", 2020, "Operativo", True, datetime(2026, 5, 10),
         datetime(2024, 10, 1), "Sin novedades", "P001", 1200, "Rutas RAEE Bogotá",
         "Bogotá", 4.7110, -74.0721],
        ["V002", "XYZ987", "Furgón", 2018, "En mantenimiento", True, datetime(2025, 11, 20),
         datetime(2024, 9, 15), "Cambio de frenos", "P002", 980, "Recolección vidrio Medellín",
         "Medellín", 6.2518, -75.5636],
        ["V003", "KLM456", "Camión", 2019, "Operativo", True, datetime(2025, 8, 30),
         datetime(2024, 7, 5), "Sin novedades", None, 1500, "Rutas mixtas Caribe",
         "Barranquilla", 10.9878, -74.7889],
    ]
    vehiculos_cols = ["id_vehiculo", "placa", "tipo", "año", "estado_actual",
                      "soat_vigente", "fecha_vencimiento_soat", "ultima_revision_mantenimiento",
                      "problemas_reportados", "personal_asignado", "tiempo_operacion_horas",
                      "trabajos_realizados", "ubicacion_actual", "lat", "lon"]
    vehiculos_df = pd.DataFrame(vehiculos_data, columns=vehiculos_cols)

    # ---- Solicitudes ----
    hoy = datetime.now()
    solicitudes_data = [
        ["S001", "C001", "Electrónicos", 180, hoy - timedelta(days=7),
         hoy + timedelta(days=1), "En tránsito", "Ruta Bogotá Norte",
         "Carlos, Andrés", "Excelente servicio, muy puntuales.",
         "https://images.pexels.com/photos/929282/pexels-photo-929282.jpeg",
         "https://example.com/doc/s001_evidencia.pdf",
         True, "https://example.com/cert/s001_cert.pdf", "P001",
         hoy - timedelta(days=1)],
        ["S002", "C002", "Baterías", 95, hoy - timedelta(days=10),
         hoy - timedelta(days=2), "Finalizada", "Ruta Medellín Centro",
         "Equipo interno", "Todo el proceso fue claro.",
         "https://images.pexels.com/photos/209271/pexels-photo-209271.jpeg",
         "https://example.com/doc/s002_evidencia.pdf",
         True, "https://example.com/cert/s002_cert.pdf", "P002",
         hoy - timedelta(days=2)],
        ["S003", "C003", "Vidrio", 250, hoy - timedelta(days=3),
         hoy + timedelta(days=3), "Pendiente", None,
         None, None, None, False, None, None,
         hoy - timedelta(days=3)],
        ["S004", "C004", "Papel", 60, hoy - timedelta(days=1),
         hoy + timedelta(days=4), "Solicitada", None,
         None, None, None, False, None, None,
         hoy - timedelta(days=1)],
        ["S005", "C005", "Plástico", 130, hoy - timedelta(days=15),
         hoy - timedelta(days=5), "Incidencia", "Ruta Caribe 02",
         "Carlos", "Hubo un retraso por tráfico, pero se resolvió.",
         "https://images.pexels.com/photos/802221/pexels-photo-802221.jpeg",
         "https://example.com/doc/s005_evidencia.pdf",
         False, None, "P001",
         hoy - timedelta(days=5)],
    ]
    solicitudes_cols = [
        "id_solicitud", "id_cliente", "tipo_residuo", "cantidad_kg",
        "fecha_solicitud", "fecha_programada", "estado", "ruta_asignada",
        "personas_que_ayudaron", "opinion_cliente", "foto_evidencia",
        "link_documento_evidencia", "certificado_emitido", "link_certificado",
        "persona_encargada_recoleccion", "fecha_ultima_actualizacion"
    ]
    solicitudes_df = pd.DataFrame(solicitudes_data, columns=solicitudes_cols)

    # ---- Eventos DataLake ----
    eventos_data = [
        ["E001", "S001", "Creación", "Solicitud creada por EcoAndes Reciclaje S.A.S.", hoy - timedelta(days=7),
         "Paola (Operadora)", None],
        ["E002", "S001", "Programación", "Recolección programada para mañana.", hoy - timedelta(days=2),
         "María (Operadora)", None],
        ["E003", "S001", "En ruta", "Vehículo ABC123 salió hacia el punto de recolección.", hoy - timedelta(days=1),
         "Carlos (Conductor)", "https://example.com/gps/s001_ruta"],
        ["E004", "S002", "Creación", "Solicitud creada para BioTechNova S.A.S.", hoy - timedelta(days=10),
         "María (Operadora)", None],
        ["E005", "S002", "Cierre", "Recolección finalizada y certificado generado.", hoy - timedelta(days=2),
         "Andrea (Conductor)", "https://example.com/cert/s002_cert.pdf"],
        ["E006", "S005", "Incidencia", "Retraso por congestión vial en la Vía al Mar.", hoy - timedelta(days=6),
         "Carlos (Conductor)", "https://example.com/gps/s005_incidente"],
        ["E007", "S003", "Creación", "Solicitud creada para Logística Verde Colombia S.A.S.", hoy - timedelta(days=3),
         "Paola (Operadora)", None],
    ]
    eventos_cols = ["id_evento", "id_solicitud", "tipo_evento",
                    "descripcion_evento", "fecha_evento", "usuario_responsable",
                    "link_archivo"]
    eventos_df = pd.DataFrame(eventos_data, columns=eventos_cols)

    # ---- Historias públicas ----
    historias_data = [
        ["H001", "S001",
         "https://images.pexels.com/photos/2547565/pexels-photo-2547565.jpeg",
         "EcoAndes y EcoSynchro: RAEE con propósito",
         "EcoAndes Reciclaje S.A.S.",
         "Bogotá",
         "EcoAndes confió en EcoSynchro para gestionar de forma responsable sus residuos electrónicos, garantizando trazabilidad y disposición final certificada.",
         "Es clave poder demostrarle a nuestros clientes que nuestros residuos tienen un destino responsable.",
         "Saber que nuestro trabajo cuida al planeta y sostiene a nuestras familias nos motiva cada día.",
         hoy - timedelta(days=1),
         "https://example.com/historias/ecoandes"],
        ["H002", "S002",
         "https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg",
         "BioTechNova reduce su huella con EcoSynchro",
         "BioTechNova S.A.S.",
         "Medellín",
         "BioTechNova integró la recolección de baterías usadas al modelo de EcoSynchro, fortaleciendo su compromiso con la sostenibilidad.",
         "No solo cumplimos la norma, ahora podemos mostrarlo con datos.",
         "Cada ruta bien planificada es tiempo ganado y menos estrés en la vía.",
         hoy - timedelta(days=5),
         "https://example.com/historias/biotechnova"],
    ]
    historias_cols = ["id_historia", "id_solicitud", "portada_imagen",
                      "titulo_publicacion", "cliente_visible", "ciudad",
                      "resumen_situacion", "frase_del_cliente",
                      "frase_del_recolector", "fecha_publicacion",
                      "link_externo"]
    historias_df = pd.DataFrame(historias_data, columns=historias_cols)

    return clientes_df, personal_df, vehiculos_df, solicitudes_df, eventos_df, historias_df

# Configuración de página
st.set_page_config(
    page_title="EcoSynchro - Gestión Ambiental",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# ESTILOS PROFESIONALES
# ==========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-green: #10b981;
    --dark-green: #047857;
    --light-green: #d1fae5;
    --accent-green: #34d399;
    --bg-dark: #0f172a;
    --bg-card: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --border-color: #334155;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* SIDEBAR PROFESIONAL */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 1rem;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px 16px;
    transition: all 0.2s ease;
    cursor: pointer;
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--primary-green);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
}

[data-testid="stSidebar"] div[role="radio"][aria-checked="true"] {
    background: linear-gradient(135deg, var(--primary-green), var(--dark-green));
    border-color: var(--accent-green);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

[data-testid="stSidebar"] div[role="radio"] > div:first-child {
    display: none;
}

/* TÍTULOS */
h1 {
    background: linear-gradient(135deg, var(--primary-green), var(--accent-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* TEXTO GENERAL */
p, span, label, div {
    color: var(--text-primary) !important;
}

/* CAPTIONS Y TEXTO SECUNDARIO */
.stCaption {
    color: var(--text-secondary) !important;
}

/* MARKDOWN TEXT */
.stMarkdown {
    color: var(--text-primary) !important;
}

/* SELECTBOX Y DROPDOWNS */
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stSelectbox label {
    color: var(--text-primary) !important;
}

/* OPCIONES DEL SELECTBOX */
[data-baseweb="select"] {
    background-color: var(--bg-card) !important;
}

[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

/* MENU DESPLEGABLE */
[role="listbox"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
}

[role="option"] {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

[role="option"]:hover {
    background-color: var(--primary-green) !important;
    color: white !important;
}

/* RADIO BUTTONS */
.stRadio > label {
    color: var(--text-primary) !important;
}

/* EXPANDER MEJORADO */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, var(--bg-card), rgba(16, 185, 129, 0.1)) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-bottom: 0.5rem !important;
}

.streamlit-expanderHeader:hover {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.2)) !important;
    border-color: var(--primary-green) !important;
}

.streamlit-expanderContent {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.5rem !important;
    margin-top: -0.5rem !important;
}

/* ICONO DEL EXPANDER */
.streamlit-expanderHeader svg {
    color: var(--primary-green) !important;
}

/* OCULTAR KEYBOARD ARROW TEXT */
.streamlit-expanderHeader {
    font-size: 0 !important;
}

.streamlit-expanderHeader::before {
    content: "Configurar Filtros de Búsqueda" !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

.streamlit-expanderHeader::after {
    content: "▼" !important;
    font-size: 1rem !important;
    color: var(--primary-green) !important;
    float: right !important;
    transition: transform 0.2s ease !important;
}

.streamlit-expanderHeader[aria-expanded="true"]::after {
    transform: rotate(180deg) !important;
}

/* BOTONES DE MATPLOTLIB */
.stPlotlyChart button {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

/* TOOLBAR DE MATPLOTLIB */
.js-plotly-plot .plotly .modebar {
    background-color: var(--bg-card) !important;
}

.js-plotly-plot .plotly .modebar-btn {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.js-plotly-plot .plotly .modebar-btn:hover {
    background-color: var(--primary-green) !important;
}

/* MÉTRICAS */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
}

/* TABLAS */
[data-testid="stDataFrame"] {
    background: var(--bg-card);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

/* FILTROS */
[data-testid="stMultiSelect"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}

[data-baseweb="tag"] {
    background: var(--primary-green) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: 500 !important;
}

/* ALERTAS */
.stAlert {
    background: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid var(--primary-green) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}

/* BOTONES */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-green), var(--dark-green));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

/* HEADER PERSONALIZADO */
.header-container {
    background: linear-gradient(135deg, var(--bg-card), rgba(16, 185, 129, 0.05));
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    border: 1px solid var(--border-color);
    text-align: center;
}

.subtitle {
    color: var(--text-secondary);
    font-size: 1.2rem;
    font-weight: 400;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Cargar datos una sola vez
if "datos_cargados" not in st.session_state:
    (st.session_state.clientes,
     st.session_state.personal,
     st.session_state.vehiculos,
     st.session_state.solicitudes,
     st.session_state.eventos,
     st.session_state.historias) = generar_datos()
    st.session_state.datos_cargados = True

clientes_df = st.session_state.clientes
personal_df = st.session_state.personal
vehiculos_df = st.session_state.vehiculos
solicitudes_df = st.session_state.solicitudes
eventos_df = st.session_state.eventos
historias_df = st.session_state.historias

# KPIs globales
total_solicitudes = len(solicitudes_df)
total_kg = solicitudes_df["cantidad_kg"].sum()

# Logo y navegación en el sidebar
with st.sidebar:
    try:
        logo = Image.open("LogoEcosynchro.jpg")
        st.image(logo, use_container_width=True)
    except Exception:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: #10b981; margin: 0;">EcoSynchro</h2>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Gestión Ambiental Inteligente</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "**Navegación**",
        ["Dashboard", "Estadísticas", "Solicitudes", "Personal", "Vehículos", "Historias"],
        index=0,
    )

# Header principal mejorado
st.markdown("""
<div class="header-container">
    <h1>EcoSynchro</h1>
    <div class="subtitle">La tecnología al servicio de un planeta eficiente</div>
</div>
""", unsafe_allow_html=True)

# Función auxiliar
def join_solicitudes_clientes(df_s):
    return df_s.merge(clientes_df, on="id_cliente", how="left", suffixes=("", "_cliente"))

# ==========================
# SECCIONES DE LA APLICACIÓN
# ==========================

if menu == "Dashboard":
    st.header("Dashboard de Trazabilidad")
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    pct_finalizadas = (len(solicitudes_df[solicitudes_df["estado"] == "Finalizada"]) /
                       total_solicitudes * 100) if total_solicitudes > 0 else 0
    incidencias = len(solicitudes_df[solicitudes_df["estado"] == "Incidencia"])
    
    with col1:
        st.metric("Solicitudes", total_solicitudes, delta="Total registradas")
    with col2:
        st.metric("Kg Gestionados", f"{total_kg:,}", delta="Residuos procesados")
    with col3:
        st.metric("Finalizadas", f"{pct_finalizadas:.1f}%", delta="Tasa de éxito")
    with col4:
        st.metric("Incidencias", incidencias, delta="Casos especiales")
    
    st.markdown("---")
    
    # Filtros con toggle
    show_filters = st.toggle("Mostrar filtros")
    
    if show_filters:
        st.markdown("**Personaliza los datos mostrados:**")
        
        colf1, colf2, colf3 = st.columns(3)
        
        with colf1:
            filtro_tipo_evento = st.multiselect(
                "Tipo de Evento",
                options=eventos_df["tipo_evento"].unique().tolist(),
                default=eventos_df["tipo_evento"].unique().tolist(),
                help="Selecciona los tipos de eventos a mostrar"
            )
        with colf2:
            filtro_ciudad = st.multiselect(
                "Ciudad",
                options=CIUDADES,
                default=CIUDADES,
                help="Filtra por ubicación geográfica"
            )
        with colf3:
            filtro_estado = st.multiselect(
                "Estado de Solicitud",
                options=solicitudes_df["estado"].unique().tolist(),
                default=solicitudes_df["estado"].unique().tolist(),
                help="Filtra por estado del proceso"
            )
    else:
        # Valores por defecto cuando los filtros están ocultos
        filtro_tipo_evento = eventos_df["tipo_evento"].unique().tolist()
        filtro_ciudad = CIUDADES
        filtro_estado = solicitudes_df["estado"].unique().tolist()
    
    # Datos filtrados
    ev_sol = eventos_df.merge(solicitudes_df, on="id_solicitud", how="left", suffixes=("", "_sol"))
    ev_sol_cli = ev_sol.merge(clientes_df, on="id_cliente", how="left", suffixes=("", "_cli"))
    
    df_filtrado = ev_sol_cli[
        (ev_sol_cli["tipo_evento"].isin(filtro_tipo_evento)) &
        (ev_sol_cli["ciudad"].isin(filtro_ciudad)) &
        (ev_sol_cli["estado"].isin(filtro_estado))
    ].copy()
    
    df_mostrar = df_filtrado[[
        "id_evento", "tipo_evento", "fecha_evento",
        "nombre_cliente", "ciudad", "tipo_residuo",
        "cantidad_kg", "estado", "descripcion_evento",
        "usuario_responsable"
    ]].sort_values("fecha_evento", ascending=False)
    
    st.subheader("Histórico de Eventos")
    st.dataframe(df_mostrar, use_container_width=True, height=400)
    
    st.info("Este dashboard integra eventos en tiempo real para trazabilidad completa y transparencia con los clientes.")

elif menu == "Estadísticas":
    st.header("Estadísticas y Análisis")
    
    # KPIs superiores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Solicitudes", total_solicitudes)
    with col2:
        avg_kg = (total_kg / total_solicitudes) if total_solicitudes > 0 else 0
        st.metric("Promedio por Solicitud", f"{avg_kg:.1f} kg")
    with col3:
        num_empresas = len(clientes_df[clientes_df["tipo_cliente"] == "Empresa"])
        st.metric("Clientes Empresariales", num_empresas)
    
    st.markdown("---")
    
    # Gráficos mejorados
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución por Tipo de Residuo")
        kg_por_residuo = solicitudes_df.groupby("tipo_residuo")["cantidad_kg"].sum()
        if not kg_por_residuo.empty:
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            colors = ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5', '#ecfdf5', '#f0fdfa']
            ax1.pie(kg_por_residuo.values, labels=kg_por_residuo.index, autopct="%1.1f%%", 
                   startangle=90, colors=colors[:len(kg_por_residuo)])
            ax1.axis("equal")
            st.pyplot(fig1)
        else:
            st.write("Sin datos disponibles")
    
    with col2:
        st.subheader("Solicitudes por Ciudad")
        sol_por_ciudad = join_solicitudes_clientes(solicitudes_df).groupby("ciudad")["id_solicitud"].count()
        st.bar_chart(sol_por_ciudad)
    
    # Indicadores de calidad
    st.markdown("---")
    st.subheader("Indicadores de Calidad")
    
    col1, col2 = st.columns(2)
    with col1:
        total_opiniones = solicitudes_df["opinion_cliente"].notna().sum()
        incidencias = len(solicitudes_df[solicitudes_df["estado"] == "Incidencia"])
        pct_incidencias = (incidencias / total_solicitudes * 100) if total_solicitudes > 0 else 0.0
        
        st.write(f"**Opiniones registradas:** {total_opiniones}")
        st.write(f"**Porcentaje de incidencias:** {pct_incidencias:.1f}%")
        
        if pct_incidencias > 20:
            st.warning("Alto porcentaje de incidencias. Revisar operaciones.")
        else:
            st.success("Incidencias bajo control.")
    
    with col2:
        if not kg_por_residuo.empty:
            top_residuo = kg_por_residuo.idxmax()
            st.write(f"**Residuo principal:** {top_residuo}")
        if not sol_por_ciudad.empty:
            top_ciudad = sol_por_ciudad.idxmax()
            st.write(f"**Ciudad más activa:** {top_ciudad}")

elif menu == "Solicitudes":
    st.header("Gestión de Solicitudes")
    
    estados_activos = ["Solicitada", "Pendiente", "En tránsito", "Incidencia", "Rechazada"]
    sol_activas = solicitudes_df[solicitudes_df["estado"].isin(estados_activos)].copy()
    joined = join_solicitudes_clientes(sol_activas)
    
    st.caption("Solicitudes pendientes de finalización")
    
    # Filtros con toggle
    show_filters_sol = st.toggle("Mostrar filtros ")
    
    if show_filters_sol:
        st.markdown("**Personaliza las solicitudes mostradas:**")
        
        col1, col2 = st.columns(2)
        with col1:
            filtro_ciudad = st.multiselect(
                "Filtrar por Ciudad", 
                CIUDADES, 
                default=CIUDADES,
                help="Selecciona las ciudades a mostrar"
            )
        with col2:
            filtro_estado = st.multiselect(
                "Filtrar por Estado", 
                estados_activos, 
                default=estados_activos,
                help="Filtra por estado de la solicitud"
            )
    else:
        # Valores por defecto cuando los filtros están ocultos
        filtro_ciudad = CIUDADES
        filtro_estado = estados_activos
    
    joined_filtrado = joined[
        (joined["ciudad"].isin(filtro_ciudad)) &
        (joined["estado"].isin(filtro_estado))
    ]
    
    st.dataframe(
        joined_filtrado[[
            "id_solicitud", "nombre_cliente", "ciudad",
            "tipo_residuo", "cantidad_kg", "estado",
            "fecha_programada", "ruta_asignada"
        ]],
        use_container_width=True
    )
    
    # Detalle de solicitud
    if not joined_filtrado.empty:
        st.markdown("---")
        st.subheader("Detalle de Solicitud")
        
        seleccion = st.selectbox("Seleccionar solicitud:", joined_filtrado["id_solicitud"].tolist())
        detalle = joined_filtrado[joined_filtrado["id_solicitud"] == seleccion].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Cliente:** {detalle['nombre_cliente']}")
            st.markdown(f"**Tipo:** {detalle['tipo_cliente']}")
            st.markdown(f"**Ciudad:** {detalle['ciudad']}")
            st.markdown(f"**Residuo:** {detalle['tipo_residuo']}")
            st.markdown(f"**Cantidad:** {detalle['cantidad_kg']} kg")
            st.markdown(f"**Estado:** {detalle['estado']}")
        
        with col2:
            if pd.notna(detalle["foto_evidencia"]):
                st.image(detalle["foto_evidencia"], caption="Evidencia fotográfica", use_container_width=True)
            else:
                st.info("Sin evidencia fotográfica disponible")

elif menu == "Personal":
    st.header("Gestión de Personal")
    
    st.dataframe(
        personal_df[[
            "id_personal", "nombre", "rol", "ciudad_base",
            "activo", "en_servicio_ahora", "quejas_recibidas",
            "incidencias_resueltas"
        ]],
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("Perfil del Personal")
    
    seleccion = st.selectbox("Seleccionar persona:", personal_df["id_personal"])
    persona = personal_df[personal_df["id_personal"] == seleccion].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Nombre:** {persona['nombre']}")
        st.markdown(f"**Rol:** {persona['rol']}")
        st.markdown(f"**Ciudad:** {persona['ciudad_base']}")
        st.markdown(f"**Activo:** {'Sí' if persona['activo'] else 'No'}")
    
    with col2:
        st.markdown(f"**En servicio:** {'Sí' if persona['en_servicio_ahora'] else 'No'}")
        st.markdown(f"**Quejas:** {persona['quejas_recibidas']}")
        st.markdown(f"**Incidencias resueltas:** {persona['incidencias_resueltas']}")
    
    st.markdown("**Comentarios:**")
    st.write(persona["comentarios_internos"])

elif menu == "Vehículos":
    st.header("Gestión de Flota")
    
    st.dataframe(
        vehiculos_df[[
            "id_vehiculo", "placa", "tipo", "año", "estado_actual",
            "ubicacion_actual", "soat_vigente"
        ]],
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("Ubicación de Vehículos")
    
    mapa_df = vehiculos_df[["lat", "lon"]].dropna()
    if not mapa_df.empty:
        st.map(mapa_df, zoom=5)
    else:
        st.info("Sin coordenadas GPS configuradas")

elif menu == "Historias":
    st.header("Casos de Éxito")
    
    st.caption("Testimonios de clientes satisfechos con EcoSynchro")
    
    for _, row in historias_df.sort_values("fecha_publicacion", ascending=False).iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(row["portada_imagen"], use_container_width=True)
            
            with col2:
                st.subheader(row["titulo_publicacion"])
                st.markdown(f"**Cliente:** {row['cliente_visible']}")
                st.markdown(f"**Ciudad:** {row['ciudad']}")
                st.markdown(f"**Fecha:** {row['fecha_publicacion']:%Y-%m-%d}")
                st.write(row["resumen_situacion"])
                st.markdown(f"*{row['frase_del_cliente']}*")
                st.markdown(f"*{row['frase_del_recolector']}*")
        
        st.markdown("---")