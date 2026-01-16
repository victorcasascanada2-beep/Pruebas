# generador_informe.py
import base64

def transformar_foto_a_base64(foto):
    """Convierte la imagen de Streamlit a formato Base64 para incrustarla en el HTML"""
    try:
        bytes_foto = foto.getvalue()
        encoded = base64.b64encode(bytes_foto).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except:
        return ""

def crear_html_descargable(marca, modelo, resultado_ia, fotos_subidas):
    """Genera un archivo HTML único con el texto de la IA y las fotos incrustadas"""
    
    # Creamos la galería de imágenes en HTML
    html_fotos = ""
    for f in fotos_subidas:
        img_base64 = transformar_foto_a_base64(f)
        if img_base64:
            html_fotos += f'''
            <div style="display: inline-block; margin: 10px; border: 1px solid #ddd; padding: 5px; border-radius: 8px;">
                <img src="{img_base64}" style="width:250px; height:auto; border-radius: 5px;">
            </div>'''

    # Construcción del documento completo
    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: auto; padding: 20px; }}
            h1 {{ color: #1b5e20; border-bottom: 2px solid #1b5e20; padding-bottom: 10px; }}
            .informe {{ background: #f1f8e9; padding: 25px; border-radius: 15px; border: 1px solid #c8e6c9; white-space: pre-wrap; }}
            .galeria {{ margin-top: 40px; text-align: center; }}
            h2 {{ color: #333; border-bottom: 1px solid #ccc; }}
            .footer {{ margin-top: 50px; font-size: 0.8em; color: #888; text-align: center; }}
        </style>
    </head>
    <body>
        <h1>Informe de Tasación Profesional</h1>
        <p><strong>Unidad:</strong> {marca} {modelo}</p>
        
        <div class="informe">
{resultado_ia}
        </div>

        <div class="galeria">
            <h2>Evidencia Gráfica</h2>
            {html_fotos}
        </div>

        <div class="footer">
            Generado por Sistema de Peritaje Agrícola V2.0
        </div>
    </body>
    </html>
    """
    return html_completo
