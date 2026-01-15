import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image
import datetime

# 1. CONFIGURACIÓN
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def limpiar_texto_para_pdf(texto):
    """Limpia caracteres raros para que el PDF no falle"""
    texto = texto.replace('€', 'Euros').replace('**', '').replace('*', '')
    return texto.encode('latin-1', 'replace').decode('latin-1')

# 2. INTERFAZ SIMPLE PARA PRUEBAS
st.title("🚜 Test de Generación PDF - V2.0")

marca = st.text_input("Marca")
modelo = st.text_input("Modelo")
fotos = st.file_uploader("Sube fotos para activar el proceso", accept_multiple_files=True)

if st.button("🚀 PROBAR GENERACIÓN"):
    if not fotos:
        st.error("Sube al menos una foto para la prueba.")
    else:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            with st.spinner('Generando respuesta de prueba...'):
                # Redimensionamos para evitar el error de cuota 429
                lista_ia = ["Haz un resumen corto de este tractor y crea una tabla de precios ficticia."]
                for f in fotos:
                    img = Image.open(f)
                    img.thumbnail((800, 800))
                    lista_ia.append(img)
                
                res = model.generate_content(lista_ia)

            # --- MOSTRAR EN APP ---
            st.markdown(res.text)

            # --- CREAR EL PDF ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt="INFORME DE PRUEBA", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=11)
            # Pasamos el texto por la limpieza antes de escribir
            texto_listo = limpiar_texto_para_pdf(res.text)
            pdf.multi_cell(0, 7, txt=texto_listo)

            # --- LA DESCARGA (CORREGIDO) ---
            # En las versiones nuevas de fpdf2, esto ya devuelve bytes
            pdf_bytes = pdf.output() 
            
            st.download_button(
                label="📥 DESCARGAR PDF DE PRUEBA",
                data=pdf_bytes,
                file_name="test_tasacion.pdf",
                mime="application/pdf"
            )
            st.success("¡PDF generado! Dale al botón de arriba para descargarlo.")

        except Exception as e:
            st.error(f"Error detectado: {e}")
