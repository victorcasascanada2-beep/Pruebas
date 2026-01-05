import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="Tasador Pro 2026", layout="centered")
st.title("🚜 Tasador Alta Potencia (Nueva API)")

# Clave API en el lateral
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        # Nueva forma oficial de conectar (SDK v1)
        client = genai.Client(api_key=api_key)
        
        with st.form("tasacion_form"):
            st.subheader("Datos Mandatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas de motor *", min_value=0)
            estado = st.text_area("Descripción de averías *")
            
            foto = st.file_uploader("Sube la foto del tractor *", type=['jpg', 'jpeg', 'png'])
            
            if foto:
                st.image(PIL.Image.open(foto), width=250)

            submit = st.form_submit_button("GENERAR TASACIÓN")

        if submit:
            if not (modelo and estado and foto):
                st.error("⚠️ Faltan datos obligatorios o la foto.")
            else:
                with st.spinner("Gemini Pro analizando..."):
                    img = PIL.Image.open(foto)
                    
                    # Tu lógica de 10.000€ y 100h integrada
                    prompt = f"""
                    Actúa como tasador experto. Analiza este tractor: {modelo}, con {horas}h.
                    Descripción: {estado}.
                    REGLA TÉCNICA: Si hay averías graves, resta 10.000€ y 100h de taller al valor.
                    Precio mercado 2026.
                    """
                    
                    # Llamada con la nueva librería
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt, img]
                    )
                    
                    st.success("✅ Tasación Completada")
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.warning("Escribe tu clave API para activar la App.")
