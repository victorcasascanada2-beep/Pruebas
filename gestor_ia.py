# gestor_ia.py
import google.generativeai as genai
from PIL import Image
import streamlit as st

def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Mantenemos tu prompt exacto porque ya te da los resultados que buscas
    prompt = f"""
    Actúa como un perito tasador y director comercial de maquinaria agrícola. Tu objetivo es calcular el valor de compra y el precio de venta recomendado para un {marca} {modelo} ({anio}).

    DATOS DE LA UNIDAD:
    - Modelo: {marca} {modelo} | Año: {anio} | Uso: {horas} horas.
    - Extras declarados: {observaciones} (Incluyendo Tripuntal Zuidberg y Neumáticos al 75% si procede).

    INSTRUCCIONES DE ANÁLISIS:
    1. ANÁLISIS VISUAL FOTO A FOTO:
       - Identifica y resume cada imagen. Busca específicamente el Tripuntal delantero, el estado de los tacos de las ruedas y la limpieza de la cabina/motor.
       - Si detectas extras de alto valor (Zuidberg, pesas, suspensión), úsalos para justificar un posicionamiento en la banda alta.
    2.- Si la unidad tiene mas de 2000 horas y ves en las fotos protecciones de plastico en palancas o asiento no las tomes como que son de fabrica, eso normalmente se hace
        para presentar mas pulcredad no es porque las conserve de fabrica.
    3. Prioriza anuncios actualizados y tu conocimiento profundo de mercado de España, Francia y Portugal. Solo usa anuncios del resto de Europa si no hay suficiente muestra, pero aplica un factor de corrección 
        a la baja del 15% por costes de importación y logística."
    4. PROCEDIMIENTO ESTADÍSTICO (Media Truncada):
       - Busca en Agriaffaires, y Milanuncios y si encuentras pocos resultados, usa otros portales de compraventa especializados en el sector.  Si el tractor es fendt elimina automaticamente efarm o tractorpool de la ecuacion.
       - Toma toda la muestra europea de este modelo y año. Ordena por precio y ELIMINA el 10% más caro y el 10% más barato para limpiar la muestra de anuncios irreales.
        -Asegurate de que el precio sea en euros.
    5. CÁLCULO DE VALORES (Lógica Comercial):
       - PRECIO DE ATERRIZAJE: Es el valor real de mercado basado en la media truncada, ajustado por horas y extras visuales. (Este debe ser vuestro valor de anuncio).
       - PRECIO DE COMPRA (PVP): Sobre el precio de aterrizaje, resta un margen del 15 para cubrir preparación.

    6. En el inicio de la salida no utilices mensajes en cuanto a tus limitaciones como IA, asume tu rol de experto en compraventa de maquinaria con plenos conocimientos de mercado.
    SALIDA DE DATOS REQUERIDA:
    -TABLA DE ANUNCIOS [Una tabla con pais ciudad año y precio de anuncio]
    - MUESTRA ANALIZADA: [Nº anuncios encontrados en Europa]
    - RESUMEN VISUAL: [Breve descripción de lo detectado en las fotos subidas]
    - ESTADO GENERAL: [Puntuación 1-10]
    - RESULTADOS FINALES:
      * VALOR DE MERCADO (Aterrizaje): [Cifra en €]
      * PRECIO DE COMPRA SUGERIDA (PVP): [Cifra en €] 
    
    - NOTA COMERCIAL: [Justificación de por qué este tractor permite ese margen (ej: "Unidad muy buscada por horas y tripuntal Zuidberg").]
    """

    contenido = [prompt]
    for f in fotos_subidas:
        img = Image.open(f)
        contenido.append(img)
    
    res = model.generate_content(contenido)
    return res.text
