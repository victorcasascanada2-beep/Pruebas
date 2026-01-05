import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la App
st.set_page_config(page_title="Tasador Pro 2026", layout="centered")

st.title("🚜 Tasador Agrícola Pro")
st.markdown("---")

# Barra lateral para la llave (Usa la de la cuenta nueva)
api_key = st.sidebar.text_input("🔑 API Key de Google", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Formulario con validación mandatoria según tus instrucciones
    with st.form("main_form"):
        st.subheader("Datos Obligatorios *")
        modelo = st.text_input("Marca y Modelo *", placeholder="Ej: John Deere 6155M")
        
        col_input = st.columns(2)
        with col_input[0]:
            horas = st.number_input("Horas de trabajo *", min_value=0, step=1)
        with col_input[1]:
            año = st.number_input("Año fabricación *", min_value=1980, max_value=2026, value=2022)
            
        estado = st.text_area("Descripción del estado y averías *", 
                             placeholder="Indica extras o daños específicos...")

        st.subheader("Fotos de Inspección (Mínimo 4) *")
        fotos = st.file_uploader("Sube las fotos aquí", 
                                type=['jpg', 'jpeg', 'png'], 
                                accept_multiple_files=True)

        # Previsualización pequeña (instrucción del usuario)
        if fotos:
            st.write("Vista previa:")
            cols = st.columns(5) # 5 fotos por fila para que se vean pequeñas
            for i, f in enumerate(fotos):
                with cols[i % 5]:
                    st.image(Image.open(f), use_container_width=True)

        submit = st.form_submit_button("🚀 GENERAR INFORME DE TASACIÓN")

    if submit:
        # Validación estricta
        if not (modelo and estado and len(fotos) >= 4):
            st.error("⚠️ Error: Debes completar todos los campos y subir al menos 4 fotos.")
        else:
            with st.spinner("Analizando con Gemini 1.5 Flash..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    img_objs = [Image.open(f) for f in fotos]
                    
                    # Lógica de costes integrada (10.000€ y 100h)
                    prompt = f"""
                    Eres un tasador experto. Analiza: {modelo}, año {año}, {horas}h.
                    Descripción: {estado}.
                    REGLA TÉCNICA: Si hay averías mecánicas, resta 10.000€ de valor y 100h de taller.
                    PROYECCIÓN: Valor de mercado para el año 2026.
                    """
                    
                    response = model.generate_content([prompt] + img_objs)
                    st.success("✅ Tasación Completada")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("Introduce tu API Key en la barra lateral para empezar.")
