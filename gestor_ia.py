import streamlit as st
from google import genai  # <--- ESTA LÍNEA ES LA QUE TE FALTA
from PIL import Image
import io

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # Inicializamos el cliente con la API KEY de tus secrets
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    prompt = f"""Actúa como experto tasador de Agrícola Noroeste. 
            Analiza este {marca} {modelo} del año {anio} con {horas} horas.
            
            TAREAS:
            1. Analiza el estado visual a través de las fotos adjuntas.
            2. Busca precios reales de mercado en Agriaffaires, Tractorpool y E-farm.
            3. Genera una tabla comparativa de unidades similares.
            4. Calcula:
               - Precio Venta (Aterrizaje).
               - Precio Compra recomendado para Agrícola Noroeste.
            
            Notas adicionales: {observaciones}"""
    
    contenidos = [prompt]
    
    # Procesamiento de fotos
    for foto in fotos_subidas:
        foto.seek(0) # Asegura que empezamos a leer la foto desde el inicio
        img = Image.open(foto)
        img.thumbnail((800, 800)) # Reducción para evitar errores de cuota (429)
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        buf.seek(0)
        contenidos.append(Image.open(buf))
    
    try:
        # Usamos el modelo 2.0 que es el más rápido y estable para este código
        res = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=contenidos
        )
        return res.text
    except Exception as e:
        return f"Error en la IA: {e}"
