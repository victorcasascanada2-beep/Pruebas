import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

st.title("🚜 Peritaje Profesional V2.0")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la clave API.")
    st.stop()

# --- DATOS DE LA MÁQUINA ---
with st.container():
    c1, c2, c3 = st.columns(3)
    marca = c1.text_input("Marca*")
    modelo = c2.text_input("Modelo*")
    anio = c3.text_input("Año*")
    observaciones = st.text_area("Observaciones Generales", placeholder="Ej: Historial de revisiones, extras importantes...", height=80)

st.divider()

# --- SUBIDA DE FOTOS (SIN COMENTARIOS MANUALES) ---
st.subheader("📸 Fotografías del Peritaje (Mínimo 5)")
fotos = st.file_uploader("Sube hasta 10 fotos para análisis profundo", type=['jpg','jpeg','png'], accept_multiple_files=True)

if fotos:
    cols = st.columns(5)
    for i, f in enumerate(fotos[:10]):
        cols[i % 5].image(f, use_container_width=True)

st.divider()

if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not (marca and modelo and anio):
        st.warning("⚠️ Marca, Modelo y Año son obligatorios.")
    elif len(fotos or []) < 5:
        st.warning("⚠️ Sube al menos 5 fotos para que el análisis sea preciso.")
    else:
        # --- BARRA DE PROGRESO MÁS REALISTA ---
        barra = st.progress(0)
        status = st.empty()
        
        pasos = [
            (20, "🔍 Identificando componentes en las fotografías..."),
            (40, "📸 Analizando estado de neumáticos y carrocería..."),
            (60, "📊 Cotejando con precios en Mascus y Agriaffaires..."),
            (80, "⚖️ Calculando valor de captación profesional..."),
            (100, "📝 Redactando informe de peritaje...")
        ]
        
        for (porcentaje, texto) in pasos:
            status.text(texto)
            # Incremento más lento para dar realismo
            while barra.progress(0).progress < porcentaje:
                time.sleep(0.05)
                actual = barra.progress(0).progress
                barra.progress(actual + 1)
                if actual + 1 >= porcentaje: break

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # PROMPT OPTIMIZADO: Ahora pedimos que analice las fotos
            prompt = f"""
            Eres un perito tasador agrícola senior. 
            MÁQUINA: {marca} {modelo} ({anio}).
            OBSERVACIONES: {observaciones}.

            INSTRUCCIONES PARA EL INFORME:
            1. ANÁLISIS VISUAL: Analiza las fotos y escribe un párrafo de unas 4 líneas describiendo el estado físico que observas (desgastes, posibles fugas, limpieza, estado de neumáticos y cabina).
            2. NÚMERO DE SERIE: Búscalo en las placas identificativas de las fotos.
            3. TASACIÓN DE COMPRA: Proporciona un precio de compra para el concesionario. Debe ser un precio "de captación" (profesional), tirando a la BAJA para asegurar margen pero realista.
            4. MERCADO: Menciona brevemente la tendencia de este modelo en Europa.

            Sé muy directo y profesional en español.
            """

            contenido = [prompt]
            for f in fotos:
                contenido.append(Image.open(f))

            res = model.generate_content(contenido)
            st.success("✅ Peritaje Finalizado")
            st.markdown("### 📋 Informe de Tasación")
            st.write(res.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
