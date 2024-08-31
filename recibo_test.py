from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import platform
import datetime
import os
import subprocess
import random

def crear_recibo_imagen(empresa_nombre, empresa_direccion, empresa_telefono, num_recibo, fecha, total, efectivo, concepto, mensaje_cliente, logo_path, archivo_salida):
    # Crear una nueva imagen en blanco
    width, height = 400, 600
    imagen = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(imagen)
    
    # Cargar fuentes
    try:
        font_path = Path("arial.ttf")  # Ajusta según el entorno
        font_title = ImageFont.truetype(str(font_path), 24)
        font_text = ImageFont.truetype(str(font_path), 16)
        font_bold = ImageFont.truetype(str(font_path), 20)
    except IOError:
        print("No se pudo cargar la fuente arial.ttf. Asegúrate de que la fuente esté disponible.")
        return
    
    # Cargar el logotipo
    try:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
    except IOError:
        print(f"No se pudo cargar el logotipo desde {logo_path}. Asegúrate de que el archivo esté disponible.")
        return
    
    # Redimensionar el logotipo si es necesario
    logo_width, logo_height = logo.size
    max_logo_width = 100
    if logo_width > max_logo_width:
        scale_factor = max_logo_width / logo_width
        logo = logo.resize((int(logo_width * scale_factor), int(logo_height * scale_factor)))
    
    # Colocar el logotipo en la parte superior
    imagen.paste(logo, (int((width - logo.size[0]) / 2), 10), logo)
    
    # Offset inicial después del logotipo
    y_offset = logo.size[1] + 20
    
    # Dibujar encabezado de la tienda
    draw.text((20, y_offset), empresa_nombre, font=font_bold, fill="black")
    y_offset += 30
    draw.text((20, y_offset), empresa_direccion, font=font_text, fill="black")
    y_offset += 20
    draw.text((20, y_offset), f"Tel: {empresa_telefono}", font=font_text, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Información del recibo
    y_offset += 20
    draw.text((20, y_offset), f"Recibo № {num_recibo}", font=font_text, fill="black")
    y_offset += 20
    draw.text((20, y_offset), f"Fecha: {fecha}", font=font_text, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Concepto
    y_offset += 20
    draw.text((20, y_offset), f"Concepto: {concepto}", font=font_text, fill="black")
    
    # Total
    y_offset += 30
    draw.text((20, y_offset), "TOTAL", font=font_bold, fill="black")
    draw.text((width - 100, y_offset), f"${total:.2f}", font=font_bold, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Efectivo recibido
    y_offset += 20
    draw.text((20, y_offset), "Efectivo", font=font_text, fill="black")
    draw.text((width - 100, y_offset), f"${efectivo:.2f}", font=font_text, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Mensaje para el cliente
    y_offset += 20
    draw.text((20, y_offset), mensaje_cliente, font=font_text, fill="black")
    
    # Mensaje de agradecimiento
    y_offset += 40
    draw.text((width / 2 - 80, y_offset), "¡Gracias por su compra!", font=font_text, fill="black")
    
    # Guardar la imagen
    directorio_recibos = Path("recibos")
    
    if platform.system() == "Windows":
        directorio_recibos = Path(os.path.expanduser("~\\recibos"))
    elif platform.system() in ["Linux", "Darwin"]:
        directorio_recibos = Path(os.path.expanduser("~/recibos"))

    directorio_recibos.mkdir(parents=True, exist_ok=True)
    
    ruta_salida = directorio_recibos / archivo_salida
    imagen.save(ruta_salida)
    print(f"Recibo guardado como {ruta_salida}")

    # Abrir el archivo
    if platform.system() == "Windows":
        os.startfile(ruta_salida)
    elif platform.system() == "Darwin":
        subprocess.run(["open", ruta_salida])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", ruta_salida])


# Ejemplo de uso:
num_recibo_aleatorio = random.randint(0, 1000)

crear_recibo_imagen(
    empresa_nombre="Doblenet",
    empresa_direccion="Joaquin Amaro",
    empresa_telefono="(098) 765-4321",
    num_recibo=num_recibo_aleatorio,
    fecha="21/09/2017 18:35",
    total=300.00,
    efectivo=300.00,
    concepto="Pago de servicio de internet",
    mensaje_cliente="¡Recuerde pagar puntualmente para mantener su servicio activo!",
    logo_path="icons/logo.png",  # Reemplaza con la ruta real del logotipo
    archivo_salida="recibo_ejemplo.png"
)