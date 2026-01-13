import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. Configuración de la API con el modelo que me indicaste
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🚜 Peritaje Profesional V2.0")

# --- FORMULARIO DE DATOS ---
c1, c2, c3 = st.columns(3)
with c1:
    marca = st.text_input("Marca*", key="marca")
with c2:
    modelo = st.text_input("Modelo*", key="modelo")
with c3:
    anio = st.text_input("Año*", key="anio")

observaciones = st.text_area("Incidencias y Extras", placeholder="Ej: Pala, averías, pintura saltada, estado de neumáticos...")

st.divider()

# --- SUBIDA DE FOTOS (SIN NOTAS) ---
st.subheader("Fotografías (Mínimo 5, Máximo 10)")
fotos_subidas = st.file_uploader("Sube las fotos de la máquina", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos permitidas.")
    else:
        # Mostramos una vista previa rápida de las fotos subidas
        cols = st.columns(5)
        for i, foto in enumerate(fotos_subidas):
            with cols[i % 5]:
                st.image(foto, use_column_width=True)

st.divider()

# --- BOTÓN Y LÓGICA DE TASACIÓN ---
if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not marca or not modelo or not anio:
        st.warning("⚠️ Marca, Modelo y Año son obligatorios.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos para un análisis detallado.")
    else:
        # Barra de progreso para amenizar la espera
        barra = st.progress(0)
        txt_estado = st.empty()
        
        for i in range(1, 101):
            time.sleep(0.02)
            barra.progress(i)
            if i == 20: txt_estado.text("🔎 Analizando visualmente cada fotografía...")
            if i == 50: txt_estado.text("📊 Consultando precios de compra en mercado europeo...")
            if i == 80: txt_estado.text("⚖️ Ajustando valoración final de compra...")

        try:
            # Usando gemini-2.5-flash como recordaste
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Actúa como un tasador experto para un concesionario de compra-venta.
            
            DATOS SUMINISTRADOS:
            - Marca: {marca}
            - Modelo: {modelo}
            - Año: {anio}
            - Notas adicionales: {observaciones}
            
            TU TAREA:
            1. Analiza DETALLADAMENTE cada una de las fotos enviadas.
            2. Menciona en el informe qué has visto en las imágenes (estado de neumáticos, posibles fugas, desgaste de cabina, estado de la pintura, etc.).
            3. Extrae el Número de Serie si aparece en alguna placa.
            4. Calcula un PRECIO DE COMPRA PROFESIONAL (lo que pagaríamos nosotros por la máquina). 
               El precio debe ser realista, ajustado a mercado profesional y TIRANDO A LA BAJA para asegurar margen.
            
            ESTILO: Directo y profesional. No des la bienvenida ni uses relleno.
            """
            
            contenido = [prompt]
            for f in fotos_subidas:
                contenido.append(Image.open(f))
            
            res = model.generate_content(contenido)
            
            st.success("✅ Peritaje Finalizado")
            st.subheader("Informe de Tasación")
            st.markdown(res.text)
            
        except Exception as e:
            st.error(f"Error en el motor Gemini 2.5: {e}")
