import google.generativeai as genai
from PIL import Image
import streamlit as st

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # 1. Configuración (Asegúrate de que esto esté dentro de la función)
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # 2. Definición del modelo (La pieza que te decía que faltaba)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 3. Tu nuevo prompt "seco" y sin fantasías
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
    
    LÓGICA DE VALORES:
    - PRECIO DE ATERRIZAJE: Valor de mercado real en España para venta rápida.
    - PRECIO DE COMPRA: Aterrizaje menos 15% (margen de beneficio, transporte y preparación).

    SALIDA REQUERIDA (Directa al grano, SIN TABLAS INVENTADAS):
    - RESUMEN VISUAL: [Análisis técnico de fotos: Tripuntal, neumáticos, estado motor].
    - ANÁLISIS DE MERCADO: [Nº de unidades reales encontradas y precio medio real].
    - ESTADO GENERAL: [Puntuación 1-10].
    -A NO SER QUE SE PIDA EXPRESAMENTE NO SAQUES TABLA DE DATOS.
    - RESULTADOS FINALES:
      * VALOR DE MERCADO (Aterrizaje): [Cifra en €]
      * PRECIO DE COMPRA SUGERIDO (PVP): [Cifra en €]
    
    - NOTA COMERCIAL: [Justificación realista basada en horas y mercado actual].
    """

    # 4. Preparación y llamada
    contenido = [prompt]
    for f in fotos_subidas:
        img = Image.open(f)
        contenido.append(img)
    
    # Aquí es donde se usa el 'model' definido en el punto 2
    res = model.generate_content(contenido)
    return res.text
