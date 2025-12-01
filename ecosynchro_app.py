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
         None, None,
         None,
         False, None, None,
         hoy - timedelta(days=3)],
        ["S004", "C004", "Papel", 60, hoy - timedelta(days=1),
         hoy + timedelta(days=4), "Solicitada", None,
         None, None,
         None,
         False, None, None,
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
         "https://images.pexels.com/photos/1260402/pexels-photo-1260402.jpeg",
         "EcoAndes y EcoSynchro: RAEE con propósito",
         "EcoAndes Reciclaje S.A.S.",
         "Bogotá",
         "EcoAndes confió en EcoSynchro para gestionar de forma responsable sus residuos electrónicos, garantizando trazabilidad y disposición final certificada.",
         "“Es clave poder demostrarle a nuestros clientes que nuestros residuos tienen un destino responsable.”",
         "“Saber que nuestro trabajo cuida al planeta y sostiene a nuestras familias nos motiva cada día.”",
         hoy - timedelta(days=1),
         "https://example.com/historias/ecoandes"],
        ["H002", "S002",
         "https://images.pexels.com/photos/3735210/pexels-photo-3735210.jpeg",
         "BioTechNova reduce su huella con EcoSynchro",
         "BioTechNova S.A.S.",
         "Medellín",
         "BioTechNova integró la recolección de baterías usadas al modelo de EcoSynchro, fortaleciendo su compromiso con la sostenibilidad.",
         "“No solo cumplimos la norma, ahora podemos mostrarlo con datos.”",
         "“Cada ruta bien planificada es tiempo ganado y menos estrés en la vía.”",
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

# KPIs globales (para que no dé error en ninguna sección)
total_solicitudes = len(solicitudes_df)
total_kg = solicitudes_df["cantidad_kg"].sum()

st.set_page_config(
    page_title="EcoSynchro",
    page_icon="♻️",
    layout="wide"
)

# ==========================
# ESTILOS (CSS)
# ==========================
st.markdown("""
<style>

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #021c13, #064930);
    padding-top: 0.5rem;
    color: #eafff5;
}

/* Todo lo que esté adentro del sidebar */
[data-testid="stSidebar"] * {
    color: #eafff5 !important;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Títulos generales (app) en tonos verdes */
h1, h2, h3 {
    color: #c4f8dd !important;
}

/* Pequeño ajuste a subtítulos / captions */
p, span, label {
    color: #e3f6ee;
}

/* Contenedor del grupo de radios del menú (6 opciones) */
[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.4rem;
}

/* Cada opción del menú como tarjeta */
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    border-radius: 14px;
    padding: 0.55rem 0.9rem;
    border: 1px solid rgba(225, 255, 245, 0.18);
    background: rgba(3, 60, 40, 0.55);
    cursor: pointer;
    transition: all 0.15s ease-in-out;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
}

/* Hover del menú */
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(31, 155, 109, 0.90);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.45);
}

/* Estado seleccionado del radio (la “tarjeta activa”) */
[data-testid="stSidebar"] div[role="radio"][aria-checked="true"] {
    background: linear-gradient(90deg, #27c47f, #1c9a68);
    border-radius: 14px;
    box-shadow: 0 0 14px rgba(39, 196, 127, 0.75);
}

/* Oculta el círculo típico del radio para que parezca solo tarjeta */
[data-testid="stSidebar"] div[role="radio"] > div:first-child {
    display: none;
}

/* ===== TAGS DE MULTISELECT (para que dejen de ser rojos) ===== */
[data-baseweb="tag"] {
    background-color: #1f9b6d !important;  /* verde principal */
    color: #eafff5 !important;
    border-radius: 999px !important;
    border: none !important;
    padding: 0.15rem 0.6rem !important;
    font-weight: 500;
}

/* texto interno del tag */
[data-baseweb="tag"] span {
    color: #eafff5 !important;
}

/* Botoncito de “x” en los tags */
[data-baseweb="tag"] svg {
    fill: #eafff5 !important;
}

/* Fondo de los cuadros de filtros (contenedor del multiselect) */
[data-testid="stMultiSelect"] > div {
    background-color: #141b1a !important;
    border-radius: 18px !important;
}

/* Etiquetas de los filtros */
[data-testid="stMultiSelect"] label p {
    color: #c4f8dd !important;
    font-weight: 500;
}

/* ===== Ajustes generales del cuerpo ===== */
body {
    color: #e3f6ee;
}

/* Tablas ligeramente más integradas con la paleta */
[data-testid="stTable"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Tooltips / mensajes informativos */
.stAlert > div {
    background-color: rgba(17, 92, 63, 0.25) !important;
    border: 1px solid rgba(39, 196, 127, 0.6) !important;
}
</style>
""", unsafe_allow_html=True)


# Logo en el sidebar
with st.sidebar:
    try:
        logo = Image.open("LogoEcosynchro.jpg")
        st.image(logo, use_container_width=True)
    except Exception:
        st.markdown("### EcoSynchro ♻️")
    st.markdown("#### Navegación")

    menu = st.radio(
        "",
        ["DataLake", "Estadísticas", "Solicitudes", "Personal", "Vehículos", "Historias"],
        index=0,
    )

# Título principal
st.title("EcoSynchro ♻️")
st.caption("La tecnología al servicio de un planeta eficiente")

# Función auxiliar
def join_solicitudes_clientes(df_s):
    return df_s.merge(clientes_df, on="id_cliente", how="left",
                      suffixes=("", "_cliente"))

# ==========================
# 1. DATALAKE
# ==========================
if menu == "DataLake":
    st.header("DataLake de trazabilidad")

    col1, col2, col3, col4 = st.columns(4)
    pct_finalizadas = (len(solicitudes_df[solicitudes_df["estado"] == "Finalizada"]) /
                       total_solicitudes * 100) if total_solicitudes > 0 else 0
    incidencias = len(solicitudes_df[solicitudes_df["estado"] == "Incidencia"])

    col1.metric("Solicitudes registradas", total_solicitudes)
    col2.metric("Kg gestionados (total)", f"{total_kg} kg")
    col3.metric("Solicitudes finalizadas", f"{pct_finalizadas:.1f} %")
    col4.metric("Solicitudes con incidencia", incidencias)

    st.markdown("---")
    st.subheader("Histórico de eventos (vista DataLake)")

    colf1, colf2, colf3 = st.columns(3)
    filtro_tipo_evento = colf1.multiselect(
        "Filtrar por tipo de evento",
        options=eventos_df["tipo_evento"].unique().tolist(),
        default=eventos_df["tipo_evento"].unique().tolist()
    )
    filtro_ciudad = colf2.multiselect(
        "Filtrar por ciudad",
        options=CIUDADES,
        default=CIUDADES
    )
    filtro_estado = colf3.multiselect(
        "Filtrar por estado de solicitud",
        options=solicitudes_df["estado"].unique().tolist(),
        default=solicitudes_df["estado"].unique().tolist()
    )

    ev_sol = eventos_df.merge(solicitudes_df, on="id_solicitud", how="left",
                              suffixes=("", "_sol"))
    ev_sol_cli = ev_sol.merge(clientes_df, on="id_cliente", how="left",
                              suffixes=("", "_cli"))

    df_filtrado = ev_sol_cli[
        (ev_sol_cli["tipo_evento"].isin(filtro_tipo_evento)) &
        (ev_sol_cli["ciudad"].isin(filtro_ciudad)) &
        (ev_sol_cli["estado"].isin(filtro_estado))
    ].copy()

    df_mostrar = df_filtrado[[
        "id_evento", "tipo_evento", "fecha_evento",
        "nombre_cliente", "ciudad", "tipo_residuo",
        "cantidad_kg", "estado", "descripcion_evento",
        "usuario_responsable", "link_archivo"
    ]].sort_values("fecha_evento", ascending=False)

    st.dataframe(df_mostrar, use_container_width=True)

    st.info(
        "Este DataLake integra eventos de creación, programación, cambios de estado, "
        "incidencias y cierres para cada solicitud. Sobre esta base se construyen KPIs "
        "de operación, auditoría y transparencia para los clientes."
    )

# ==========================
# 2. ESTADÍSTICAS
# ==========================
elif menu == "Estadísticas":
    st.header("Estadísticas y retroalimentación")

    # KPIs arriba
    col0_1, col0_2, col0_3 = st.columns(3)
    col0_1.metric("Total de solicitudes", total_solicitudes)
    col0_2.metric("Kg promedio por solicitud",
                  f"{(total_kg / total_solicitudes):.1f} kg" if total_solicitudes > 0 else "0 kg")
    num_empresas = len(clientes_df[clientes_df["tipo_cliente"] == "Empresa"])
    col0_3.metric("Clientes empresariales", num_empresas)

    st.markdown("---")

    colg1, colg2 = st.columns(2)

    # Pie + barras
    with colg1:
        st.subheader("Distribución de kg por tipo de residuo (torta)")
        kg_por_residuo = solicitudes_df.groupby("tipo_residuo")["cantidad_kg"].sum()
        if not kg_por_residuo.empty:
            fig1, ax1 = plt.subplots()
            ax1.pie(kg_por_residuo.values,
                    labels=kg_por_residuo.index,
                    autopct="%1.1f%%",
                    startangle=90)
            ax1.axis("equal")
            st.pyplot(fig1)
        else:
            st.write("Aún no hay datos de residuos.")

    with colg2:
        st.subheader("Solicitudes por ciudad (barras)")
        sol_por_ciudad = join_solicitudes_clientes(solicitudes_df).groupby("ciudad")["id_solicitud"].count()
        st.bar_chart(sol_por_ciudad)

    st.markdown("---")

    colg3, colg4 = st.columns(2)
    with colg3:
        st.subheader("Distribución por estado de solicitud")
        estado_counts = solicitudes_df["estado"].value_counts()
        st.bar_chart(estado_counts)

    with colg4:
        st.subheader("Indicadores de calidad")
        total_opiniones = solicitudes_df["opinion_cliente"].notna().sum()
        st.write(f"- Opiniones registradas: **{total_opiniones}**")

        incidencias = len(solicitudes_df[solicitudes_df["estado"] == "Incidencia"])
        pct_incidencias = (incidencias / total_solicitudes * 100) if total_solicitudes > 0 else 0.0
        st.write(f"- Porcentaje de solicitudes con incidencia: **{pct_incidencias:.1f} %**")

        if pct_incidencias > 20:
            st.warning("Advertencia: el porcentaje de incidencias es alto. Se recomienda revisar rutas y recursos.")
        else:
            st.success("Las incidencias se mantienen en un nivel controlado.")

        # Insight rápido
        if not kg_por_residuo.empty:
            top_residuo = kg_por_residuo.idxmax()
            st.write(f"- Residuo con mayor volumen gestionado: **{top_residuo}**")
        if not sol_por_ciudad.empty:
            top_ciudad = sol_por_ciudad.idxmax()
            st.write(f"- Ciudad más activa en solicitudes: **{top_ciudad}**")

    st.markdown("---")
    st.subheader("Retroalimentaciones de clientes")

    opiniones = solicitudes_df.dropna(subset=["opinion_cliente"])
    if opiniones.empty:
        st.write("Aún no hay opiniones registradas.")
    else:
        joined = join_solicitudes_clientes(opiniones)
        for _, row in joined.iterrows():
            st.markdown(
                f"**{row['nombre_cliente']}** ({row['ciudad']}) — "
                f"*{row['tipo_residuo']}, {row['cantidad_kg']} kg*"
            )
            st.write(f"“{row['opinion_cliente']}”")
            st.markdown("---")

# ==========================
# 3. SOLICITUDES
# ==========================
elif menu == "Solicitudes":
    st.header("Solicitudes activas y en proceso")

    estados_activos = ["Solicitada", "Pendiente", "En tránsito", "Incidencia", "Rechazada"]
    sol_activas = solicitudes_df[solicitudes_df["estado"].isin(estados_activos)].copy()
    joined = join_solicitudes_clientes(sol_activas)

    st.caption("Lista de solicitudes que aún no están completamente finalizadas.")

    colf1, colf2 = st.columns(2)
    filtro_ciudad = colf1.multiselect(
        "Filtrar por ciudad",
        options=CIUDADES,
        default=CIUDADES
    )
    filtro_estado = colf2.multiselect(
        "Filtrar por estado",
        options=estados_activos,
        default=estados_activos
    )

    joined_filtrado = joined[
        (joined["ciudad"].isin(filtro_ciudad)) &
        (joined["estado"].isin(filtro_estado))
    ]

    st.dataframe(
        joined_filtrado[[
            "id_solicitud", "nombre_cliente", "ciudad",
            "tipo_residuo", "cantidad_kg", "estado",
            "fecha_programada", "ruta_asignada", "persona_encargada_recoleccion"
        ]],
    use_container_width=True
    )

    st.markdown("---")
    st.subheader("Detalle de una solicitud")

    ids_disponibles = joined_filtrado["id_solicitud"].tolist()
    if ids_disponibles:
        seleccion = st.selectbox("Selecciona una solicitud", ids_disponibles)
        detalle = joined_filtrado[joined_filtrado["id_solicitud"] == seleccion].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Cliente:** {detalle['nombre_cliente']} ({detalle['tipo_cliente']})")
            st.markdown(f"**Ciudad:** {detalle['ciudad']}")
            st.markdown(f"**Dirección:** {detalle['direccion']}")
            st.markdown(f"**Residuo:** {detalle['tipo_residuo']}")
            st.markdown(f"**Cantidad:** {detalle['cantidad_kg']} kg")
            st.markdown(f"**Estado actual:** {detalle['estado']}")
            st.markdown(f"**Ruta asignada:** {detalle['ruta_asignada'] or 'No asignada'}")
            st.markdown(f"**Encargado/a:** {detalle['persona_encargada_recoleccion'] or 'Por asignar'}")

        with col2:
            st.markdown("**Evidencia:**")
            if pd.notna(detalle["foto_evidencia"]):
                st.image(detalle["foto_evidencia"], use_container_width=True)
            else:
                st.write("Sin imagen disponible.")

            if pd.notna(detalle["link_documento_evidencia"]):
                st.markdown(f"[Documento de evidencia]({detalle['link_documento_evidencia']})")
            if detalle["certificado_emitido"]:
                st.markdown(f"[Certificado emitido]({detalle['link_certificado']})")

        st.markdown("---")
        st.markdown("### Timeline de eventos")

        eventos_s = eventos_df[eventos_df["id_solicitud"] == seleccion].sort_values("fecha_evento")
        if eventos_s.empty:
            st.write("Aún no hay eventos registrados para esta solicitud.")
        else:
            for _, ev in eventos_s.iterrows():
                st.markdown(f"**{ev['tipo_evento']}** — {ev['fecha_evento']:%Y-%m-%d %H:%M}")
                st.write(ev["descripcion_evento"])
                if pd.notna(ev["link_archivo"]):
                    st.markdown(f"[Ver detalle]({ev['link_archivo']})")
                st.markdown("---")

        st.info(
            "En una versión plenamente productiva, estos flujos actualizarían el estado en tiempo real "
            "y alimentarían automáticamente el DataLake para analítica avanzada."
        )

    else:
        st.write("No hay solicitudes activas con los filtros actuales.")

# ==========================
# 4. PERSONAL
# ==========================
elif menu == "Personal":
    st.header("Personal vinculado a EcoSynchro")

    st.dataframe(
        personal_df[[
            "id_personal", "nombre", "rol", "ciudad_base",
            "activo", "en_servicio_ahora", "quejas_recibidas",
            "incidencias_resueltas"
        ]],
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Detalle de una persona")

    seleccion = st.selectbox("Selecciona a un miembro del personal", personal_df["id_personal"])
    persona = personal_df[personal_df["id_personal"] == seleccion].iloc[0]

    st.markdown(f"**Nombre:** {persona['nombre']}")
    st.markdown(f"**Rol:** {persona['rol']}")
    st.markdown(f"**Ciudad base:** {persona['ciudad_base']}")
    st.markdown(f"**Activo:** {'Sí' if persona['activo'] else 'No'}")
    st.markdown(f"**En servicio ahora:** {'Sí' if persona['en_servicio_ahora'] else 'No'}")
    st.markdown(f"**Quejas recibidas:** {persona['quejas_recibidas']}")
    st.markdown(f"**Incidencias resueltas:** {persona['incidencias_resueltas']}")
    st.markdown("**Comentarios internos:**")
    st.write(persona["comentarios_internos"])

    sol_rel = solicitudes_df[solicitudes_df["persona_encargada_recoleccion"] == persona["id_personal"]]
    st.markdown("### Solicitudes asociadas")
    if sol_rel.empty:
        st.write("Aún no hay solicitudes asignadas directamente a esta persona.")
    else:
        joined_rel = join_solicitudes_clientes(sol_rel)
        st.dataframe(
            joined_rel[["id_solicitud", "nombre_cliente", "ciudad", "tipo_residuo", "cantidad_kg", "estado"]],
            use_container_width=True
        )

# ==========================
# 5. VEHÍCULOS
# ==========================
elif menu == "Vehículos":
    st.header("Vehículos y estado de la flota")

    st.dataframe(
        vehiculos_df[[
            "id_vehiculo", "placa", "tipo", "año", "estado_actual",
            "ubicacion_actual", "soat_vigente", "fecha_vencimiento_soat",
            "ultima_revision_mantenimiento"
        ]],
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Mapa de ubicación aproximada de vehículos operativos")

    mapa_df = vehiculos_df[["lat", "lon"]].dropna()
    if not mapa_df.empty:
        st.map(mapa_df, zoom=5)
    else:
        st.write("No hay coordenadas configuradas para los vehículos.")

    st.markdown("---")
    st.subheader("Detalle de un vehículo")

    seleccion = st.selectbox("Selecciona un vehículo", vehiculos_df["id_vehiculo"])
    veh = vehiculos_df[vehiculos_df["id_vehiculo"] == seleccion].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Placa:** {veh['placa']}")
        st.markdown(f"**Tipo:** {veh['tipo']}")
        st.markdown(f"**Año:** {veh['año']}")
        st.markdown(f"**Estado actual:** {veh['estado_actual']}")
        st.markdown(f"**Ubicación actual:** {veh['ubicacion_actual']}")
        st.markdown(f"**Tiempo de operación:** {veh['tiempo_operacion_horas']} horas")

    with col2:
        st.markdown("**Información legal y mantenimiento**")
        st.markdown(f"- SOAT vigente: {'Sí' if veh['soat_vigente'] else 'No'}")
        st.markdown(f"- Vence SOAT: {veh['fecha_vencimiento_soat']:%Y-%m-%d}")
        st.markdown(f"- Última revisión: {veh['ultima_revision_mantenimiento']:%Y-%m-%d}")
        st.markdown(f"- Problemas reportados: {veh['problemas_reportados']}")
        st.markdown(f"- Trabajos realizados: {veh['trabajos_realizados']}")

# ==========================
# 6. HISTORIAS
# ==========================
elif menu == "Historias":
    st.header("Historias públicas y reputación ambiental")

    st.caption("Casos de éxito de empresas y personas que han trabajado con EcoSynchro y aceptan hacer pública su experiencia.")

    for _, row in historias_df.sort_values("fecha_publicacion", ascending=False).iterrows():
        st.markdown("----")
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(row["portada_imagen"], use_container_width=True)
        with cols[1]:
            st.subheader(row["titulo_publicacion"])
            st.markdown(f"**Cliente:** {row['cliente_visible']} — {row['ciudad']}")
            st.markdown(f"**Fecha:** {row['fecha_publicacion']:%Y-%m-%d}")
            st.markdown(row["resumen_situacion"])
            st.markdown(f"💬 Cliente: {row['frase_del_cliente']}")
            st.markdown(f"🚚 Recolector: {row['frase_del_recolector']}")
            if pd.notna(row["link_externo"]):
                st.markdown(f"[Ver más detalles]({row['link_externo']})")
