import streamlit as st
from gestor_ia import ejecutar_tasacion_v2
from usuarios import validar_usuario
from generador_informe import crear_html_descargable
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Peritaje Pro V2.0", layout="wide")

# --- 1. INICIALIZACIÓN ---
if 'vendedor' not in st.session_state:
    st.session_state.vendedor = None
if 'ultima_tasacion' not in st.session_state:
    st.session_state.ultima_tasacion = None

# --- 2. ACCESO ---
if not st.session_state.vendedor:
    st.title("🚜 Acceso")
    codigo = st.text_input("Código de empleado", type="password")
    if st.button("Entrar"):
        user = validar_usuario(codigo)
        if user:
            st.session_state.vendedor = user
            st.rerun()
        else:
            st.error("Código incorrecto")
    st.stop()

# --- 3. INTERFAZ ---
st.title(f"🚜 Peritaje - {st.session_state.vendedor['nombre']}")

with st.sidebar:
    if st.button("🗑️ Nueva Tasación"):
        st.session_state.ultima_tasacion = None
        st.rerun()

marca = st.text_input("Marca*")
modelo = st.text_input("Modelo*")
anio = st.text_input("Año*")
horas = st.number_input("Horas de uso*", min_value=0)
observaciones = st.text_area("Notas")

fotos_subidas = st.file_uploader("Fotos (min 5)", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

# --- 4. EJECUCIÓN ---
if st.button("🚀 TASAR"):
    if not marca or not modelo or len(fotos_subidas) < 5:
        st.warning("⚠️ Datos incompletos o faltan fotos.")
    else:
        try:
            with st.spinner('🔍 Analizando...'):
                res = ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas)
                st.session_state.ultima_tasacion = res
        except Exception as e:
            st.error(f"Error: {e}")

# --- 5. RESULTADOS ---
if st.session_state.ultima_tasacion:
    st.success("✅ Tasación lista")
    st.markdown(st.session_state.ultima_tasacion)
    
    try:
        html = crear_html_descargable(marca, modelo, st.session_state.ultima_tasacion, fotos_subidas)
        st.download_button("📥 Descargar Informe", data=html, file_name=f"{modelo}.html", mime="text/html")
    except:
        st.warning("El botón de descarga falló, pero tienes el resultado arriba.")
