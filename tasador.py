import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración básica
st.set_page_config(page_title="Tasador One-Shot", layout="centered")
st.title("🚜 Tasador de Tractores (Versión 1 Foto)")

# Barra lateral para la API Key
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo más estable
        model = genai.GenerativeModel('gemini-1.5-flash')

        with st.form("formulario_tasacion"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas de trabajo *", min_value=0)
            estado = st.text_area("Descripción del estado y averías *")
            
            # Subida de UNA SOLA FOTO
            foto = st.file_uploader("Sube la foto principal del vehículo *", type=['jpg', 'jpeg', 'png'], accept_multiple_files=False)
            
            if foto:
                # Previsualización pequeña (ajustamos el ancho a 250px)
                img_previa = Image.open(foto)
                st.image(img_previa, caption="Foto cargada", width=250)

            enviar = st.form_submit_button("GENERAR TASACIÓN")

        if enviar:
            # Validación estricta: campos y foto obligatorios
            if not (modelo and estado and foto):
                st.error("⚠️ Error: Debes rellenar todos los campos y subir una foto.")
            else:
                with st.spinner("Analizando vehículo..."):
                    img_objeto = Image.open(foto)
                    
                    # Tu lógica de 10.000€ y 100 horas integrada
                    prompt = f"""
                    Actúa como tasador experto. Analiza este vehículo: {modelo}, con {horas}h de trabajo.
                    Descripción del usuario: {estado}.
                    REGLA TÉCNICA: Si detectas averías o el estado es malo, resta 10.000€ y 100h de taller al valor.
                    OBJETIVO: Da un precio de mercado profesional para el año 2026 basado en la foto y datos.
                    """
                    
                    response = model.generate_content([prompt, img_objeto])
                    st.success("✅ Tasación Completada")
                    st.markdown(response.text)

    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.info("Asegúrate de que la API esté 'Habilitada' en tu proyecto de Google Cloud.")

else:
    st.warning("Introduce la API Key en la barra lateral para activar el tasador.")
