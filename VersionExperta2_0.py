import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURACIÓN
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def limpiar_texto_para_pdf(texto):
    """
    Limpia el texto para que FPDF no falle al generar el PDF.
    Sustituye símbolos y asegura codificación latin-1.
    """
    # Cambios básicos de símbolos
    texto = texto.replace('€', 'Euros').replace('**', '').replace('*', '-')
    
    # Manejo de acentos y caracteres especiales para evitar errores de codificación
    texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    texto = texto.replace('ñ', 'n').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    
    # Retornamos el texto codificado de forma segura
    return texto.encode('latin-1', 'replace').decode('latin-1')

# 2. INTERFAZ DE USUARIO
st.set_page_config(page_title="Test PDF Pro", layout="centered")
st.title("🚜 Generador de Informes PDF")

marca = st.text_input("Marca del tractor", placeholder="Ej: John Deere")
modelo = st.text_input("Modelo", placeholder="Ej: 6155M")
fotos = st.file_uploader("Sube fotos para el peritaje", accept_multiple_files=True)

if st.button("🚀 GENERAR TASACIÓN Y PDF"):
    if not fotos or not marca:
        st.error("⚠️ Por favor, introduce la marca y sube alguna foto.")
    else:
        try:
            # Motor Gemini 2.5 Flash
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            with st.spinner('Analizando maquinaria...'):
                # Redimensionamos fotos para optimizar la cuota
                lista_ia = [f"Haz un informe técnico del tractor {marca} {modelo}."]
                for f in fotos:
                    img = Image.open(f)
                    img.thumbnail((800, 800))
                    lista_ia.append(img)
                
                res = model.generate_content(lista_ia)

            # Mostrar resultado en la App
            st.markdown("### Vista Previa del Informe")
            st.info(res.text)

            # --- CONSTRUCCIÓN DEL PDF ---
            pdf = FPDF()
            pdf.add_page()
            
            # Título
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=f"INFORME DE TASACION: {marca.upper()}", ln=True, align='C')
            pdf.ln(10)
            
            # Contenido
            pdf.set_font("Arial", size=11)
            texto_limpio = limpiar_texto_para_pdf(res.text)
            pdf.multi_cell(0, 7, txt=texto_limpio)

            # --- CONVERSIÓN A BYTES (SOLUCIÓN AL ERROR) ---
            # Forzamos la conversión de bytearray a bytes inmutables
            pdf_output = pdf.output()
            pdf_bytes = bytes(pdf_output) 
            
            # --- BOTÓN DE DESCARGA ---
            st.download_button(
                label="📥 DESCARGAR INFORME PDF",
                data=pdf_bytes,
                file_name=f"Tasacion_{marca}.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF generado correctamente.")

        except Exception as e:
            st.error(f"❌ Error detectado: {e}")
