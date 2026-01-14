import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. Configuración de la API (Usando el modelo recordado)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🚜 Peritaje Profesional V2.0")

# --- FORMULARIO DE DATOS ---
c1, c2, c3, c4= st.columns(4)
with c1:
    marca = st.text_input("Marca*", key="marca_v2")
with c2:
    modelo = st.text_input("Modelo*", key="modelo_v2")
with c3:
    anio = st.text_input("Año*", key="anio_v2")
with c4:
    horas = st.number_input("Horas de uso*", min_value=0, key="horas_input")

observaciones = st.text_area("Incidencias y Extras", placeholder="Ej: Pala, averías, pintura...")

st.divider()

# --- SUBIDA DE FOTOS ---
st.subheader("Fotografías (Mínimo 5)")
fotos_subidas = st.file_uploader("Sube tus fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos.")
    else:
        # Usamos una cuadrícula para ver las fotos rápido
        cols = st.columns(5)
        for i, foto in enumerate(fotos_subidas):
            with cols[i % 5]:
                st.image(foto, width=150)

st.divider()

# --- BOTÓN Y LÓGICA ---
if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        # Barra de progreso
        barra = st.progress(0)
        txt_estado = st.empty()
        
        for i in range(1, 101):
            time.sleep(0.08)
            barra.progress(i)
            if i == 30: txt_estado.text("🔎 Analizando estado visual...")
            if i == 70: txt_estado.text("📊 Calculando horquilla de mercado...")

        try:
            # Motor 2.5-flash como solicitaste
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Actúa como tasador para un compra-venta profesional. 
            DATOS: Marca {marca}, Modelo {modelo}, Año {anio}, Horas {horas}.
            NOTAS: {observaciones}.
            
            TAREA:
            1. ANALIZA LAS FOTOS: Menciona qué ves en ellas (neumáticos, cabina, posibles fallos).
            2. VALOR DE COMPRA: Calcula una horquilla de precios (Mínimo - Máximo) con un margen del 15% entre ellos.
            3. Estilo profesional, directo y realista para captación.
            """
            
            contenido = [prompt]
            for f in fotos_subidas:
                contenido.append(Image.open(f))
            
            res = model.generate_content(contenido)
            st.success("Tasación Finalizada")
            st.markdown(res.text)
            
        except Exception as e:
            st.error(f"Fallo en la IA: {e}")
