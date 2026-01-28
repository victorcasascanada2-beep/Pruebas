import streamlit as st
from google import genai
from PIL import Image
import io

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # Forzamos Vertex AI (tu vía de pago despejada)
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options={'api_version': 'v1'}
    )
    
    prompt = f"Actúa como perito experto. Tasa este {marca} {modelo} de {anio} con {horas} horas. Notas: {observaciones}"
    contenidos = [prompt]
    
    for foto in fotos_subidas:
        img = Image.open(foto)
        # Reducción para evitar el error 429
        img.thumbnail((800, 800))
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        contenidos.append(Image.open(buf))
    
    try:
        res = client.models.generate_content(model="gemini-1.5-flash", contents=contenidos)
        return res.text
    except Exception as e:
        return f"Error en la IA: {e}"
