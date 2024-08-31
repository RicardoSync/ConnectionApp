import sqlite3
import subprocess
import os
import platform
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from tkinter import messagebox
import datetime as dt


def antenas_activas():
    messagebox.askokcancel("Iniciar Prueba", "Al iniciar, tomara un tiempo dependiendo de la cantidad de clientes que tengas.")
    # Conectar a la base de datos
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()

    # Obtener la lista de clientes y sus IPs
    cursor.execute('SELECT id, nombre, ip FROM clientes')
    clientes = cursor.fetchall()

    # Lista para almacenar los resultados
    resultados = []

    # Función para hacer ping usando subprocess
    def ping(ip):
        try:
            output = subprocess.check_output(["ping", "-c", "1", "-W", "2", ip], universal_newlines=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # Iterar sobre cada cliente y hacer ping a su IP
    for cliente in clientes:
        id_cliente, nombre, ip = cliente
        
        print(f"Verificando conectividad para {nombre} con IP {ip}...")
        
        if ping(ip):
            estado = 'activado'
            print(f"Antena para {nombre} ({ip}) está Activa.")
        else:
            estado = 'inactivado'
            print(f"Antena para {nombre} ({ip}) está Inactiva.")
        
        # Actualizar el estado en la base de datos
        cursor.execute('UPDATE clientes SET estado = ? WHERE id = ?', (estado, id_cliente))
        conn.commit()
        
        # Guardar el resultado en la lista
        resultados.append((nombre, ip, estado))

    # Cerrar la conexión a la base de datos
    conn.close()

    print("Verificación completada.")

    # Definir la ruta para guardar el PDF
    current_date = str(dt.date.today())
    titulo = "Dispositivos conectados"
    archivo_salida = titulo + current_date + ".pdf"
    #archivo_salida = "resultado_conectividad.pdf"
    directorio_recibos = Path("recibos")

    if platform.system() == "Windows":
        directorio_recibos = Path(os.path.expanduser("~\\recibos"))
    elif platform.system() in ["Linux", "Darwin"]:
        directorio_recibos = Path(os.path.expanduser("~/recibos"))

    directorio_recibos.mkdir(parents=True, exist_ok=True)
    ruta_salida = directorio_recibos / archivo_salida

    # Crear el PDF en la ruta especificada
    documento = SimpleDocTemplate(str(ruta_salida), pagesize=letter)

    # Configurar estilos
    styles = getSampleStyleSheet()

    # Crear los datos para la tabla
    data = [["Nombre", "IP", "Estado"]]
    for nombre, ip, estado in resultados:
        color = "green" if estado == "activado" else "red"
        data.append([nombre, ip, estado])

    # Crear la tabla
    tabla = Table(data, colWidths=[200, 150, 100])

    # Estilo de la tabla
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Aplicar colores a las filas según el estado
    for i, row in enumerate(data[1:], start=1):
        bg_color = colors.lightgreen if row[2] == "activado" else colors.lightcoral
        tabla.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))

    # Crear una lista de elementos para el PDF
    elementos = []
    elementos.append(Paragraph("Resultados de Conectividad - ConnectionApp", styles['Title']))
    elementos.append(tabla)

    # Construir el PDF
    documento.build(elementos)

    print(f"PDF generado: {ruta_salida}")

    # Abrir el archivo PDF generado
    if platform.system() == "Windows":
        os.startfile(ruta_salida)
    elif platform.system() == "Darwin":
        subprocess.run(["open", ruta_salida])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", ruta_salida])
