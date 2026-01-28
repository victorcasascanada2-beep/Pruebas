import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from datetime import datetime

class GestorDrive:
    def __init__(self):
        # Cargamos las credenciales desde el TOML de Secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        self.service = build('drive', 'v3', credentials=creds)
        self.folder_id_base = "TU_ID_DE_CARPETA_PRINCIPAL" # Pon aquí el ID de la carpeta madre

    def crear_carpeta_tasacion(self):
        # Genera el nombre: 280125164033
        nombre_carpeta = datetime.now().strftime("%d%m%y%H%M%S")
        
        file_metadata = {
            'name': nombre_carpeta,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.folder_id_base]
        }
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id'), nombre_carpeta

    def subir_archivo(self, nombre, contenido, folder_id, mime_type='image/jpeg'):
        file_metadata = {
            'name': nombre,
            'parents': [folder_id]
        }
        
        # Si el contenido ya son bytes (foto original), lo usamos directamente
        # Si es texto (HTML), lo convertimos a bytes
        if isinstance(contenido, str):
            fh = io.BytesIO(contenido.encode('utf-8'))
        else:
            # Para las fotos subidas desde Streamlit
            fh = io.BytesIO(contenido.getvalue())
            
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def guardar_todo_en_drive(fotos_originales, html_contenido):
    try:
        drive = GestorDrive()
        # 1. Crear la subcarpeta con fecha y hora
        id_subcarpeta, nombre_subcarpeta = drive.crear_carpeta_tasacion()
        
        # 2. Subir las fotos ORIGINALES (sin procesar por la IA)
        for i, foto in enumerate(fotos_originales):
            drive.subir_archivo(f"foto_{i+1}.jpg", foto, id_subcarpeta)
            
        # 3. Subir el informe HTML
        drive.subir_archivo("informe_tasacion.html", html_contenido, id_subcarpeta, 'text/html')
        
        return True, nombre_subcarpeta
    except Exception as e:
        return False, str(e)
