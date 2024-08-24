import os
import json
from PIL import Image, ImageTk
from db import crear_base_datos
from tkinter import Menu, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox
from tkinter import ttk
from vista_cliente_registro import ventana_principal_registro
from mostrar_tabla_clientes import mostrar_datos_cliente
from editar_buscar_eliminar import ventana_buscar_actualizar
import webbrowser
from registrar_pago_vista import ventana_buscar_cliente_pagar
from ver_pagos_tabla import mostrar_datos
from vista_credenciales_microtik import vista_credenciales
from cambio_de_velocidad import ventana_cambio_velocidad
from bloqueos_desbloqueo import vista_bloqueo_desbloque
from bloqueo_automatico import comprobar_funcion_gestion_bloqueos
import tkinter as tk
import sqlite3
from name_wisp import nombre_wisp
from reiniciar_antena import reiniciar
from definir_mensaje_automatico import definir_mensaje_automatico
from enviar_mensaje_automatoco_vs import iniciar_envio_masivo_automatico
from enviar_mensaje_personal import vista_mensaje_personal
from enviar_mensaje_automatoco_vs import comprobacion_de_mensaje_definido
from ping import iniciar_tarea
from leases import mostrar_leases
from test_ancho_de_banda import crear_interfaz
import platform
from carpeta_recibos  import crear_ventana
from pathlib import Path
from cambiar_logo import llamar_gestor_logo
from usuarios import usuarios_ventana
from test_mk import inicar_prueba
from test_internet import inicio_de_test

