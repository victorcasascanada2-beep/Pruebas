import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la App
st.set_page_config(page_title="Tasador Tractor Pro", layout="centered")
st.title("🚜 Tasador Experto")

# Barra lateral para la clave
api_key = st.sidebar.text_input("Pega tu API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # CAMBIO CLAVE: Usamos el nombre del modelo sin versiones extra
        model = genai.GenerativeModel('gemini-1.5-flash')

        with st.form("tasacion_unica"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas de motor *", min_value=0)
            estado = st.text_area("Descripción de averías *")
            
            # Solo una foto para evitar fallos de memoria
            foto = st.file_uploader("Sube la foto principal *", type=['jpg', 'jpeg', 'png'])
            
            if foto:
                st.image(Image.open(foto), width=250)

            submit = st.form_submit_button("GENERAR VALORACIÓN")

        if submit:
            if not (modelo and estado and foto):
                st.error("⚠️ Rellena todos los campos y sube la foto.")
            else:
                with st.spinner("La IA está tasando..."):
                    img = Image.open(foto)
                    # Tu regla: 10.000€ y 100 horas
                    prompt = f"""
                    Actúa como tasador experto agrícola. Analiza: {modelo}, {horas}h, {estado}. 
                    REGLA ORO: Si hay averías graves, resta 10.000€ y 100h de mano de obra al valor.
                    Da un precio para el mercado de 2026.
                    """
                    response = model.generate_content([prompt, img])
                    st.success("✅ Tasación Completada")
                    st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Escribe la API Key a la izquierda.")
