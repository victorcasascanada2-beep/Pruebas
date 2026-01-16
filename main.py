import streamlit as st
from gestor_ia import ejecutar_tasacion_v2
from usuarios import validar_usuario

st.set_page_config(page_title="Peritaje Profesional V2.0", layout="wide")

# --- CONTROL DE ACCESO ---
if 'vendedor' not in st.session_state:
    st.session_state.vendedor = None

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

# --- INTERFAZ ORIGINAL ---
st.title(f"🚜 Peritaje Profesional V2.0 - {st.session_state.vendedor['nombre']}")

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

if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        try:
            with st.spinner(f'🔍 {st.session_state.vendedor["nombre"]}, estamos analizando los portales europeos...'):
                resultado_texto = ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas)
                
            st.success("✅ Tasación Finalizada con éxito")
            st.markdown(resultado_texto)
            
            # Aquí ya tenemos el nombre del mecánico para el futuro log/drive
            st.info(f"Informe preparado por: {st.session_state.vendedor['nombre']}")
            
        except Exception as e:
            st.error(f"❌ Error en el motor de tasación: {e}")