valid_keys = ['MoCawN07gMSYraorEKCD', 'bdNfUCMwvCJ2D8vIjmnD',
              '6IWqROUMkBhgpolTubDx', 'SMDle3q7ATJmiHRRusKC',
              'F3aI5xrnvgtCQOi6I6Dt', 'm97OMRuiMKFSgNtuD5oS',
              'wG5UIpYxJ6Yf9VDJQ1W8', 'wf9aCgU6ZpmSLE0jxs31',
              'vf43vpHjIF3bISDsLYfk', 'G7DXHkn0juR9szeJwLMu',
              'fnE8yMMvTk9Y7nFvCuSx', '13ay7n9Y6D2G21n59ckP',
              '2vVnKKLtuC4c7ki4t892', 'MZdDYuWf4XzQj3NOu68c',
              'pNGVJO2fgZW5nTg3RszP', '4CqhhUr3d3JBJaWn5r4I',
              'ZgvQM5CnPNAXnqrHXKT5', 'IGvdGSD64Db3JiC26SLG',
              '6LMNE5QbfH4lfe66Pwxm', 'PbJUFtjXnyCrX7TfL6U9',
              '8wEDSsjfvpLrC5JbMVjI', 'nSaxXvFvm3msR56i9Nap',
              'w4FLio0IzCLLa294Fz2N', 'wuFroaApHIJxokwmCovg',
              'sXJclRY0R7EkskzCAAf8', 'aabQVGZoqyGIsfWmoGn2',
              'sqNOoTXxdunv6QMrFRBP', 'wIsdAvldpLmYYRUi1VQg',
              '6ZeK6OIKYV4m5t2FsNa2', 'IeYbXNW8WaxDL0MKCNqh',
              'sJzCWOkeYclZBUK9ITmC', '5swZV1fPgmEouO5t7V64',
              'XLoWYZd72eB2w9Rspp2N', 'YiyBXsH7yAarGuLzLEVO',
              'wn3eUK6YVmXXbRx7bOjb', '7SLdj8W1ZJBnmTZvCHCa',
              '5dIYniXC8g8AwcyPg9zf', 'MYrOQYFmbEWo5TOIorcH',
              'wR07I9JAi1ruGYyqio86', 'jhLngVsE4FV3tXL2O1xa', 
              'jcmAep1p9rKeDRvumzgg', 'f8MeZ5U3ocSZKqr3EnWW', 'pE6EwajppQBDOw2FMFXx',
              '1weXJfMXu9eP5k6hOCRK', 'REhcKynyqTEPpvDJ2WmK', 'TeMFBwFZUmPBp8BDakA9',
              'AnDFPA1EMeTZPeSBzEye', 'IPg2cJay7yg50dqgbBid', 'LzpLqvGWYxh13xNKCuRs', 
              'IgQbzXIaHuyyK7Bzpwgc', 'CETvnFrjDBLM5cVHqPsc', 'gNm3CsfJedf1lJX0O7RA',
              'OdCekutvDUHk1tPPRur6', 'ndl6cAHifBPFi2Tb3iIE', 'JZC8SJcZ5AAWDw94WHPz',
              'R8i3lxw96g2XxHo8BUFH', 'fVyER7yShOjPWRz7orLT', 'qlgQ45HI8lg1BpRBDPVS',
              '8OyGEInn5V1au34WKosp', 'MKMQSuMxpmCvCivecgVA', 'NSF5Ufk4k5gw0N0LV2nw',
              'F9R0pF1cYLXLLp2gosCj', 'ib3sDpDZBdlJZLudW3Cz', 'X1NADCurmOxYWrtHHe6g',
              'hle9HpvPD0J3M2H6sXPP', 'luDCUhF5JUzi3JO6Jnlm', 'ukPAs2jhtcxJUYmuNEpf',
              'iEOJIaXHtYVllb6YkOzO', 'NPvrT6M4oS9VLdSPOXF9', 'pvdPuxZPeH4HYKafY4Rx',
              'oJ7Emwt0eFhUPr8wEcVi', 'F4hKv2xhVBMbhf5EiLLO', '7ssv6J25oQDZI76gBIQw', 'hLNTibmJRnBY86fXmPEZ',
              'JetOaZ1NPYiNrmIr30iM', 'AHfGTRLvDs6RUIhXvoet', 'hdH1V4Hcjs1fPNvyhBL1', '5j6AHhITmrgMfmoCUk21',
              '6Wg0JkQTSi1KvMOmKbcN', 'K9lbVFTB9SoExdhW2DRE', '34PY0a4kV1EO3ng3v71B', 'FbTPOQWfNOw5bnhFUKCj',
              'tMkgP9dAcRCVwINKwF9F', 'M3iVvCaogcfutds29OxT', 'PRhrrS9yrhkHRouCL9AC', 'M9x0d0WAomvsU3WfQKvA',
              'N2ej7ppfZ2kPEd6KCwXR', 'eZSPKP5lUAH6jxmM1vmM', 'uRKN56Tns1DFmFK7sSMk', 'Hjnh8yE49mc25BUHIn3Z',
              'jWhCk4txVtSbVfCkI0Gb', 'KSWahDoXPnuuS3wnhVfa', 'hVldClO3uuOyWyrlYq7A', 'kjsoraWeugnYjOWMDnPk',
              'DOeZE1o9nKohawCWRPRH', 'aPTkTjLHulrcHOu6rCPI', 'FMmXL7wY9DipYwFkhnxN', 'BN9jSFkN0F01A3FKDBt9',
              'pBQ9WzhmeufpaOvx0GmR', 'TIW5euZVcm6ToLTWGbW9', 'MinuzaFea265/', 'demo']

url = "https://www.facebook.com/profile.php?id=100065750894627"


crear_base_datos()

def verify_activation_key(input_key):
    return input_key in valid_keys

def check_activation():
    user_key = activation_key.get()
    if verify_activation_key(user_key):
        messagebox.showinfo("Activacion", "Activacion satisfactoria!")
        store_activation_key(user_key)
        activation_window.destroy()
        create_main_window()
    else:
        messagebox.showerror("Activation", "Invalid activation key. Please try again.")

def store_activation_key(key):
    config = {'activation_key': key}
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file)

def load_activation_key():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config.get('activation_key')
    return None


def crear_usuario(username, password):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def verificar_usuario(username, password):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None



# Lista de velocidades
velocidades = ["100M/10M", "100M15M", "100M/20M", "100M/25M", "100M/30M", "100M/50M",
               "100M/60M", "100M/70M", "100M/80M", "100M/90M", "100M/100M",
               "200M/200M", "250M/250M", "300M/300M", "Seleccion Libre"]

