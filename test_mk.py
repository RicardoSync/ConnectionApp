import paramiko
import time
import json
from tkinter import messagebox

def leer_credenciales():
    with open('credenciales.json', 'r') as archivo:
        datos = json.load(archivo)
        return datos


def test_conexion_mikrotik(hostname, port, username, password):
    # Crear un cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto aceptar claves de host

    try:
        # Conectar al MikroTik usando las credenciales proporcionadas
        client.connect(hostname=hostname, port=port, username=username, password=password)
        print(f"Conexión exitosa a {hostname}")

        # Realizar una simple operación para verificar la conexión
        stdin, stdout, stderr = client.exec_command("/system identity print")
        time.sleep(1)
        output = stdout.read().decode('utf-8')
        print("Resultado del comando:", output)

    except paramiko.AuthenticationException:
        print("Error de autenticación, verifique el nombre de usuario o contraseña.")
    except paramiko.SSHException as sshException:
        print(f"Error de conexión SSH: {sshException}")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        client.close()


def inicar_prueba():
    credenciales = leer_credenciales()
    hostname = credenciales['ip']
    username = credenciales['usuario']
    password = credenciales['password']

    port = 22                  # Puerto SSH (por defecto 22)

    # Llamar a la función de test de conexión
    test_conexion_mikrotik(hostname, port, username, password)
    messagebox.showinfo("Exito", "La prueba de conexion es exitosa para: " + hostname)