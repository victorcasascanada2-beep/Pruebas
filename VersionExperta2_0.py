import streamlit as st
from gestor_ia import ejecutar_tasacion_v2
from usuarios import validar_usuario
from generador_informe import crear_html_descargable 
from gestor_drive import guardar_todo_en_drive 
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Peritaje Profesional V2.0", layout="wide")

# Ocultar menús de Streamlit para apariencia limpia
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. INICIALIZACIÓN DE MEMORIA (Session State) ---
if 'vendedor' not in st.session_state:
    st.session_state.vendedor = None
if 'ultima_tasacion' not in st.session_state:
    st.session_state.ultima_tasacion = None
if 'nombre_carpeta_drive' not in st.session_state:
    st.session_state.nombre_carpeta_drive = None

# --- 2. CONTROL DE ACCESO ---
if not st.session_state.vendedor:
    st.title("🚜 Acceso al Sistema")
    codigo = st.text_input("Introduce tu código de empleado", type="password")
    if st.button("Entrar"):
        user = validar_usuario(codigo)
        if user:
            st.session_state.vendedor = user
            st.rerun()
        else:
            st.error("Código incorrecto")
    st.stop()

# --- 3. INTERFAZ DE USUARIO ---
st.title(f"🚜 Peritaje Profesional V2.0")
st.write(f"Bienvenido, **{st.session_state.vendedor['nombre']}**")

# Sidebar de utilidades
with st.sidebar:
    st.header("Menú de Control")
    if st.button("🗑️ Nueva Tasación"):
        st.session_state.ultima_tasacion = None
        st.session_state.nombre_carpeta_drive = None
        st.rerun()
    st.divider()
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.vendedor = None
        st.session_state.ultima_tasacion = None
        st.rerun()

# Formulario de datos
c1, c2, c3, c4 = st.columns(4)
with c1: marca = st.text_input("Marca*", placeholder="Ej: John Deere")
with c2: modelo = st.text_input("Modelo*", placeholder="Ej: 6155M")
with c3: anio = st.text_input("Año*", placeholder="Ej: 2018")
with c4: horas = st.number_input("Horas de uso*", min_value=0)

observaciones = st.text_area("Incidencias y Extras", placeholder="Describe estado de neumáticos, pala, averías detectadas...")

st.divider()

# Subida de fotos
st.subheader("Fotografías del Vehículo (Mínimo 5)")
fotos_subidas = st.file_uploader("Arrastra aquí las fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Por favor, sube un máximo de 10 fotos.")
    else:
        cols = st.columns(5)
        for i, foto in enumerate(fotos_subidas):
            with cols[i % 5]:
                st.image(foto, width=150)

st.divider()

# --- 4. LÓGICA DE EJECUCIÓN ---
if st.button("🚀 REALIZAR TASACIÓN Y GUARDAR"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Faltan datos obligatorios (Marca, Modelo, Año, Horas).")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Se requieren al menos 5 fotos para un peritaje fiable.")
    else:
        try:
            with st.spinner('⚙️ Procesando tasación...'):
                # 1. Ejecutar IA (gestor_ia se encarga de reducir las fotos para la API)
                resultado_texto = ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas)
                st.session_state.ultima_tasacion = resultado_texto
                
                # 2. Generar Informe HTML con fotos ORIGINALES (Alta resolución)
                documento_html = crear_html_descargable(marca, modelo, resultado_texto, fotos_subidas)
                
                # 3. Guardar en Google Drive (Carpeta automática con fecha/hora)
                exito_drive, info_drive = guardar_todo_en_drive(fotos_subidas, documento_html)
                
                if exito_drive:
                    st.session_state.nombre_carpeta_drive = info_drive
                else:
                    st.error(f"Error al subir a Drive: {info_drive}")
                    
        except Exception as e:
            st.error(f"❌ Error crítico en el sistema: {e}")

# --- 5. VISUALIZACIÓN DE RESULTADOS ---
if st.session_state.ultima_tasacion:
    st.success("✅ Tasación Completada")
    
    if st.session_state.nombre_carpeta_drive:
        st.info(f"📂 Archivo histórico creado en Drive: Carpeta **{st.session_state.nombre_carpeta_drive}**")
    
    # Mostrar el veredicto de la IA
    st.markdown("---")
    st.markdown(st.session_state.ultima_tasacion)
    st.markdown("---")
    
    # Botón de descarga local
    documento_html = crear_html_descargable(marca, modelo, st.session_state.ultima_tasacion, fotos_subidas)
    st.download_button(
        label="📥 Descargar Informe HTML",
        data=documento_html,
        file_name=f"Informe_{marca}_{modelo}_{datetime.now().strftime('%d%m%y')}.html",
        mime="text/html"
    )
