import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame, LEFT, RIGHT, W, E

# Conectar a la base de datos SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla de usuarios si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)''')
conn.commit()

# Función para agregar un nuevo usuario
def agregar_usuario():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Campos vacíos", "Por favor, rellene todos los campos.")
        return
    
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Éxito", "Usuario agregado exitosamente.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El nombre de usuario ya existe.")

# Función para actualizar la contraseña de un usuario existente
def actualizar_password():
    username = entry_username.get()
    new_password = entry_password.get()
    
    if not username or not new_password:
        messagebox.showwarning("Campos vacíos", "Por favor, rellene todos los campos.")
        return
    
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")
    else:
        messagebox.showerror("Error", "El usuario no existe.")

# Crear la interfaz gráfica con Tkinter
def usuarios_ventana():
    ventana = Tk()
    ventana.title("Gestión de Usuarios")
    ventana.geometry("400x200")
    ventana.configure(bg="#f0f0f0")

    frame = Frame(ventana, bg="#f0f0f0")
    frame.pack(pady=20)

    global entry_username, entry_password
    
    Label(frame, text="Usuario:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=10, sticky=W)
    entry_username = Entry(frame, textvariable=StringVar(), font=("Arial", 12))
    entry_username.grid(row=0, column=1, pady=5, padx=10)

    Label(frame, text="Contraseña:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=10, sticky=W)
    entry_password = Entry(frame, textvariable=StringVar(), show='*', font=("Arial", 12))
    entry_password.grid(row=1, column=1, pady=5, padx=10)

    button_frame = Frame(ventana, bg="#f0f0f0")
    button_frame.pack(pady=20)

    Button(button_frame, text="Agregar Usuario", command=agregar_usuario, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=LEFT, padx=10)
    Button(button_frame, text="Actualizar Contraseña", command=actualizar_password, font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5).pack(side=RIGHT, padx=10)

    ventana.mainloop()

# Llamar a la función para crear la ventana

# Cerrar la conexión a la base de datos cuando se cierra la aplicación
conn.close()
