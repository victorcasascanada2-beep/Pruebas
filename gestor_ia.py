# gestor_ia.py
import google.generativeai as genai
from PIL import Image
import streamlit as st

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Mantenemos tu prompt exacto porque ya te da los resultados que buscas
   # gestor_ia.py

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # (Configuración de API igual que antes...)
    
    prompt = f"""
    NO INVENTES DATOS. NO TE PRESENTES COMO IA. ACTÚA COMO UN COMPRADOR DE MAQUINARIA AGRESIVO EN ESPAÑA.
    
    OBJETIVO: Tasación REAL de compra-venta para un {marca} {modelo} ({anio}) con {horas} horas.
    EXTRAS: {observaciones}

    INSTRUCCIONES DE CÁLCULO (OBLIGATORIAS):
    1. FUENTES: Busca exclusivamente en Agriaffaires y Milanuncios (Mercado España/Francia). 
    2. FILTRO FENDT: Si es Fendt, ignora precios de E-FARM o Traktorpool (están fuera de la realidad del mercado español).
    3. PENALIZACIÓN POR USO: Las unidades con más de 8.000 horas deben sufrir una depreciación agresiva. Si tiene 13.000 horas o más, valóralo como unidad de alta fatiga (valor cercano a liquidación).
    4. DETECTOR DE "MAQUILLAJE": Si en las fotos ves plásticos en asientos/palancas con más de 2.000 horas, ignóralos; es estética para la venta, no conservación de fábrica.
    5. MEDIA TRUNCADA REAL: Toma los precios de Agriaffaires/Milanuncios. Elimina el 20% más caro (anuncios que no se venden).
    
    LÓGICA DE VALORES:
    - PRECIO DE ATERRIZAJE: Valor de mercado real en España para venta rápida.
    - PRECIO DE COMPRA: Aterrizaje menos 15% (margen de riesgo, transporte y preparación).

    SALIDA REQUERIDA (Directa al grano, sin tablas de anuncios inventadas):
    - RESUMEN VISUAL: [Análisis técnico de lo que ves en las fotos (Tripuntal, neumáticos, estado motor)].
    - ANÁLISIS DE MERCADO: [Nº de unidades reales encontradas en Agriaffaires/Milanuncios y precio medio detectado].
    - ESTADO GENERAL: [Puntuación 1-10 según horas y fotos].
    
    - RESULTADOS FINALES:
      * VALOR DE MERCADO (Aterrizaje): [Cifra en €]
      * PRECIO DE COMPRA SUGERIDO (PVP): [Cifra en €]
    
    - NOTA COMERCIAL: [Justificación realista del precio basada en las horas y el mercado actual].
    """

    # ... (Resto de la lógica de procesamiento de fotos y generación de contenido igual)

    contenido = [prompt]
    for f in fotos_subidas:
        img = Image.open(f)
        contenido.append(img)
    
    res = model.generate_content(contenido)
    return res.text
