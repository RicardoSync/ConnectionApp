import sqlite3
import datetime
import paramiko
from tkinter import messagebox
import json 
import os
from vista_credenciales_microtik import vista_credenciales
from tkinter import messagebox

def leer_credenciales():
    with open('credenciales.json', 'r') as archivo:
        datos = json.load(archivo)
        return datos

def gestionar_pagos_y_bloqueos():
    # Obtener el día actual
    dia_actual = datetime.datetime.now().strftime('%d')

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()

    # Obtener los clientes cuyo día de corte coincide con el día actual
    cursor.execute('SELECT nombre, ip FROM clientes WHERE diaCorte = ?', (dia_actual,))
    clientes_a_bloquear = cursor.fetchall()

    # Datos para conexión SSH
    credenciales = leer_credenciales()
    hostname = credenciales['ip']
    username = credenciales['usuario']
    password = credenciales['password']

    new_speed = '1K/1K'  # Ancho de banda bloqueado

    # Función para bloquear cliente
    def bloquear_cliente(hostname, username, password, client_ip, new_speed):
        port = 22  # Puerto SSH, generalmente es 22
        command = f'/queue simple set [find target="{client_ip}/32"] max-limit={new_speed}'

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname, port, username, password)
            stdin, stdout, stderr = client.exec_command(command)
            
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if output:
                messagebox.showerror("Error", f"Output: {output}")
            if errors:
                messagebox.showerror("Error", f"Errors: {errors}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client.close()

    # Bloquear a los clientes que deben ser bloqueados
    for cliente in clientes_a_bloquear:
        nombre, ip = cliente
        bloquear_cliente(hostname, username, password, ip, new_speed)

        # Actualizar el estado del cliente a "suspendido"
        cursor.execute('UPDATE clientes SET estado = ? WHERE nombre = ?', ('suspendido', nombre))
        conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

def bloqueo_por_dias():
    messagebox.showinfo("Precaucion", "Esto hara que el sistema obtenga el dia actual de su maquina, y bloquear a todos los clientes que tengan el mismo dia de corte y el de su maquina")
    # Nombre del archivo que deseas verificar
    archivo = "credenciales.json"
    
    # Verificar si el archivo existe en el directorio actual
    if os.path.exists(archivo):
        # Si el archivo existe, llama a la función ventana_buscar_cliente_pagar
        gestionar_pagos_y_bloqueos()
    else:
        # Si el archivo no existe, imprime un mensaje al usuario
        messagebox.showerror("Advertencia", f"No ha definido ninguna credencial para Microtik, definelo primero")
        vista_credenciales()
