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
        try:
            # 1. Definimos el modelo (operación rápida)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # 2. Preparamos el Prompt de comparación técnica
            prompt = f"""
            Actúa como un experto tasador agrícola. Compara el tractor introducido con el mercado actual (Agriaffaires, Milanuncios, Traktorpool, E-FARM y Ben Burgess).

            UNIDAD A TASAR:
            - Modelo: {marca} {modelo} | Año: {anio} | Horas: {horas}
            - Equipación Clave: {observaciones} (Pala, Tripuntal, Transmisión, Neumáticos)

            INSTRUCCIONES DE ANÁLISIS:
            1. BUSCAR HORQUILLA: Localiza anuncios con año y horas similares para establecer el rango Base.
            2. COMPARAR EQUIPACIÓN:
               - Si tiene PALA o TRIPUNTAL: Súbelo hacia el precio de Ben Burgess o E-FARM.
               - Si la TRANSMISIÓN es superior (ej. AutoPower/Vario o IVT o Cambio continuo): Posiciónalo en el tercio superior de la horquilla.
               - Si los NEUMÁTICOS están >70%: Evita el descuento por mantenimiento inmediato.
            3. FILTRO DE HORAS ALTAS: Si supera las 8.500h, ancla el precio al 'suelo' detectado en Milanuncios/Agriaffaires para evitar valores irreales.

            SALIDA RESUMIDA (Formato Estricto):
            - RANGO MERCADO: [Precio Mín - Precio Máx encontrado]
            - POSICIONAMIENTO: [Bajo / Medio / Alto] Justificado por equipación.
            - PRECIO SUGERIDO: [Cifra única en €]
            - ANUNCIO DE REFERENCIA: [Link o descripción breve del anuncio más similar encontrado]
            """

            # 3. El spinner envuelve el proceso de análisis y carga de imágenes
            with st.spinner('🔍 Analizando fotos y rastreando anuncios en Agriaffaires, Ben Burgess y portales europeos...'):
                
                # Preparamos el contenido mezclando texto e imágenes
                contenido = [prompt]
                for f in fotos_subidas:
                    img = Image.open(f)
                    contenido.append(img)
                
                # Llamada única al motor 2.5-flash
                res = model.generate_content(contenido)
            
            # 4. Resultado final
            st.success("✅ Tasación Finalizada con éxito")
            st.markdown(res.text)
            
        except Exception as e:
            st.error(f"❌ Error en el motor de tasación: {e}")