# Función para leer usuarios
def leer_usuarios(nombre="", direccion="", telefono=""):
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    query = 'SELECT id, nombre, direccion, telefono, api, ip, estado, proximoPago FROM clientes WHERE 1=1'
    
    params = []
    if nombre:
        query += ' AND nombre LIKE ?'
        params.append(f'%{nombre}%')
    if direccion:
        query += ' AND direccion LIKE ?'
        params.append(f'%{direccion}%')
    if telefono:
        query += ' AND telefono LIKE ?'
        params.append(f'%{telefono}%')
    
    cursor.execute(query, params)
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Función para cargar usuarios en la tabla
def cargar_usuarios():
    for item in tree.get_children():
        tree.delete(item)
    usuarios = leer_usuarios()
    for usuario in usuarios:
        estado = usuario[6].lower()
        tree.insert("", tk.END, values=usuario, tags=(estado,))
# Función para actualizar la tabla
def actualizar_tabla():
    # Limpia la tabla
    for row in tree.get_children():
        tree.delete(row)
    # Vuelve a cargar los datos
    cargar_usuarios()

# Función para mostrar el menú contextual
def mostrar_menu_contextual(event):
    try:
        menu_contextual.tk_popup(event.x_root, event.y_root)
    finally:
        menu_contextual.grab_release()

