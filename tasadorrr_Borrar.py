import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página para móvil
st.set_page_config(page_title="Tasador Pro", layout="centered")

# Acceder a la clave de forma segura
# (Debes configurarla en 'Settings' -> 'Secrets' de Streamlit Cloud)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("🚜 Tasador de Maquinaria")

# Formulario para asegurar campos obligatorios
with st.form("tasacion_form"):
    st.subheader("Datos de la Máquina")
    
    # Subida de foto con vista previa pequeña como pediste
    foto = st.file_uploader("Captura o sube foto del tractor", type=['jpg', 'png', 'jpeg'])
    
    if foto:
        st.image(foto, caption="Vista previa", width=200) # Miniatura
        
    # Campos obligatorios
    horas_reparacion = st.number_input("Horas de reparación", min_value=1, value=100)
    coste_reparacion = st.number_input("Inversión en euros (€)", min_value=0, value=10000)
    
    submit_button = st.form_submit_button("Realizar Tasación")

if submit_button:
    if not foto:
        st.error("⚠️ La foto es obligatoria para tasar.")
    else:
        with st.spinner("Analizando con Gemini 2.5 Flash..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                img = Image.open(foto)
                
                prompt = f"""
                Tasa esta máquina considerando:
                - Inversión reciente: {coste_reparacion}€
                - Mano de obra: {horas_reparacion} horas.
                Dime: Marca, Modelo, Estado y Valor de Mercado.
                """
                
                response = model.generate_content([prompt, img])
                
                st.success("### Resultado de la Tasación")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
