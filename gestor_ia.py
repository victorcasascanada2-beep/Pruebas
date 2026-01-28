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
   ### ROL: PERITO TASADOR SENIOR - AGRÍCOLA NOROESTE
    Genera un informe técnico de valoración para un {marca} {modelo} ({anio}) con {horas} horas.
    EXTRAS DECLARADOS: {observaciones}

    ### REGLAS CRÍTICAS DE TASACIÓN:
    1. FUENTES: Busca exclusivamente en Agriaffaires y Milanuncios (Mercado España/Francia).
    2. FILTRO FENDT: Si es Fendt, ignora precios de E-FARM o Traktorpool por estar fuera de la realidad española.
    3. PENALIZACIÓN POR USO: >8.000h aplica penalización agresiva. >13.000h valorar como unidad de alta fatiga (valor de liquidación).
    4. DETECTOR DE ESTÉTICA: Ignora plásticos en asientos/mandos si tiene >2.000h; prioriza conservación mecánica.
    5. MEDIA TRUNCADA: Elimina el 20% más caro de los anuncios encontrados para evitar distorsiones.
    6. RESPETO: Mantén un tono profesional y respetuoso, sin devaluar la máquina innecesariamente.

    ### ESTRUCTURA DE SALIDA REQUERIDA:

    #### 1. RESUMEN VISUAL TÉCNICO
    [Análisis de fotos: Estado de neumáticos, motor, tripuntal/pala y limpieza general].

    #### 2. COMPARATIVA DE MERCADO (8-10 UNIDADES REALES)
    | Modelo | Año | Horas | Ubicación | Fuente | Precio (€) |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    [IA: Rellena con 8-10 resultados reales coherentes con el mercado actual]

    #### 3. ANÁLISIS DE ESTADO
    - **Puntuación General:** [1-10]
    - **Análisis de Mercado:** [Descripción del volumen de unidades encontradas y demanda actual].

    #### 4. RESULTADOS DE VALORACIÓN (Cifras Finales)
    - **VALOR DE MERCADO (Aterrizaje):** [Cifra €] (Precio de venta rápida en España).
    - **PRECIO DE COMPRA SUGERIDO:** [Cifra €] (Cálculo: Aterrizaje - 15% para margen, transporte y preparación).

    #### 5. NOTA COMERCIAL
    [Justificación profesional y realista basada en las horas, el estado visual y la situación del mercado].
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
