import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de API y Página
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
st.set_page_config(page_title="Tasador Experto 5F", layout="centered")

st.title("🚜 Peritaje Detallado (5 Fotos)")
st.write("Introduce los datos técnicos para una valoración precisa.")

# Formulario principal
with st.form("tasacion_detallada"):
    # Sección de Datos Técnicos (Obligatorios)
    col1, col2 = st.columns(2)
    with col1:
        marca = st.text_input("Marca*", placeholder="Ej: John Deere")
        modelo = st.text_input("Modelo*", placeholder="Ej: 6155M")
    with col2:
        horas_uso = st.number_input("Horas de uso totales*", min_value=0, step=100)
    
    # Subida de hasta 5 fotos
    st.subheader("Fotos de la máquina (Máx. 5)")
    fotos = st.file_uploader("Selecciona las fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    # Vista previa en miniatura (como pediste)
    if fotos:
        if len(fotos) > 5:
            st.warning("⚠️ Solo se procesarán las primeras 5 fotos.")
            fotos = fotos[:5]
        
        # Mostramos las fotos en columnas pequeñas
        cols_previa = st.columns(5)
        for i, f in enumerate(fotos):
            with cols_previa[i]:
                st.image(f, use_container_width=True)

    submit = st.form_submit_button("Generar Informe de Tasación")

if submit:
    # Validación de campos obligatorios
    if not (marca and modelo and fotos):
        st.error("❌ Por favor, rellena la Marca, Modelo y sube al menos una foto.")
    else:
        with st.spinner("Analizando ángulos y datos técnicos..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Preparamos la lista de contenidos para la IA
                contenido_ia = [
                    f"Realiza un peritaje técnico para este tractor.",
                    f"Marca: {marca}",
                    f"Modelo: {modelo}",
                    f"Horas de trabajo: {horas_uso} h.",
                    "Instrucciones: Analiza las fotos adjuntas para evaluar el estado de los neumáticos, carrocería y posibles fugas. Estima un valor de mercado profesional."
                ]
                
                # Añadimos las imágenes procesadas
                for f in fotos:
                    img = Image.open(f)
                    contenido_ia.append(img)
                
                response = model.generate_content(contenido_ia)
                
                st.success("✅ Tasación Finalizada")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hubo un problema: {e}")