# Función para crear la ventana principal
def create_main_window():



    # Nombre del archivo que deseas verificar
    archivo = "credenciales.json"
    
    # Verificar si el archivo existe en el directorio actual
    if os.path.exists(archivo):
        # Si el archivo existe, llama a la función ventana_buscar_cliente_pagar
        pass
    else:
        # Si el archivo no existe, imprime un mensaje al usuario
        messagebox.showerror("Advertencia", f"Antes de inciar debe ingresar las credenciales de Microtik para las funciones especiales")
        vista_credenciales()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("ConnectionApp")
    root.geometry("1200x600")

    # Detectar el sistema operativo
    if platform.system() == "Windows":
        # Establecer el ícono de la aplicación en Windows
        icon_path = "icons/icono.ico"  # Reemplaza con la ruta de tu archivo .ico
        root.iconbitmap(icon_path)
    elif platform.system() == "Linux":
        # Establecer el ícono de la aplicación en Linux usando un archivo .png
        icon_path = "icons/logo.png"  # Reemplaza con la ruta de tu archivo .png
        img = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, img)
    # Crear la barra de menú
    menu_bar = Menu(root)


    # Crear el menú Cliente
    cliente_menu = Menu(menu_bar, tearoff=0)
    cliente_menu.add_command(label="Crear Cliente", command=crear_cliente)
    cliente_menu.add_command(label="Ver Cliente", command=ver_cliente)
    cliente_menu.add_command(label="Buscar Cliente", command=buscar_cliente)
    menu_bar.add_cascade(label="Cliente", menu=cliente_menu)

    # Crear el menú Pagos
    pagos_menu = Menu(menu_bar, tearoff=0)
    pagos_menu.add_command(label="Nombre de wisp", command=nombre_wisp)
    pagos_menu.add_command(label="Registrar Pago", command=comprobar_archivo_y_llamar_funcion)
    pagos_menu.add_command(label="Ver Pagos", command=ver_pagos)
    pagos_menu.add_command(label="Carpeta Pagos", command=crear_ventana)
    menu_bar.add_cascade(label="Pagos", menu=pagos_menu)

    # Crear el menú Herramientas de red
    herramientas_red_menu = Menu(menu_bar, tearoff=0)
    herramientas_red_menu.add_command(label="Enviar Ping", command=iniciar_tarea)
    herramientas_red_menu.add_command(label="Iniciar Fast", command=crear_interfaz)
    herramientas_red_menu.add_command(label="Credenciales Microtik", command=credenciales_microtik)
    herramientas_red_menu.add_command(label="Cambio Velocidad", command=ventana_cambio_velocidad)
    herramientas_red_menu.add_command(label="Desbloquear/Bloquear Cliente", command=desbloquear_cliente)
    herramientas_red_menu.add_command(label="Cortes Automáticos", command=cortes_automaticos)
    herramientas_red_menu.add_command(label="Mostrar Clientes Leases", command=mostrar_leases)
    herramientas_red_menu.add_command(label="Reiniciar antena", command=reiniciar)
    menu_bar.add_cascade(label="Herramientas de red", menu=herramientas_red_menu)
    


    # Crear el menú Herramientas de red
    opciones_bot = Menu(menu_bar, tearoff=0)
    opciones_bot.add_command(label="Definir mensaje automatico", command=definir_mensaje_automatico)
    opciones_bot.add_command(label="Enviar mensaje automatico", command=comprobacion_de_mensaje_definido)
    opciones_bot.add_command(label="Enviar mensaje personalizado", command=vista_mensaje_personal)
    menu_bar.add_cascade(label="BotWhatsApp", menu=opciones_bot)

    # Crear opción de creación de base
    creacion_base = Menu(menu_bar, tearoff=0)
    creacion_base.add_command(label="?", command=version)
    creacion_base.add_command(label="Contacto", command=acerca_de)
    creacion_base.add_command(label="Salir", command=root.destroy)
    menu_bar.add_cascade(label="Información", menu=creacion_base)


    configuracion = Menu(menu_bar, tearoff=0)
    configuracion.add_command(label="Cambiar logo recibo", command=llamar_gestor_logo)
    configuracion.add_command(label="Cambiar usuario y clave", command=usuarios_ventana)
    configuracion.add_command(label="Prueba de Conexion Microtik", command=inicar_prueba)
    configuracion.add_command(label="Prueba de Conexion Internet", command=inicio_de_test)
    menu_bar.add_cascade(label="Configuracion", menu=configuracion)

    # Mostrar la barra de menú
    root.config(menu=menu_bar)

    # Crear un marco principal
    marco_principal = tk.Frame(root)
    marco_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Crear un marco para los botones a la izquierda
    marco_botones = tk.Frame(marco_principal)
    marco_botones.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Crear botones en el marco de botones
    botones = [
        ("Crear Cliente", crear_cliente),
        ("Ver Cliente", ver_cliente),
        ("Buscar Cliente", buscar_cliente),
        ("Registrar Pago", comprobar_archivo_y_llamar_funcion),
        ("Bloqueos", desbloquear_cliente)

    ]

    for i, (text, command) in enumerate(botones):
        row = i // 2  # Determina la fila (2 botones por fila)
        col = i % 2   # Determina la columna (0 o 1)
        boton = tk.Button(marco_botones, text=text, command=command, width=15)
        boton.grid(row=row, column=col, padx=5, pady=5)

    # Crear Treeview para mostrar datos
    global tree
    tree = ttk.Treeview(marco_principal, columns=("Id", "Nombre", "Direccion", "Telefono", "api", "IP", "Estado", "ProximoPago"), show="headings")
    
    # Definir las columnas
    tree.heading("Id", text="Id")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Direccion", text="Direccion")
    tree.heading("Telefono", text="Telefono")
    tree.heading("api", text="api")
    tree.heading("IP", text="IP")
    tree.heading("Estado", text="Estado")
    tree.heading("ProximoPago", text="Proximo Pago")
    
    # Definir el ancho de las columnas
    tree.column("Nombre", width=150)
    tree.column("Direccion", width=150)
    tree.column("Telefono", width=100)
    tree.column("api", width=100)
    tree.column("IP", width=100)
    tree.column("Estado", width=100)
    tree.column("ProximoPago", width=150)

    # Configurar las etiquetas de estilo
    tree.tag_configure("activado", background="lightgreen")
    tree.tag_configure("suspendido", background="lightcoral")
    tree.tag_configure("desactivado", background="lightgray")
    tree.tag_configure("bloqueado", background="lightyellow")
    
    # Colocar el Treeview en la ventana principal
    tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Crear el menú contextual
    global menu_contextual
    menu_contextual = Menu(root, tearoff=0)
    menu_contextual.add_command(label="Crear Cliente", command=ventana_principal_registro)
    menu_contextual.add_command(label="Actualizar", command=actualizar_tabla)
    menu_contextual.add_command(label="Salir", command=root.destroy)
    
    # Asociar el evento de clic derecho al Treeview
    tree.bind("<Button-3>", mostrar_menu_contextual)
    
    # Cargar usuarios en la tabla al iniciar
    cargar_usuarios()
    
    root.mainloop()

