import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tasador Pro 2026", layout="centered")
st.title("🚜 Tasador Alta Potencia (Gemini 1.5 Pro)")

api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # APLICAMOS LA SOLUCIÓN DE GITHUB:
        # Cambiamos 'gemini-pro' por 'gemini-1.5-pro' que es el ID válido actual
        model = genai.GenerativeModel('gemini-1.5-pro')

        with st.form("tasacion_form"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas de motor *", min_value=0)
            estado = st.text_area("Estado y Averías *")
            
            # Subida de una sola foto para evitar fallos
            foto = st.file_uploader("Sube la foto del tractor *", type=['jpg', 'jpeg', 'png'])
            
            if foto:
                st.image(Image.open(foto), width=300)

            submit = st.form_submit_button("GENERAR TASACIÓN")

        if submit:
            if not (modelo and estado and foto):
                st.error("⚠️ Error: Rellena todos los campos y sube la foto.")
            else:
                with st.spinner("Gemini 1.5 Pro está analizando..."):
                    img = Image.open(foto)
                    # Aplicamos tu regla: resta 10.000€ y 100h de taller si hay averías graves
                    prompt = f"Tasador experto. Analiza: {modelo}, {horas}h, {estado}. REGLA: Si hay averías, resta 10.000€ y 100h de taller. Valoración mercado 2026."
                    
                    response = model.generate_content([prompt, img])
                    st.success("✅ Informe Generado")
                    st.write(response.text)
                    
    except Exception as e:
        # Si sigue dando error, este mensaje te dirá qué está fallando
        st.error(f"Error técnico: {e}")
        st.info("Asegúrate de que la API esté habilitada en Google Cloud Console.")
else:
    st.warning("Escribe tu clave API en la barra lateral.")
