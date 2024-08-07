import json
from tkinter import *
from tkinter import messagebox

def definir_mensaje_automatico():
    def guardar_datos():
        # Obtener el texto del widget Text
        mensaje = mensajeEntry.get("1.0", END).strip()

        # Crear un diccionario con los datos
        datos = {
            "mensaje": mensaje
        }

        # Guardar el diccionario en un archivo JSON
        with open("mensaje_automatico.json", "w") as file:
            json.dump(datos, file, indent=4)
            messagebox.showinfo("Mensaje Bot", "Mensaje guardado de manera correcta") 

    app = Tk()
    app.title("Mensaje Masivo")
    app.geometry("450x450")
    app.resizable(False, False)

    mensajeL = Label(app, text="Ingresa un mensaje pre-definido para todos tus clientes.")
    mensajeEntry = Text(app, width=50, height=20)
    guardar_datos_button = Button(app, text="Guardar Mensaje", width=20, command=guardar_datos)
    
    mensajeL.pack()
    mensajeEntry.pack()
    guardar_datos_button.pack()

    app.mainloop()
