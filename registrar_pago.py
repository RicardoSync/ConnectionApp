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
import random

def leer_credenciales():
        with open('nombre_wisp.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos

# Función para registrar un pago y actualizar el estado y el próximo pago
def registrar_pago_recibo(id_cliente, nombreCliente, mensualidad, fechaPago, estado, proximoPago, efectivo):
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

    nombreCliente = nombreCliente
    fecha = fechaPago
    total = mensualidad
    concepto = "Servicio de internet"
    archivo_salida = nombreCliente + fechaPago + ".png"
    logo_path = "icons/logo.png"
    num_recibo = random.randint(0, 10000)
    credenciales = leer_credenciales()
    empresa_nombre = credenciales['nombre']
    mensaje_cliente = credenciales['mensaje']
    empresa_direccion = credenciales['direccion']
    empresa_telefono = credenciales['telefono']
    efectivo = efectivo
    nombre_cliente = nombreCliente
    proximo_pago = proximoPago

    crear_recibo_imagen(empresa_nombre, empresa_direccion, empresa_telefono, nombre_cliente ,num_recibo, fecha, proximo_pago, total, efectivo, concepto, mensaje_cliente, logo_path, archivo_salida)

def crear_recibo_imagen(empresa_nombre, empresa_direccion, empresa_telefono, nombre_cliente,  num_recibo, fecha, proximo_pago, total, efectivo, concepto, mensaje_cliente, logo_path, archivo_salida):
    # Asegurarse de que total y efectivo son números
    try:
        total = float(total)
        efectivo = float(efectivo)
    except ValueError:
        print("Error: 'total' y 'efectivo' deben ser valores numéricos.")
        return
    
    # Calcular el cambio
    cambio = efectivo - total
    if cambio < 0:
        print("Error: El efectivo recibido es menor que el total. No se puede generar el recibo.")
        return
    
    # Crear una nueva imagen en blanco
    width, height = 600, 800
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
    draw.text((20, y_offset), f"Nombre cliente: {nombre_cliente}", font=font_text, fill="black")

    y_offset += 20
    draw.text((20, y_offset), f"Recibo № {num_recibo}", font=font_text, fill="black")
    y_offset += 20
    draw.text((20, y_offset), f"Fecha: {fecha}", font=font_text, fill="black")
    

    #Proximo pago
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)

    y_offset += 20
    draw.text((20, y_offset), f"Por favor realizar su pago en la proxima fecha: {proximo_pago}", font=font_text, fill="black")

    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Concepto
    y_offset += 20
    draw.text((20, y_offset), f"Concepto: {concepto}", font=font_text, fill="black")
    
    # Total
    y_offset += 30
    draw.text((20, y_offset), "TOTAL", font=font_bold, fill="black")
    
    total_text = f"${total:.2f}"
    total_bbox = draw.textbbox((0, 0), total_text, font=font_bold)
    total_text_width = total_bbox[2] - total_bbox[0]
    draw.text((width - total_text_width - 20, y_offset), total_text, font=font_bold, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Efectivo recibido
    y_offset += 20
    draw.text((20, y_offset), "Efectivo", font=font_text, fill="black")
    
    efectivo_text = f"${efectivo:.2f}"
    efectivo_bbox = draw.textbbox((0, 0), efectivo_text, font=font_text)
    efectivo_text_width = efectivo_bbox[2] - efectivo_bbox[0]
    draw.text((width - efectivo_text_width - 20, y_offset), efectivo_text, font=font_text, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)

    # Cambio
    y_offset += 20
    draw.text((20, y_offset), "Cambio", font=font_text, fill="black")
    
    cambio_text = f"${cambio:.2f}"
    cambio_bbox = draw.textbbox((0, 0), cambio_text, font=font_text)
    cambio_text_width = cambio_bbox[2] - cambio_bbox[0]
    draw.text((width - cambio_text_width - 20, y_offset), cambio_text, font=font_text, fill="black")
    
    # Línea punteada
    y_offset += 30
    draw.line((20, y_offset, width - 20, y_offset), fill="black", width=2)
    
    # Mensaje para el cliente
    y_offset += 20
    draw.text((20, y_offset), mensaje_cliente, font=font_text, fill="black")
    
    # Mensaje de agradecimiento
    y_offset += 40
    draw.text((width / 2 - 80, y_offset), "Conserva tu comprobante!", font=font_text, fill="black")
    
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
