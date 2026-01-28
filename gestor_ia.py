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
    
    prompt = f" Actúa como experto tasador de Agrícola Noroeste. Busca y cerciorate de que los datos son reales
            Analiza este {marca} {modelo} del año {anio} con {horas} horas.
            
            TAREAS:
            1. Analiza el estado visual a través de las fotos adjuntas. No des una salida de comentarios mas alla de 30 palabras por foto
            2. Busca precios reales de mercado en Agriaffaires, Tractorpool y E-farm para unidades similares.
            3. Genera una tabla comparativa de 10-15 unidades.
            4. Calcula:
               - Precio Venta (Aterrizaje).
               - Precio Compra recomendado para Agrícola Noroeste.
            
            Notas adicionales: {observaciones}"
    contenidos = [prompt]
    
    for foto in fotos_subidas:
        img = Image.open(foto)
        # Reducción para evitar el error 429
        img.thumbnail((800, 800))
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        contenidos.append(Image.open(buf))
    
    try:
        res = client.models.generate_content(model="gemini-2.5-flash-preview-09-2025", contents=contenidos)
        return res.text
    except Exception as e:
        return f"Error en la IA: {e}"