def crear_cliente():
    ventana_principal_registro()
    
def ver_cliente():
    mostrar_datos_cliente()

def buscar_cliente():
    ventana_buscar_actualizar()


def comprobar_archivo_y_llamar_funcion():
    # Nombre del archivo que deseas verificar
    archivo = "nombre_wisp.json"
    
    # Verificar si el archivo existe en el directorio actual
    if os.path.exists(archivo):
        # Si el archivo existe, llama a la función ventana_buscar_cliente_pagar
        ventana_buscar_cliente_pagar()
    else:
        # Si el archivo no existe, imprime un mensaje al usuario
        messagebox.showerror("Advertencia", f"No ha definido un nombre de WISP ni un mensaje. Por favor, definalos para poder crear sus recibos")
        nombre_wisp()



def ver_pagos():
    mostrar_datos()

def credenciales_microtik():
    vista_credenciales()

def bloquear_cliente():
    vista_bloqueo_desbloque()

def cortes_automaticos():
    comprobar_funcion_gestion_bloqueos()

        
def desbloquear_cliente():
    vista_bloqueo_desbloque()

def proximamente():
    messagebox.showinfo("Proximamente", "Aun encontramos trabajando con estas opciones. En la proxima version Connectio v1.0")

def acerca_de():
    webbrowser.open(url)

def version():
    messagebox.askyesno("Informacion", "Software Connection para wisp desarrollado por Ing Escobedo. Con la version 0.9")   
    
def crear_usuario_y_contrasena():
    def crear_usuario_func():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            crear_usuario(username, password)
            messagebox.showinfo("Usuario creado", "Usuario y contraseña creados exitosamente.")
            user_window.destroy()
            create_main_window()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de usuario y una contraseña.")
    
    # Crear ventana para ingresar usuario y contraseña
    user_window = Tk()
    user_window.title("Crear Usuario")
    user_window.geometry("300x250")
    user_window.resizable(False, False)
    Label(user_window, text="Nombre de usuario:").pack(pady=5)
    username_entry = Entry(user_window)
    username_entry.pack(pady=5)

    Label(user_window, text="Contraseña:").pack(pady=5)
    password_entry = Entry(user_window, show="*")
    password_entry.pack(pady=5)

    Button(user_window, text="Crear Usuario", command=crear_usuario_func).pack(pady=10)
    
    user_window.mainloop()

def iniciar_sesion():
    def verificar_sesion():
        username = username_entry.get()
        password = password_entry.get()
        if verificar_usuario(username, password):
            login_window.destroy()
            create_main_window()
        else:
            messagebox.showerror("Error de inicio de sesión", "Nombre de usuario o contraseña incorrectos.")
    
    login_window = Tk()
    login_window.title("Iniciar Sesión")
    login_window.geometry("300x250")
    login_window.resizable(False,False)
    Label(login_window, text="Nombre de usuario:").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    Label(login_window, text="Contraseña:").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    Button(login_window, text="Iniciar Sesión", command=verificar_sesion).pack(pady=10)
    
    login_window.mainloop()

# Verificar si ya hay una clave de activación almacenada
stored_key = load_activation_key()

if stored_key and verify_activation_key(stored_key):
    # Verificar si ya se creó un usuario
    conn = sqlite3.connect('network_software.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    user_count = cursor.fetchone()[0]
    conn.close()
    
    if user_count == 0:
        crear_usuario_y_contrasena()
    else:
        iniciar_sesion()
else:
    # Crear la ventana de activación
    activation_window = Tk()
    activation_window.title("Activación")
    activation_window.geometry("300x150")
    activation_window.resizable(False, False)

    activation_key = StringVar()

    Label(activation_window, text="Ingresa la llave de activación:").pack(pady=10)
    Entry(activation_window, textvariable=activation_key).pack(pady=5)
    Button(activation_window, text="Activar", command=check_activation).pack(pady=10)

    activation_window.mainloop()