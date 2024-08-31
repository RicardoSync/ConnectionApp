import paramiko
import sqlite3
from tkinter import messagebox
import json

def leer_credenciales():
    with open('credenciales.json', 'r') as archivo:
        datos = json.load(archivo)
        return datos

# Función para desbloquear cliente
def desbloquear_cliente(hostname, username, password, client_ip, original_speed):
    port = 22  # Puerto SSH, generalmente es 22
    command = f'/queue simple set [find target="{client_ip}/32"] max-limit={original_speed}'

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

def obtener_datos_cliente(id_cliente):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ip, velocidad FROM clientes WHERE id = ?', (id_cliente,))
    resultado = cursor.fetchone()

    conn.close()
    if resultado:
        client_ip, original_speed = resultado
        return client_ip, original_speed
    else:
        return None, None

def get_datos(id_cliente):    
    # Datos para conexión SSH
    credenciales = leer_credenciales()
    hostname = credenciales['ip']
    username = credenciales['usuario']
    password = credenciales['password']

    # Obtener datos del cliente desde la base de datos
    client_ip, original_speed = obtener_datos_cliente(id_cliente)

    if client_ip and original_speed:
        desbloquear_cliente(hostname, username, password, client_ip, original_speed)
    else:
        print(f"No se encontraron datos para el cliente con ID {id_cliente}")

