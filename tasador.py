import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="Tasador Pro 2026", layout="centered")
st.title("🚜 Tasador Alta Potencia")

# Campo para la API Key
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        # Forzamos el uso de la API v1 (estable), no la v1beta
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
        
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
                st.error("⚠️ Error: Rellena todos los campos y sube la foto.")
            else:
                with st.spinner("Gemini Pro analizando..."):
                    img = PIL.Image.open(foto)
                    
                    # Tu lógica de 10.000€ y 100h
                    prompt = f"Tasador experto. Analiza: {modelo}, {horas}h, {estado}. REGLA: Si hay averías, resta 10.000€ y 100h de taller. Precio 2026."
                    
                    # Usamos el modelo estable
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt, img]
                    )
                    
                    st.success("✅ Tasación Completada")
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.info("Si el error 404 persiste, entra en Google Cloud Console y asegúrate de que el proyecto seleccionado coincide con tu API Key.")
else:
    st.warning("Escribe tu clave API en la barra lateral.")
