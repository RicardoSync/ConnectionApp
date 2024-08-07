import tkinter as tk
from plyer import notification

def mostrar_notificacion(titulo, mensaje):

    notification.notify(
        title=titulo,
        message=mensaje,
        app_name='ConnectionApp',
        timeout=10
    )

