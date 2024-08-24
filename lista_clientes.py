import paramiko
import re
import tkinter as tk
from tkinter import ttk

# Configuración de conexión SSH
hostname = '122.122.126.1'  # IP del router MikroTik
username = 'admin'         # Usuario de MikroTik
password = '070523'      # Contraseña del usuario

def get_simple_queue_list(hostname, username, password):
    # Crear un cliente SSH
    client = paramiko.SSHClient()
    # Agregar automáticamente el host a la lista de hosts conocidos
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conectar al router MikroTik
        client.connect(hostname, username=username, password=password)
        
        # Ejecutar el comando para listar las colas simples
        stdin, stdout, stderr = client.exec_command('/queue simple print')
        
        # Leer la salida del comando
        output = stdout.read().decode('utf-8')
        
        # Procesar la salida para extraer los datos relevantes
        client_info = []
        queue_entries = output.split("\n\n")  # Dividir en bloques por cliente
        
        for entry in queue_entries:
            name_match = re.search(r'name="([^"]+)"', entry)
            target_match = re.search(r'target=([^\s]+)', entry)
            max_limit_match = re.search(r'max-limit=([^\s]+)', entry)
            
            if name_match and target_match and max_limit_match:
                name = name_match.group(1)
                target = target_match.group(1)
                max_limit = max_limit_match.group(1)
                client_info.append((name, target, max_limit))
        
        return client_info
        
    finally:
        # Cerrar la conexión SSH
        client.close()

def update_table():
    # Limpiar la tabla
    for row in tree.get_children():
        tree.delete(row)
    
    # Obtener la lista de clientes desde el MikroTik
    client_list = get_simple_queue_list(hostname, username, password)
    
    # Insertar los datos en la tabla
    for client in client_list:
        tree.insert("", tk.END, values=client)

# Crear la ventana principal
window = tk.Tk()
window.title("Lista de Clientes en Simple Queue")

# Crear el Treeview (tabla)
columns = ("Nombre", "Target", "Max Limit")
tree = ttk.Treeview(window, columns=columns, show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("Target", text="Target")
tree.heading("Max Limit", text="Max Limit")

# Ajustar el tamaño de las columnas
tree.column("Nombre", width=200)
tree.column("Target", width=150)
tree.column("Max Limit", width=100)

tree.pack(padx=10, pady=10)

# Crear un botón para actualizar la tabla
update_button = tk.Button(window, text="Actualizar Lista", command=update_table)
update_button.pack(pady=10)

# Ejecutar el ciclo principal de la aplicación
window.mainloop()
