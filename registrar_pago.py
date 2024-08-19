import datetime
import os
import platform
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sqlite3
from tkinter import messagebox
import json
import subprocess
from notificacion_test import mostrar_notificacion
from desbloqueo_automatico import get_datos

def leer_credenciales():
        with open('nombre_wisp.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos

# Función para registrar un pago y actualizar el estado y el próximo pago
def registrar_pago_recibo(id_cliente, nombreCliente, mensualidad, fechaPago, estado, proximoPago):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    
    try:
        # Registrar el pago en la tabla pagos
        cursor.execute('''
            INSERT INTO pagos (nombreCliente, mensualidad, fechaPago, proximoPago)
            VALUES (?, ?, ?, ?)
        ''', (nombreCliente, mensualidad, fechaPago, proximoPago))
        
        # Actualizar el estado y el próximo pago en la tabla clientes
        cursor.execute('''
            UPDATE clientes
            SET estado = ?, proximoPago = ?
            WHERE id = ?
        ''', (estado, proximoPago, id_cliente))
        
        conn.commit()
        print("Pago registrado y cliente actualizado con éxito")
        get_datos(id_cliente)
    except sqlite3.Error as e:
        print(f"Error al registrar el pago y actualizar el cliente: {e}")
    finally:
        conn.close()


    nombre = nombreCliente
    fecha = fechaPago
    monto = mensualidad
    proximo_pago = proximoPago
    concepto = "Servicio de internet"
    archivo_salida = nombreCliente + fechaPago + ".png"

    credenciales = leer_credenciales()
    titulo = credenciales['nombre']
    mensaje = credenciales['mensaje']

    crear_recibo_imagen(titulo, mensaje, nombre, fecha, monto, proximo_pago, concepto, archivo_salida)


def crear_recibo_imagen(titulo, mensaje, nombre, fecha, monto, proximo_pago, concepto, archivo_salida):
    # Crear una nueva imagen en blanco
    width, height = 600, 700
    imagen = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(imagen)
    
    # Cargar fuentes
    try:
        font_path = Path("arial.ttf")  # Ajusta según el entorno
        font_title = ImageFont.truetype(str(font_path), 24)
        font_subtitle = ImageFont.truetype(str(font_path), 20)
        font_text = ImageFont.truetype(str(font_path), 16)
        font_mono = ImageFont.truetype(str(font_path), 18)
        font_bold = ImageFont.truetype(str(font_path), 20)
    except IOError:
        print("No se pudo cargar la fuente arial.ttf. Asegúrate de que la fuente esté disponible.")
        return
    
    # Cargar el logotipo
    try:
        logo = Image.open("icons/logo.png")
        logo = logo.convert("RGBA")
    except IOError:
        print("No se pudo cargar el logotipo. Asegúrate de que el archivo icons/logo.png esté disponible.")
        return
    
    # Redimensionar el logotipo
    logo_width, logo_height = logo.size
    scale_factor = 0.3  # Escala para reducir el tamaño del logotipo
    logo = logo.resize((int(logo_width * scale_factor), int(logo_height * scale_factor)))
    
    # Añadir el logotipo como marca de agua
    logo_width, logo_height = logo.size
    logo_position = (width - logo_width - 20, height - logo_height - 20)
    
    # Crear una imagen temporal para combinar el logotipo con la imagen principal
    temp_image = Image.new('RGBA', (width, height))
    temp_image.paste(imagen, (0, 0))
    temp_image.paste(logo, logo_position, mask=logo)
    
    # Convertir de vuelta a modo 'RGB'
    imagen = temp_image.convert("RGB")
    draw = ImageDraw.Draw(imagen)
    
    # Título
    text_bbox = draw.textbbox((0, 0), titulo, font=font_title)
    text_width = text_bbox[2] - text_bbox[0]
    x = (width - text_width) / 2
    y = 30
    draw.text((x, y), titulo, font=font_title, fill="black")
    
    # Línea punteada
    draw.line((20, 110, width - 20, 110), fill="black", width=2)
    draw.line((20, 114, width - 20, 114), fill="black", width=2)
    
    # Información del recibo
    draw.text((20, 130), f"Fecha: {fecha}", font=font_text, fill="black")
    
    # Caja de cobro de EBANX
    draw.text((20, 170), mensaje, font=font_text, fill="black")
    
    # Información de pago
    draw.text((20, 250), f"Recibo a nombre de: {nombre}", font=font_text, fill="black")
    draw.text((20, 310), f"Pago el día: {fecha} a la hora: {datetime.datetime.now().strftime('%H:%M')}", font=font_text, fill="black")
    
    # Valor
    draw.text((width / 2 - 60, 350), f"VALOR ${monto}", font=font_bold, fill="black")
    
    # Línea punteada
    draw.line((20, 390, width - 20, 390), fill="black", width=2)
    draw.line((20, 394, width - 20, 394), fill="black", width=2)
    
    # Folio e ID
    draw.text((20, 410), f"Concepto: {concepto}", font=font_text, fill="black")
    draw.text((20, 440), f"Próximo Pago: {proximo_pago}", font=font_text, fill="black")
    
    # Nota de conservación
    draw.text((width / 2 - 120, 470), "*Conserva el comprobante*", font=font_text, fill="black")
    
    # Crear el directorio "recibos" si no existe, utilizando 'os' para compatibilidad multiplataforma
    directorio_recibos = Path("recibos")

    # Determinar el sistema operativo y crear el directorio en consecuencia
    if platform.system() == "Windows":
        directorio_recibos = Path(os.path.expanduser("~\\recibos"))
    elif platform.system() in ["Linux", "Darwin"]:  # Darwin es el nombre del sistema operativo de macOS
        directorio_recibos = Path(os.path.expanduser("~/recibos"))

    directorio_recibos.mkdir(parents=True, exist_ok=True)
    
    # Guardar la imagen en el directorio "recibos"
    ruta_salida = directorio_recibos / archivo_salida
    imagen.save(ruta_salida)
    mensaje = f"Recibo de pago guardado como {ruta_salida}"
    titulo = "Recibo generado"

    messagebox.showinfo("Recibo creado", "Se registro de manera correcta el recibo")

    # Abrir el archivo
    if platform.system() == "Windows":
        os.startfile(ruta_salida)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", ruta_salida])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", ruta_salida])
