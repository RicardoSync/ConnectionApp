import os
import platform
import subprocess
from pathlib import Path
from tkinter import Tk, Button

def abrir_gestor_archivos(directorio):
    # Verificar si el directorio existe
    if not directorio.exists():
        print(f"El directorio {directorio} no existe.")
        return
    
    # Abrir el gestor de archivos dependiendo del sistema operativo
    sistema_operativo = platform.system()
    
    try:
        if sistema_operativo == "Windows":
            subprocess.run(["explorer", str(directorio)])
        elif sistema_operativo == "Linux":
            subprocess.run(["xdg-open", str(directorio)])
        elif sistema_operativo == "Darwin":  # Darwin es el nombre del sistema operativo de macOS
            subprocess.run(["open", str(directorio)])
        else:
            print(f"El sistema operativo {sistema_operativo} no es compatible.")
    except Exception as e:
        print(f"No se pudo abrir el gestor de archivos: {e}")

# Obtener el directorio del script principal
directorio_principal = Path(__file__).parent

# Ruta al directorio 'icons'
directorio_icons = directorio_principal / 'icons'

# Crear una aplicación simple con Tkinter
def llamar_gestor_logo():
    abrir_gestor_archivos(directorio_icons)
