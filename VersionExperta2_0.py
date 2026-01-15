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
            


            # --- PROMPT DE TASACIÓN COMERCIAL PROFESIONAL ---
            prompt = f"""
            Actúa como un perito tasador y director comercial de maquinaria agrícola. Tu objetivo es calcular el valor de compra y el precio de venta recomendado para un {marca} {modelo} ({anio}).

            DATOS DE LA UNIDAD:
            - Modelo: {marca} {modelo} | Año: {anio} | Uso: {horas} horas.
            - Extras declarados: {observaciones} (Incluyendo Tripuntal Zuidberg y Neumáticos al 75% si procede).

            INSTRUCCIONES DE ANÁLISIS:
            1. ANÁLISIS VISUAL FOTO A FOTO:
               - Identifica y resume cada imagen. Busca específicamente el Tripuntal delantero, el estado de los tacos de las ruedas y la limpieza de la cabina/motor.
               - Si detectas extras de alto valor (Zuidberg, pesas, suspensión), úsalos para justificar un posicionamiento en la banda alta.

            2. PROCEDIMIENTO ESTADÍSTICO (Media Truncada):
               - Busca en Agriaffaires, Traktorpool, E-FARM y Mascus. 
               - Toma toda la muestra europea de este modelo y año. Ordena por precio y ELIMINA el 10% más caro y el 10% más barato para limpiar la muestra de anuncios irreales.

            3. CÁLCULO DE VALORES (Lógica Comercial):
               - PRECIO DE ATERRIZAJE: Es el valor real de mercado basado en la media truncada, ajustado por horas y extras visuales. (Este debe ser vuestro valor de anuncio).
               - PRECIO DE COMPRA (PVP): Sobre el precio de aterrizaje, resta un margen del 15 para cubrir preparación.

            SALIDA DE DATOS REQUERIDA:
            -TABLA DE ANUNCIOS [Una tabla con pais ciudad año y precio de anuncio]
            - MUESTRA ANALIZADA: [Nº anuncios encontrados en Europa]
            - RESUMEN VISUAL: [Breve descripción de lo detectado en las fotos subidas]
            - ESTADO GENERAL: [Puntuación 1-10]
            
            - RESULTADOS FINALES:
              * VALOR DE MERCADO (Aterrizaje): [Cifra en €]
              * PRECIO DE COMPRA SUGERIDA (PVP): [Cifra en €] 
            
            - NOTA COMERCIAL: [Justificación de por qué este tractor permite ese margen (ej: "Unidad muy buscada por horas y tripuntal Zuidberg").]
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
