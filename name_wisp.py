import json
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


def nombre_wisp():


    def guardar_datos():
        # Crear un diccionario con los datos
        datos = {
                "nombre": nombre_wisp_input,
                "mensaje": mensaje,
                "direccion" : direccion,
                "telefono" : telefono,
                "email" : email
 
            }

                # Guardar el diccionario en un archivo JSON
        with open("nombre_wisp.json", "w") as file:
                json.dump(datos, file, indent=4)
                messagebox.showinfo("Correcto", "Informacion guardada de manera correcta") 
    
    nombre_wisp_input = simpledialog.askstring("Nombre Wisp", "Ingresa el nombre de wisp, es el que aparecera en tus recibos")
    mensaje = simpledialog.askstring("Mensaje Wisp", "Ingresa el mensaje que quieras que se muestre a tus clientes")
    direccion = simpledialog.askstring("Direccion Empresa ","Ingresa la direccion de tu WISP")
    telefono = simpledialog.askstring("Telefono Contacto","Ingresa el numero de telefono, para tu contacto ")
    email = simpledialog.askstring("Correo Electronico","Ingresa tu direccion de correo electronico")
   
    if nombre_wisp_input:
         guardar_datos()