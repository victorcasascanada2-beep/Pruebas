import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import datetime

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
# Tu clave de Gemini guardada en Streamlit Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def imagen_a_base64(img_file):
    """Convierte la foto en texto para que viaje dentro del archivo HTML"""
    img = Image.open(img_file)
    # Redimensionamos a 800px para que el archivo no pese demasiado en Drive
    img.thumbnail((800, 800)) 
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def subir_a_drive(nombre, html_content, id_carpeta):
    """Sube el archivo asegurando que no use la cuota del bot"""
    try:
        info_llave = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info_llave)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': nombre, 
            'parents': [id_carpeta],
            'mimeType': 'text/html'
        }
        
        # Convertimos el contenido a bytes
        media_content = BytesIO(html_content.encode('utf-8'))
        media = MediaIoBaseUpload(media_content, mimetype='text/html', resumable=True)
        
        # IMPORTANTE: supportsAllDrives=True permite subir a carpetas donde el bot es editor
        # aunque el bot no tenga espacio propio.
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id',
            supportsAllDrives=True  # <--- Esto es clave
        ).execute()
        
        return True
    except Exception as e:
        # Si sigue fallando, es que el bot no tiene permiso de Editor en esa carpeta
        st.error(f"Error técnico al subir a Drive: {e}")
        return False

# ==========================================
# 2. INTERFAZ DE LA APLICACIÓN
# ==========================================
st.set_page_config(page_title="Tasador Experto V2.0", layout="centered")
st.title("🚜 Sistema de Tasación Centralizada")
st.write("Los informes se guardarán automáticamente en la carpeta compartida.")

# Formulario de datos
c1, c2 = st.columns(2)
with c1:
    marca = st.text_input("Marca*", placeholder="Ej: John Deere")
    anio = st.text_input("Año*", placeholder="Ej: 2018")
with c2:
    modelo = st.text_input("Modelo*", placeholder="Ej: 6155M")
    horas = st.number_input("Horas*", min_value=0)

observaciones = st.text_area("Extras e Incidencias", placeholder="Pala, estado de neumáticos, averías...")

# Subida de fotos
fotos = st.file_uploader("Fotos del vehículo (Mínimo 5)", accept_multiple_files=True)

if fotos:
    st.image(fotos, width=100) # Previsualización rápida

st.divider()

# ==========================================
# 3. EJECUCIÓN
# ==========================================
if st.button("🚀 FINALIZAR Y ENVIAR A CENTRAL"):
    if not fotos or not marca or not modelo:
        st.warning("⚠️ Completa los campos obligatorios y sube las fotos.")
    else:
        try:
            # Usamos Gemini 2.5 Flash para el análisis
            model = genai.GenerativeModel('gemini-2.5-flash') # Cambiar a 2.5 si ya tienes acceso
            
            with st.spinner('Analizando y enviando informe...'):
                # 1. IA analiza fotos y datos
                prompt = f"Actúa como perito tasador. Analiza este {marca} {modelo} del {anio} con {horas}h. Extras: {observaciones}. Genera un informe profesional con precios de mercado."
                res = model.generate_content([prompt] + [Image.open(f) for f in fotos])
                
                # Mostramos resultado en la pantalla del móvil del vendedor
                st.success("✅ Tasación generada")
                st.markdown(res.text)

                # 2. Creamos el archivo HTML "Todo en Uno"
                html_fotos = ""
                for f in fotos:
                    b64 = imagen_a_base64(f)
                    html_fotos += f'<div style="margin-bottom:20px;"><img src="data:image/jpeg;base64,{b64}" style="width:100%; max-width:600px; border-radius:10px;"></div>'

                texto_ia_html = res.text.replace('\n', '<br>')
                fecha_hoy = datetime.date.today().strftime('%d/%m/%Y')
                
                contenido_final = f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 30px; color: #333; line-height: 1.6;">
                    <h1 style="color: #2e7d32;">Informe de Tasación Profesional</h1>
                    <p><b>Unidad:</b> {marca} {modelo} ({anio})</p>
                    <p><b>Fecha de peritaje:</b> {fecha_hoy}</p>
                    <hr>
                    <div style="background: #f9f9f9; padding: 20px; border-radius: 10px;">
                        {texto_ia_html}
                    </div>
                    <hr>
                    <h2 style="color: #2e7d32;">Evidencia Fotográfica</h2>
                    {html_fotos}
                    <p style="font-size: 0.8em; color: #888;">Generado por Tasador Experto V2.0</p>
                </body>
                </html>
                """

                # 3. Subida a tu carpeta específica
                ID_CARPETA = "1nC0BvL3Yv1X6ui0oK1Nz0SJ0mSYEBLzK"
                nombre_archivo = f"TASACION_{marca}_{modelo}_{datetime.date.today()}.html"
                
                if subir_a_drive(nombre_archivo, contenido_final, ID_CARPETA):
                    st.balloons()
                    st.success(f"📂 ¡ENVIADO! El informe ya está en la carpeta de la central.")
                
        except Exception as e:
            st.error(f"Se produjo un error: {e}")
