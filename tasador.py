import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tasador Pro 2026", layout="centered")
st.title("🚜 Tasador Experto de Tractores")

api_key = st.sidebar.text_input("Introduce tu API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # CAMBIO CLAVE: Usamos 'gemini-1.5-flash' sin el '-latest' 
        # para que sea compatible con la versión v1beta que detecta tu sistema.
        model = genai.GenerativeModel('gemini-1.5-flash')

        with st.form("tasacion_form"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas *", min_value=0)
            detalles = st.text_area("Estado general y averías *")
            
            # Fotos en 5 columnas para que sean pequeñas
            fotos = st.file_uploader("Sube fotos (mínimo 4) *", type=['jpg','png','jpeg'], accept_multiple_files=True)
            
            if fotos:
                cols = st.columns(5)
                for i, f in enumerate(fotos):
                    with cols[i % 5]:
                        st.image(Image.open(f), use_container_width=True)

            submit = st.form_submit_button("TASAR AHORA")

        if submit:
            if not (modelo and detalles and len(fotos) >= 4):
                st.error("⚠️ Error: Todos los campos con * son mandatorios.")
            else:
                with st.spinner("Conectando con la IA..."):
                    # Recordamos tu lógica de reparación: 10.000€ y 100 horas
                    prompt = f"Actúa como tasador. Analiza: {modelo}, {horas}h, {detalles}. REGLA: Si hay averías, resta 10.000€ y 100h de taller. Precio para 2026."
                    imgs = [Image.open(f) for f in fotos]
                    response = model.generate_content([prompt] + imgs)
                    st.success("✅ Tasación Lista")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.warning("Escribe tu API Key en la izquierda.")
