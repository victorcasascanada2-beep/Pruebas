import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. Configuración de la API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# NOTA: Hemos quitado set_page_config para evitar el error de ayer
st.title("🚜 Peritaje Profesional V2.0")

# --- FORMULARIO DE DATOS ---
# Usamos columnas simples para Marca, Modelo y Año
c1, c2, c3 = st.columns(3)
with c1:
    marca = st.text_input("Marca*", key="marca")
with c2:
    modelo = st.text_input("Modelo*", key="modelo")
with c3:
    anio = st.text_input("Año*", key="anio")

observaciones = st.text_area("Incidencias y Extras", placeholder="Ej: Pala, averías, pintura...")

st.divider()

# --- SUBIDA DE FOTOS ---
st.subheader("Fotografías (Mínimo 5)")
fotos_subidas = st.file_uploader("Sube tus fotos aquí", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

comentarios = []

# Cambiamos la lógica de las columnas por una lista simple para evitar el TypeError
if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos.")
    else:
        for i, foto in enumerate(fotos_subidas):
            st.image(foto, width=200) # Imagen pequeña para no ocupar toda la pantalla
            nota = st.text_input(f"Nota para foto {i+1} (máx 4 líneas)", key=f"nota_{i}")
            comentarios.append(nota)

st.divider()

# --- BOTÓN Y LÓGICA ---
if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        # Barra de progreso
        barra = st.progress(0)
        txt_estado = st.empty()
        
        for i in range(1, 101):
            time.sleep(0.02)
            barra.progress(i)
            if i == 20: txt_estado.text("🔎 Analizando estado visual...")
            if i == 50: txt_estado.text("📊 Consultando precios de compra profesional...")
            if i == 80: txt_estado.text("⚖️ Ajustando tasación a la baja...")

        try:
            model = genai.GenerativeModel('gemini-1.5-flash') # Usamos 1.5 que es más estable
            
            # Prompt optimizado
            prompt = f"""
            Actúa como tasador para un compra-venta. 
            DATOS: Marca {marca}, Modelo {modelo}, Año {anio}.
            NOTAS DEL PERITO: {observaciones}.
            NOTAS DE FOTOS: {comentarios}.
            
            TAREA:
            1. Valor de COMPRA (lo que debemos pagar nosotros por ella).
            2. Extraer Nº Serie si se ve.
            3. Ser muy breve (4-5 líneas máximo).
            """
            
            contenido = [prompt]
            for f in fotos_subidas:
                contenido.append(Image.open(f))
            
            res = model.generate_content(contenido)
            st.success("Tasación Finalizada")
            st.markdown(res.text)
            
        except Exception as e:
            st.error(f"Fallo en la IA: {e}")
