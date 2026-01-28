import streamlit as st
from gestor_ia import ejecutar_tasacion_v2
from usuarios import validar_usuario
from generador_informe import crear_html_descargable 
from gestor_drive import guardar_todo_en_drive # Importamos el nuevo gestor
from datetime import datetime

st.set_page_config(page_title="Peritaje Profesional V2.0", layout="wide")

# Ocultar menús de Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. INICIALIZACIÓN DE MEMORIA ---
if 'vendedor' not in st.session_state:
    st.session_state.vendedor = None
if 'ultima_tasacion' not in st.session_state:
    st.session_state.ultima_tasacion = None
if 'nombre_carpeta_drive' not in st.session_state:
    st.session_state.nombre_carpeta_drive = None

# --- 2. CONTROL DE ACCESO ---
if not st.session_state.vendedor:
    st.title("🚜 Acceso al Sistema")
    codigo = st.text_input("Introduce tu código de empleado")
    if st.button("Entrar"):
        user = validar_usuario(codigo)
        if user:
            st.session_state.vendedor = user
            st.rerun()
        else:
            st.error("Código incorrecto")
    st.stop()

# --- 3. INTERFAZ DE USUARIO ---
st.title(f"🚜 Peritaje Profesional V2.0 - {st.session_state.vendedor['nombre']}")

with st.sidebar:
    st.write(f"👤 Usuario: **{st.session_state.vendedor['nombre']}**")
    if st.button("🗑️ Nueva Tasación (Limpiar)"):
        st.session_state.ultima_tasacion = None
        st.session_state.nombre_carpeta_drive = None
        st.rerun()
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.vendedor = None
        st.session_state.ultima_tasacion = None
        st.rerun()

c1, c2, c3, c4 = st.columns(4)
with c1: marca = st.text_input("Marca*", key="marca_v2")
with c2: modelo = st.text_input("Modelo*", key="modelo_v2")
with c3: anio = st.text_input("Año*", key="anio_v2")
with c4: horas = st.number_input("Horas de uso*", min_value=0, key="horas_input")

observaciones = st.text_area("Incidencias y Extras", placeholder="Ej: Pala, averías, pintura...")

st.divider()

st.subheader("Fotografías (Mínimo 5)")
fotos_subidas = st.file_uploader("Sube tus fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos.")
    else:
        cols = st.columns(5)
        for i, foto in enumerate(fotos_subidas):
            with cols[i % 5]:
                st.image(foto, width=150)

st.divider()

# --- 4. LÓGICA DE EJECUCIÓN ---
if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        try:
            with st.spinner(f'🔍 Analizando fotos (optimizado) y consultando IA...'):
                # 1. IA: Ejecuta tasación (usará fotos reducidas internamente en gestor_ia.py)
                resultado_texto = ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas)
                st.session_state.ultima_tasacion = resultado_texto
                
                # 2. GENERAR INFORME: Creamos el HTML con fotos originales
                documento_html = crear_html_descargable(marca, modelo, resultado_texto, fotos_subidas)
                
                # 3. DRIVE: Guardar todo en la carpeta con formato fecha/hora
                exito_drive, info_drive = guardar_todo_en_drive(fotos_subidas, documento_html)
                
                if exito_drive:
                    st.session_state.nombre_carpeta_drive = info_drive
                else:
                    st.error(f"Error al guardar en Drive: {info_drive}")
                    
        except Exception as e:
            st.error(f"❌ Error en el proceso: {e}")

# --- 5. MOSTRAR RESULTADOS ---
if st.session_state.ultima_tasacion:
    st.success("✅ Tasación Finalizada con éxito")
    
    if st.session_state.nombre_carpeta_drive:
        st.info(f"📂 Archivos guardados en Drive (Carpeta: {st.session_state.nombre_carpeta_drive})")
    
    st.markdown(st.session_state.ultima_tasacion)
    
    # Botón de descarga local por si acaso
    documento_html = crear_html_descargable(marca, modelo, st.session_state.ultima_tasacion, fotos_subidas)
    st.download_button(
        label="📥 Descargar Copia del Informe (HTML)",
        data=documento_html,
        file_name=f"Tasacion_{marca}_{modelo}.html",
        mime="text/html"
    )
