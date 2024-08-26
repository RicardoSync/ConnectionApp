import json
import os
from datetime import datetime, timedelta

def obtener_fecha_del_sistema():
    return datetime.now()

def sumar_dias(fecha, dias):
    return fecha + timedelta(days=dias)

def crear_archivo_json(fecha, nombre_archivo):
    datos = {'fecha': fecha.strftime('%Y-%m-%d')}
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo)

def leer_archivo_json(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
            return datetime.strptime(datos['fecha'], '%Y-%m-%d')
    return None

def eliminar_archivo_json(nombre_archivo):
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)

def main():
    nombre_archivo = 'config.json'

    # Obtener la fecha del sistema
    fecha_sistema = obtener_fecha_del_sistema()

    # Leer el archivo JSON y obtener la fecha guardada
    fecha_guardada = leer_archivo_json(nombre_archivo)

    # Comparar las fechas
    if fecha_guardada is not None:
        if fecha_sistema.date() == fecha_guardada.date():
            eliminar_archivo_json(nombre_archivo)
            print("Las fechas coinciden. El archivo JSON ha sido eliminado.")
        else:
            print("Las fechas no coinciden.")
    else:
        # Si el archivo no existe, crear uno nuevo con la fecha actual + 7 días
        fecha_nueva = sumar_dias(fecha_sistema, 7)
        crear_archivo_json(fecha_nueva, nombre_archivo)
        print("Archivo JSON creado con la fecha nueva.")

if __name__ == '__main__':
    main()
