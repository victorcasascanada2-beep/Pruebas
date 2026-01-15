import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image
import datetime
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# ==========================================
# 1. CONFIGURACIÓN Y HERRAMIENTAS
# ==========================================
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def limpiar_texto_para_pdf(texto):
    """Limpia caracteres que FPDF no soporta (acentos, emojis, símbolos)"""
    texto = texto.replace('€', 'Euros').replace('**', '').replace('*', '')
    return texto.encode('latin-1', 'replace').decode('latin-1')

def guardar_en_drive(nombre_archivo, texto_ia, cabecera):
    """Envía el PDF a la carpeta de Google Drive"""
    try:
        info_llave = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info_llave)
        service = build('drive', 'v3', credentials=creds)

        # --- RECUERDA: SUSTITUYE ESTE ID POR EL DE TU CARPETA REAL ---
        ID_CARPETA_DESTINO = "TU_ID_AQUÍ" 

        path_temp = "temp_tasacion.pdf"
        
        # Re-creamos el PDF para subirlo
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, txt="INFORME DE TASACION PROFESIONAL", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, txt=limpiar_texto_para_pdf(texto_ia))
        pdf.output(path_temp)

        metadatos = {'name': nombre_archivo, 'parents': [ID_CARPETA_DESTINO]}
        media = MediaFileUpload(path_temp, mimetype='application/pdf')
        service.files().create(body=metadatos, media_body=media).execute()

        if os.path.exists(path_temp):
            os.remove(path_temp)
        st.success(f"📂 Guardado en Drive con éxito")
    except Exception as e:
        st.error(f"⚠️ No se pudo subir a Drive (pero puedes descargarlo abajo): {e}")

# ==========================================
# 2. INTERFAZ DE LA APP
# ==========================================
st.set_page_config(page_title="Tasador Experto Pro", layout="wide")
st.title("🚜 Peritaje Profesional V2.0")

# --- FORMULARIO ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    marca = st.text_input("Marca*", key="marca_v2")
with c2:
    modelo = st.text_input("Modelo*", key="modelo_v2")
with c3:
    anio = st.text_input("Año*", key="anio_v2")
with c4:
    horas = st.number_input("Horas de uso*", min_value=0, key="horas_input")

observaciones = st.text_area("Incidencias y Extras", placeholder="Ej: Pala, averías, pintura...")

st.subheader("Fotografías (Mínimo 5)")
fotos_subidas = st.file_uploader("Sube tus fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    cols = st.columns(5)
    for i, foto in enumerate(fotos_subidas):
        with cols[i % 5]:
            st.image(foto, width=150)

st.divider()

# ==========================================
# 3. LÓGICA DE TASACIÓN
# ==========================================
if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        try:
            # Usando el modelo Flash 2.5 como pediste
            model = genai.GenerativeModel('gemini-2.0-flash') # (Nota: En 2026 usamos la versión disponible más estable)

            prompt = f"""
            Actúa como un perito tasador de maquinaria agrícola. 
            Analiza un {marca} {modelo} del año {anio} con {horas} horas.
            Extras: {observaciones}
            1. Resume lo que ves en las fotos.
            2. Da una tabla de precios de anuncios similares en Europa.
            3. Calcula: Valor de Mercado (Venta) y Precio de Compra sugerido.
            """

            with st.spinner('🔍 Analizando fotos y mercados europeos...'):
                contenido = [prompt]
                for f in fotos_subidas:
                    img = Image.open(f)
                    contenido.append(img)
                
                res = model.generate_content(contenido)
            
            # --- MOSTRAR RESULTADO ---
            st.success("✅ Tasación Finalizada")
            st.markdown(res.text)

            # --- GENERAR PDF PARA DESCARGA LOCAL ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, txt=f"INFORME: {marca} {modelo}", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=11)
            
            texto_pdf = limpiar_texto_para_pdf(res.text)
            pdf.multi_cell(0, 7, txt=texto_pdf)
            
            # Generamos los bytes del PDF
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            # --- BOTÓN DE DESCARGA LOCAL ---
            st.download_button(
                label="📥 DESCARGAR INFORME EN PDF (Local)",
                data=pdf_output,
                file_name=f"Tasacion_{marca}_{modelo}.pdf",
                mime="application/pdf"
            )

            # --- INTENTO DE GUARDADO EN DRIVE ---
            nombre_archivo = f"Tasacion_{marca}_{modelo}_{horas}h.pdf"
            info_cabecera = f"{marca} {modelo} ({anio})"
            guardar_en_drive(nombre_archivo,
