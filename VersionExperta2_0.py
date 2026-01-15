import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image
import os
import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL MOTOR (Gemini 2.5 Flash)
# ==========================================
# Se conecta con tu clave guardada en Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ==========================================
# 2. HERRAMIENTAS DE PROCESAMIENTO
# ==========================================

def limpiar_texto_para_pdf(texto):
    """
    Adapta el texto de la IA para que el generador de PDF no falle.
    Sustituye símbolos especiales y elimina marcas de formato (negritas).
    """
    # Cambios de compatibilidad
    texto = texto.replace('€', 'Euros')
    texto = texto.replace('**', '')  # Eliminar negritas de Markdown
    texto = texto.replace('*', '')   # Eliminar puntos de lista de Markdown
    
    # Codificación segura para PDF (Latin-1)
    return texto.encode('latin-1', 'replace').decode('latin-1')

# ==========================================
# 3. INTERFAZ DE USUARIO (Streamlit)
# ==========================================
st.set_page_config(page_title="Tasador Experto 2.5", layout="wide")

st.title("🚜 Peritaje Profesional V2.0")
st.info("Sistema de tasación local basado en Gemini 2.5 Flash")

# --- FORMULARIO DE ENTRADA ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        marca = st.text_input("Marca*", key="m_local")
    with c2:
        modelo = st.text_input("Modelo*", key="mod_local")
    with c3:
        anio = st.text_input("Año*", key="a_local")
    with c4:
        horas = st.number_input("Horas de uso*", min_value=0, key="h_local")

    observaciones = st.text_area(
        "Incidencias y Extras", 
        placeholder="Ej: Neumáticos al 80%, Tripuntal delantero Zuidberg, pintura original...",
        help="Cuanta más información des, más precisa será la IA."
    )

st.divider()

# --- CARGA DE IMÁGENES ---
st.subheader("📸 Galería Fotográfica")
fotos_subidas = st.file_uploader(
    "Sube entre 5 y 10 fotos para un análisis visual preciso", 
    type=['jpg', 'jpeg', 'png'], 
    accept_multiple_files=True
)

if fotos_subidas:
    # Mostrar previsualización pequeña
    cols = st.columns(5)
    for i, foto in enumerate(fotos_subidas):
        with cols[i % 5]:
            st.image(foto, use_container_width=True)

st.divider()

# ==========================================
# 4. LÓGICA DE EJECUCIÓN (El Botón)
# ==========================================
if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    # Verificaciones de seguridad
    if not marca or not modelo or not anio:
        st.warning("⚠️ Por favor, rellena Marca, Modelo y Año para continuar.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ El peritaje requiere al menos 5 fotografías para ser fiable.")
    else:
        try:
            # 1. Llamada al Modelo
            model = genai.GenerativeModel('gemini-2.5-flash')

            with st.spinner('🔍 Analizando fotos y rastreando precios en portales europeos...'):
                # Redimensionamos fotos para no agotar la cuota de la API (Tokens)
                lista_analisis = [
                    f"Tractor: {marca} {modelo}, Año: {anio}, Horas: {horas}. Notas extra: {observaciones}",
                    "Instrucción: Analiza el estado visual, busca precios de mercado en Europa y calcula valor de compra y venta."
                ]
                
                for f in fotos_subidas:
                    img = Image.open(f)
                    # Reducimos tamaño para que no pese tanto el envío a Google
                    img.thumbnail((800, 800))
                    lista_analisis.append(img)
                
                # Ejecución de la IA
                respuesta_ia = model.generate_content(lista_analisis)
            
            # 2. Presentación en Pantalla
            st.success("✅ Análisis de mercado finalizado con éxito.")
            st.markdown("### Resultado del Informe")
            st.markdown(respuesta_ia.text)

            # 3. Generación del Informe PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Cabecera del PDF
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt="INFORME PERICIAL DE MAQUINARIA", ln=True, align='C')
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(190, 10, txt=f"Generado el: {datetime.date.today()}", ln=True, align='C')
            pdf.ln(10)
            
            # Datos del vehículo
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 8, txt=f"Vehiculo: {marca.upper()} {modelo.upper()}", ln=True)
            pdf.cell(190, 8, txt=f"Ano: {anio} | Horas: {horas}", ln=True)
            pdf.ln(5)
            
            # Cuerpo del informe (Limpiado)
            pdf.set_font("Arial", size=11)
            texto_seguro = limpiar_texto_para_pdf(respuesta_ia.text)
            pdf.multi_cell(0, 7, txt=texto_seguro)
            
            # Preparar descarga
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            
            # 4. Botón de Descarga
            st.download_button(
                label="📥 DESCARGAR INFORME EN PDF",
                data=pdf_bytes,
                file_name=f"Tasacion_{marca}_{modelo}_{anio}.pdf",
                mime="application/pdf",
                help="Haz clic para guardar el informe en tu ordenador."
            )

        except Exception as e:
            # Control de errores específico para Cuota
            if "429" in str(e):
                st.error("❌ Cuota agotada: Google está recibiendo muchas peticiones. Espera 30 segundos y vuelve a pulsar el botón.")
            else:
                st.error(f"❌ Error inesperado: {e}")

# Pie de página
st.caption("Powered by Gemini 2.5 Flash | Tasador Local V2.0")
