import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Test Visión", layout="centered")
st.title("👁️ Describe la Foto")

# --- Paso 1: API Key ---
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- Paso 2: Subida de la foto ---
    uploaded_file = st.file_uploader("Sube una foto", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Previsualización de la foto
        image = Image.open(uploaded_file)
        st.image(image, caption="Foto cargada", use_container_width=True)

        # Botón para describir
        if st.button("Describir lo que ves"):
            with st.spinner("Analizando la imagen..."):
                try:
                    # --- Paso 3: Conexión con Gemini (modelo visual) ---
                    # Usamos el modelo más simple para describir imágenes
                    model = genai.GenerativeModel('gemini-pro-vision') 
                    
                    # Le pedimos que sea breve
                    response = model.generate_content(["Describe brevemente lo que ves en esta imagen.", image])
                    st.success("Descripción de la IA:")
                    st.write(response.text)
                
                except Exception as e:
                    st.error(f"Error al contactar con Gemini: {e}")
                    st.info("Asegúrate de que la API esté 'Habilitada' en tu proyecto de Google Cloud.")
else:
    st.warning("Introduce tu API Key en la barra lateral para activar la descripción de imágenes.")
