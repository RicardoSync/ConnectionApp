import paramiko
from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import json
import os
from vista_credenciales_microtik import vista_credenciales
import sqlite3

def leer_credenciales():
        with open('credenciales.json', 'r') as archivo:
            datos = json.load(archivo)
            return datos

def actualizar_estado_cliente(cliente_id, nuevo_estado):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("network_software.db")
    cursor = conn.cursor()
    
    try:
        # Actualizar la columna 'estado' para el cliente con el id dado
        cursor.execute('''
            UPDATE clientes
            SET estado = ?
            WHERE id = ?
        ''', (nuevo_estado, cliente_id))
        
        # Confirmar los cambios
        conn.commit()
        
        # Comprobar si se actualizó alguna fila
        if cursor.rowcount > 0:
            print(f"El estado del cliente con ID {cliente_id} ha sido actualizado a '{nuevo_estado}'.")
        else:
            print(f"No se encontró un cliente con ID {cliente_id}.")
    
    except sqlite3.Error as e:
        print(f"Error al actualizar el estado del cliente: {e}")
    
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()


def bloquear_cliente(id_cliente, hostname, username, password, client_ip, new_speed):
        port = 22  # Puerto SSH, generalmente es 22

        # Comando para ajustar el ancho de banda
        command = f'/queue simple set [find target="{client_ip}/32"] max-limit={new_speed}'

        # Crear una instancia del cliente SSH
        client = paramiko.SSHClient()

        # Agregar automáticamente la clave del servidor si no está en la lista de known hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Conectarse al dispositivo
            client.connect(hostname, port, username, password)
            
            # Ejecutar el comando para ajustar el ancho de banda
            stdin, stdout, stderr = client.exec_command(command)
            
            # Leer y mostrar la salida del comando, si es necesario
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if output:
                messagebox.showerror("Error", f"Output: {output}")
            if errors:
                messagebox.showerror("Error", f"Errors: {errors}")

            messagebox.showinfo("Cambio exitoso", "Cliente bloqueado de manera exitosa")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Cerrar la conexión
            client.close()
            actualizar_estado_cliente(id_cliente, "bloqueado")

