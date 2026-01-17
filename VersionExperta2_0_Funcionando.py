import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
# main.py
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
    """, unsafe_allow_status=True)
def main():
    # 1. Configuración de API
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Error: Configura GOOGLE_API_KEY en los Secrets de Streamlit.")
        return
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    st.title("🚜 Peritaje Profesional V2.0")

    # --- DATOS OBLIGATORIOS (Línea 12 corregida) ---
    st.subheader("📝 Datos de la Máquina")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        marca = st.text_input("Marca*", key="marca_input")
    with col2:
        modelo = st.text_input("Modelo*", key="modelo_input")
    with col3:
        anio = st.text_input("Año*", key="anio_input")
    
    observaciones = st.text_area("Incidencias y Extras (Pala, averías, pintura...)", height=100)

    # --- GESTIÓN DE FOTOS ---
    st.divider()
    st.subheader("📸 Fotos (Mínimo 5)")
    fotos_subidas = st.file_uploader("Sube entre 5 y 10 fotos", type=['jpg','jpeg','png'], accept_multiple_files=True)

    comentarios = []
    if fotos_subidas:
        for i, foto in enumerate(fotos_subidas[:10]):
            c1, c2 = st.columns([1, 3])
            c1.image(foto, use_container_width=True)
            # Campo de comentario de máximo 4 líneas
            nota = c2.text_area(f"Nota para foto {i+1}", key=f"nota_{i}", height=90, placeholder="Describa daños o detalles...")
            comentarios.append(nota)

    # --- BOTÓN DE ACCIÓN ---
    st.divider()
    if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
        if not marca or not modelo or not anio:
            st.warning("⚠️ Marca, Modelo y Año son obligatorios.")
        elif len(fotos_subidas) < 5:
            st.warning("⚠️ Sube al menos 5 fotografías.")
        else:
            # Barra de progreso
            barra = st.progress(0)
            texto_estado = st.empty()
            for p in range(100):
                time.sleep(0.02)
                barra.progress(p + 1)
                if p == 20: texto_estado.text("🔍 Analizando imágenes...")
                if p == 50: texto_estado.text("📊 Consultando mercado europeo...")
                if p == 85: texto_estado.text("⚖️ Ajustando precio de compra...")

            try:
                # Usamos el modelo flash que es más rápido para peritajes
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Preparamos las notas de las fotos
                notas_texto = ""
                for idx, c in enumerate(comentarios):
                    notas_texto += f"- Foto {idx+1}: {c}\n"

                prompt = f"""
                Actúa como tasador profesional de maquinaria agrícola.
                DATOS: Marca {marca}, Modelo {modelo}, Año {anio}.
                INCIDENCIAS: {observaciones}
                NOTAS DE FOTOS:
                {notas_texto}

                TAREA:
                1. Extrae el NÚMERO DE SERIE si es visible en alguna placa.
                2. Calcula un PRECIO DE COMPRA (valor para el concesionario). 
                   Debe ser un precio para captar la máquina, tirando a la BAJA para dejar margen de reventa, pero realista según mercado europeo.
                3. Sé muy breve y directo.
                """

                # Combinar texto y fotos para la IA
                input_ia = [prompt]
                for f in fotos_subidas:
                    input_ia.append(Image.open(f))

                resultado = model.generate_content(input_ia)
                
                st.success("✅ Peritaje Finalizado")
                st.markdown("### Resultado:")
                st.write(resultado.text)
                
            except Exception as error_ia:
                st.error(f"Error en el proceso: {error_ia}")

# Ejecución
if __name__ == "__main__":
    main()
