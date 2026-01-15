# --- BOTÓN Y LÓGICA ACTUALIZADA ---
if st.button("🚀 REALIZAR TASACIÓN"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Rellena Marca, Modelo y Año.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Sube al menos 5 fotos.")
    else:
        try:
            # Usamos el modelo 2.5-flash como tienes en tus instrucciones
            model = genai.GenerativeModel('gemini-2.5-flash')

            with st.spinner('🔍 Procesando imágenes y consultando mercados...'):
                contenido = [prompt]
                
                for f in fotos_subidas:
                    img = Image.open(f)
                    # REDIMENSIONAR: Reducimos la imagen para no agotar la cuota (max 800px)
                    img.thumbnail((800, 800)) 
                    contenido.append(img)
                
                # Llamada al motor
                res = model.generate_content(contenido)
            
            st.success("✅ Tasación Finalizada")
            st.markdown(res.text)
            
            # (Aquí seguiría tu código de PDF y Drive que ya tenemos)
            
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Límite de Google alcanzado. Espera 30 segundos y vuelve a dar al botón. (Es debido a la alta resolución de las fotos).")
            else:
                st.error(f"❌ Error: {e}")
