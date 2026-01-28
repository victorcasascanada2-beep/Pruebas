def ejecutar_tasacion_v2(marca, modelo, anio, horas, observaciones, fotos_subidas):
    # Usamos el cliente estándar. 
    # Nota: Si usas Vertex AI puramente, a veces el parámetro 'vertexai=True' es necesario
    client = genai.Client(
        api_key=st.secrets["GOOGLE_API_KEY"],
        http_options={'api_version': 'v1'}
    )
    
    prompt = f"""Actúa como experto tasador de Agrícola Noroeste. Busca y cerciorate de que los datos son reales.
            Analiza este {marca} {modelo} del año {anio} con {horas} horas.
            
            TAREAS:
            1. Analiza el estado visual a través de las fotos adjuntas. No des una salida de comentarios mas alla de 30 palabras por foto.
            2. Busca precios reales de mercado en Agriaffaires, Tractorpool y E-farm para unidades similares.
            3. Genera una tabla comparativa de 10-15 unidades.
            4. Calcula:
               - Precio Venta (Aterrizaje).
               - Precio Compra recomendado para Agrícola Noroeste.
            
            Notas adicionales: {observaciones}"""
    
    contenidos = [prompt]
    
    for foto in fotos_subidas:
        img = Image.open(foto)
        # Reducción para evitar el error 429 y optimizar el envío
        img.thumbnail((800, 800))
        
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        # Importante: Para la nueva librería, pasamos la imagen abierta desde el buffer
        buf.seek(0)
        contenidos.append(Image.open(buf))
    
    try:
        # PRUEBA CON ESTE NOMBRE (Es el 2.0 que funcionó esta mañana):
        res = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=contenidos
        )
        return res.text
    except Exception as e:
        # Si falla el 2.0, el modelo estable de pago es este:
        if "404" in str(e):
            try:
                res = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=contenidos
                )
                return res.text
            except Exception as e2:
                return f"Error en la IA (404): No se encuentra el modelo. Revisa el nombre. Detalle: {e2}"
        return f"Error en la IA: {e}"
