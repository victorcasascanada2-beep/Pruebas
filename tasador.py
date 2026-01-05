import streamlit as st

st.title("¡Hola Mundo!")
st.write("Si estás viendo esto, la conexión con GitHub y Streamlit funciona perfectamente.")

nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.success(f"¡Un saludo, {nombre}! El sistema está vivo.")
