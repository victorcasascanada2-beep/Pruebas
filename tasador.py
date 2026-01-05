import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la App
st.set_page_config(page_title="Tasador Express", layout="centered")
st.title("🚜 Tasador Pro (1 Sola Foto)")

# Barra lateral para la API KEY
api_key = st.sidebar.text_input("Introduce tu API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        with st.form("formulario_tasacion"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas de motor *", min_value=0)
            estado = st.text_area("Estado y Averías *")
            
            # CAMBIO CLAVE: accept_multiple_files=False (Solo una foto)
            foto = st.file_uploader("Sube la foto del tractor *", type=['jpg', 'jpeg', 'png'], accept_multiple_files=False)
            
            if foto:
                st.image(Image.open(foto), caption="Foto para tasar", width=250)

            submit = st.form_submit_button("🚀 TASAR AHORA")

        if submit:
            # Ahora la validación solo pide 1 foto
            if not (modelo and estado and foto):
                st.error("⚠️ Error: Rellena los campos y sube la foto.")
            else:
                with st.spinner("Tasando..."):
                    img = Image.open(foto)
                    # Tu lógica de 10.000€ y 100h
                    prompt = f"Tasador experto. Analiza: {modelo}, {horas}h, {estado}. Si hay averías, resta 10.000€ y 100h de taller. Valor mercado 2026."
                    response = model.generate_content([prompt, img])
                    st.success("✅ Tasación Lista")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Introduce la clave API a la izquierda.")
