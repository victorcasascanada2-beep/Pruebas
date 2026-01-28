import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def subir_informe_drive(nombre_archivo, contenido_html):
    try:
        # Cargamos credenciales desde secrets
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        
        # Construimos el servicio de Drive
        service = build('drive', 'v3', credentials=creds)
        
        # Metadata del archivo
        file_metadata = {
            'name': nombre_archivo,
            'parents': [st.secrets["google_drive"]["id_carpeta"]],
            'mimeType': 'text/html'
        }
        
        # Convertimos el string HTML a un stream de bytes
        fh = io.BytesIO(contenido_html.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype='text/html', resumable=True)
        
        # Subida
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Error subiendo a Drive: {e}")
        return None
