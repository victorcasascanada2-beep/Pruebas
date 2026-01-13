import streamlit as st
import os

# 1. Nombre del archivo que quieres arrancar (CON el .py esta vez)
VERSION_ACTIVA = "VersionExperta2_0.py" 

def lanzar_version(archivo):
    if os.path.exists(archivo):
        # Este comando lee el archivo y lo ejecuta directamente
        exec(open(archivo, encoding="utf-8").read(), globals())
    else:
        st.error(f"No encuentro el archivo {archivo} en GitHub")

# Ejecutamos
lanzar_version(VERSION_ACTIVA)
