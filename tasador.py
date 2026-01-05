import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🚜 Prueba de Visión Pro")

# Barra lateral para la llave
api_key = st.sidebar.text_input("Pega tu API Key aquí", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo 1.5-flash que es el que mejor procesa imágenes
        model = genai.GenerativeModel('gemini-1.5-flash')

        foto = st.file_uploader("Sube una foto de prueba", type=['jpg', 'png', 'jpeg'])

        if foto:
            img = Image.open(foto)
            st.image(img, width=300)
            
            if st.button("¿Qué ves en la imagen?"):
                with st.spinner("Gemini está mirando..."):
                    # Esta es la llamada que fallaba antes
                    response = model.generate_content(["Describe brevemente lo que ves.", img])
                    st.success("¡CONECTADO!")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.warning("Introduce tu API Key en la izquierda.")