def desbloquear_cliente(id_cliente, hostname, username, password, client_ip, new_speed):
        port = 22  # Puerto SSH, generalmente es 22

        # Comando para ajustar el ancho de banda
        command = f'/queue simple set [find target="{client_ip}/32"] max-limit={new_speed}'

        # Crear una instancia del cliente SSH
        client = paramiko.SSHClient()

        # Agregar automáticamente la clave del servidor si no está en la lista de known hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Conectarse al dispositivo
            client.connect(hostname, port, username, password)
            
            # Ejecutar el comando para ajustar el ancho de banda
            stdin, stdout, stderr = client.exec_command(command)
            
            # Leer y mostrar la salida del comando, si es necesario
            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            if output:
                messagebox.showerror("Error", f"Output: {output}")
            if errors:
                messagebox.showerror("Error", f"Errors: {errors}")

            messagebox.showinfo("Cambio exitoso", f"La velocidad del cliente {client_ip} ha sido cambiada a {new_speed}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Cerrar la conexión
            client.close()
            actualizar_estado_cliente(id_cliente, "activado")
      

def buscar_cliente_por_id(id_cliente):
    cliente_id = id_cliente
    if not cliente_id:
        messagebox.showerror("Error", "Por favor, ingresa un ID de cliente.")
        return

    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, direccion, telefono, equipos, ip, velocidad, fechaInstalacion, proximoPago, mensualidad, estado, api FROM clientes WHERE id=?', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()

    if cliente:
        nombre_entry.delete(0, END)
        nombre_entry.insert(0, cliente[0])
        ip_entry.delete(0, END)
        ip_entry.insert(0, cliente[4])
        velocidad_entry.delete(0, END)
        velocidad_entry.insert(0, cliente[5])


    else:
        messagebox.showinfo("Información", "Cliente no encontrado.")

def vista_bloqueo_desbloque():
    def obtener_datos():
        id_cliente = id_entry.get()
        buscar_cliente_por_id(id_cliente)

    def obtener_datos_bloque():            
        credenciales = leer_credenciales()
        hostname = credenciales['ip']
        username = credenciales['usuario']
        password = credenciales['password']
        client_ip = ip_entry.get()
        id_cliente = id_entry.get()
        new_speed = "1k/1k"
        bloquear_cliente(id_cliente, hostname, username, password, client_ip, new_speed)
        
    def obtener_datos_desbloque():
        credenciales = leer_credenciales()
        hostname = credenciales['ip']
        username = credenciales['usuario']
        password = credenciales['password']
        client_ip = ip_entry.get()
        new_speed = velocidad_entry.get()
        id_cliente = id_entry.get()
        desbloquear_cliente(id_cliente, hostname, username, password, client_ip, new_speed)



    def comprobar_archivo_y_llamar_funcion_bloqueo():
        # Nombre del archivo que deseas verificar
        archivo = "credenciales.json"
        
        # Verificar si el archivo existe en el directorio actual
        if os.path.exists(archivo):
            # Si el archivo existe, llama a la función ventana_buscar_cliente_pagar
            obtener_datos_bloque()
        else:
            # Si el archivo no existe, imprime un mensaje al usuario
            messagebox.showerror("Advertencia", f"No se ha definido las credenciales para acceder a Microtik")
            vista_credenciales()
           

    def comprobar_archivo_y_llamar_funcion_desbloqueo():
        # Nombre del archivo que deseas verificar
        archivo = "credenciales.json"
        
        # Verificar si el archivo existe en el directorio actual
        if os.path.exists(archivo):
            # Si el archivo existe, llama a la función ventana_buscar_cliente_pagar
            obtener_datos_desbloque()
        else:
            # Si el archivo no existe, imprime un mensaje al usuario
            messagebox.showerror("Advertencia", f"No se ha definido las credenciales para acceder a Microtik")
            vista_credenciales()
           

            

    vista_cambio_velocidad = tk.Tk()
    vista_cambio_velocidad.title("Bloqueo / Desbloqueo")
    vista_cambio_velocidad.geometry("750x250")
    vista_cambio_velocidad.resizable(False, False)

    
    global id_entry, nombre_entry, ip_entry, velocidad_entry

    tamano = 20

    id_label = tk.Label(vista_cambio_velocidad, text="Id del Cliente")
    id_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    buscar_button = tk.Button(vista_cambio_velocidad, text="Buscar", width=20, command=obtener_datos)

    nombre_label = tk.Label(vista_cambio_velocidad, text="Nombre Cliente")
    nombre_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    ip_label = tk.Label(vista_cambio_velocidad, text="Ip Cliente")
    ip_entry = tk.Entry(vista_cambio_velocidad, width=tamano)

    velocidad_label = tk.Label(vista_cambio_velocidad, text="Plan Actual")
    velocidad_entry = tk.Entry(vista_cambio_velocidad, width=tamano)



    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    buscar_button.grid(row=0, column=2, padx=10, pady=10)

    nombre_label.grid(row=2, column=0, padx=10, pady=10)
    nombre_entry.grid(row=2, column=1, padx=10, pady=10)

    ip_label.grid(row=2, column=2, padx=10, pady=10)
    ip_entry.grid(row=2, column=3, padx=10, pady=10)    

    velocidad_label.grid(row=3, column=0, padx=10, pady=10)
    velocidad_entry.grid(row=3, column=1, padx=10, pady=10)



    # Añadir un separador horizontal
    separador = ttk.Separator(vista_cambio_velocidad, orient='horizontal')
    separador.grid(row=1, column=0, columnspan=5, sticky='ew', padx=10, pady=10)


    # Crear un Frame para agrupar los botones
    frame_botones = tk.Frame(vista_cambio_velocidad)
    frame_botones.grid(column=0, row=7, columnspan=4, padx=10, pady=10)

    # Botón Guardar
    guardar = tk.Button(frame_botones, text="Bloquear", width=25, command=comprobar_archivo_y_llamar_funcion_bloqueo)
    guardar.pack(side=tk.LEFT, padx=5)

    bloquear = tk.Button(frame_botones, text="Desbloquear", width=25, command=comprobar_archivo_y_llamar_funcion_desbloqueo)
    bloquear.pack(side=tk.LEFT, padx=5)

    # Botón Cancelar
    cancela = tk.Button(frame_botones, text="Cancelar", width=25, command=vista_cambio_velocidad.destroy)
    cancela.pack(side=tk.LEFT, padx=5)

    vista_cambio_velocidad.mainloop()
