import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image
import datetime
import io

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================

# Configura tu clave de API de Google (Gemini)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def limpiar_texto_para_pdf(texto):
    """
    Limpia el texto de la IA para que sea compatible con FPDF (Latin-1).
    Sustituye símbolos conflictivos y quita el formato Markdown.
    """
    # Sustituciones básicas
    texto = texto.replace('€', 'Euros')
    texto = texto.replace('**', '').replace('*', '').replace('###', '')
    
    # Intentamos codificar en latin-1 (el estándar de FPDF básico)
    return texto.encode('latin-1', 'replace').decode('latin-1')

# ==========================================
# 2. INTERFAZ DE USUARIO (Streamlit)
# ==========================================
st.set_page_config(page_title="Tasador Agrícola Local", layout="wide")

st.title("🚜 Peritaje y Tasación Profesional V2.0")
st.info("Este modo genera el informe y permite la descarga directa a tu ordenador.")

# --- BLOQUE DE DATOS DEL TRACTOR ---
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        marca = st.text_input("Marca*", placeholder="Ej: John Deere")
    with col2:
        modelo = st.text_input("Modelo*", placeholder="Ej: 6820")
    with col3:
        anio = st.text_input("Año*", placeholder="Ej: 2004")
    with col4:
        horas = st.number_input("Horas de uso*", min_value=0, step=100)

    observaciones = st
