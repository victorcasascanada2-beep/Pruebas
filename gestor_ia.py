from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # 1. Configuración con el nuevo Cliente Profesional
    # Usamos la nueva librería que detecta tu proyecto de Vertex AI
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # 2. Tu prompt "seco" y sin fantasías (Tal cual lo tenías)
    prompt = f"""
    NO INVENTES DATOS. NO TE PRESENTES COMO IA. ACTÚA COMO UN COMPRADOR DE MAQUINARIA AGRESIVO EN ESPAÑA.
    
    OBJETIVO: Tasación REAL de compra-venta para un {marca} {modelo} ({anio}) con {horas} horas.
    EXTRAS: {observaciones}

    INSTRUCCIONES DE CÁLCULO (OBLIGATORIAS):
    1. FUENTES: Busca exclusivamente en Agriaffaires y Milanuncios (Mercado España/Francia). 
    2. FILTRO FENDT: Si es Fendt, ignora precios de E-FARM o Traktorpool (están fuera de la realidad del mercado español).
    3. PENALIZACIÓN POR USO: Si el tractor supera las 8.000 horas, aplica una penalización agresiva. Si tiene 13.000 horas o más, valóralo como unidad de alta fatiga (valor cercano a liquidación).
    4. DETECTOR DE "MAQUILLAJE": Si ves plásticos en asientos/palancas con más de 2.000 horas, ignóralos; es estética, no conservación.
    5. MEDIA TRUNCADA REAL: Elimina el 20% más caro de los anuncios que encuentres.
    6. NO TIRES POR TIERRA LA MAQUINA TRATA TODO CON RESPETO.
    
    LÓGICA DE VALORES:
    - PRECIO DE ATERRIZAJE: Valor de mercado real en España para venta rápida.
    - PRECIO DE COMPRA: Aterrizaje menos 15% (margen de beneficio, transporte y preparación).

    SALIDA REQUERIDA (Directa al grano pero con humildad, SIN TABLAS INVENTADAS):
    - RESUMEN VISUAL: [Análisis técnico de fotos: Tripuntal, neumáticos, estado motor].
    - ANÁLISIS DE MERCADO: [Nº de unidades reales encontradas y precio medio real].
    - ESTADO GENERAL: [Puntuación 1-10].
    - A NO SER QUE SE PIDA EXPRESAMENTE NO SAQUES TABLA DE DATOS.
    - RESULTADOS FINALES:
      * VALOR DE MERCADO (Aterrizaje): [Cifra en €]
      * PRECIO DE COMPRA SUGERIDO (PVP): [Cifra en €]
    
    - NOTA COMERCIAL: [Justificación realista basada en horas y mercado actual].
    """

    # 3. Preparación de contenidos (Texto + Fotos) para la nueva librería
    contenidos = [prompt]
    for f in fotos_subidas:
        img = Image.open(f)
        contenidos.append(img)
    
    # 4. Llamada al modelo usando el nombre profesional que funciona
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=contenidos
        )
        return res.text
    except Exception as e:
        return f"Error en la IA: {e}"
