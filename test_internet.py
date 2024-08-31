import subprocess
import socket
import time
import requests
import tkinter as tk
from tkinter import scrolledtext

class NetworkTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Test Results")

        # Crear un área de texto con desplazamiento
        self.result_area = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
        self.result_area.pack(padx=10, pady=10)
        self.result_area.insert(tk.END, "Resultados de las pruebas:\n\n")

        # Botones para ejecutar las pruebas
        self.button_ping = tk.Button(root, text="Verificar Conexión (Ping)", command=self.verificar_conexion_ping)
        self.button_ping.pack(pady=5)

        self.button_dns = tk.Button(root, text="Verificar DNS", command=self.verificar_dns)
        self.button_dns.pack(pady=5)

        self.button_http = tk.Button(root, text="Verificar Conexión HTTP", command=self.verificar_conexion_http)
        self.button_http.pack(pady=5)

    def mostrar_resultado(self, texto):
        self.result_area.insert(tk.END, texto + "\n")
        self.result_area.yview(tk.END)  # Desplazar al final del área de texto

    def verificar_conexion_ping(self):
        """
        Verifica la conexión a internet mediante un ping a un servidor conocido.
        """
        self.mostrar_resultado("Verificando conexión mediante ping...")
        try:
            output = subprocess.check_output(["ping", "-c", "4", "8.8.8.8"], universal_newlines=True)
            self.mostrar_resultado(f"Conexión a 8.8.8.8 exitosa:\n{output}")
        except subprocess.CalledProcessError as e:
            self.mostrar_resultado(f"Error al hacer ping a 8.8.8.8:\n{e.output}")

    def verificar_dns(self):
        """
        Verifica la resolución de DNS para asegurarse de que el nombre de dominio puede resolverse.
        """
        self.mostrar_resultado("Verificando resolución DNS...")
        try:
            resolved_ip = socket.gethostbyname("www.google.com")
            self.mostrar_resultado(f"DNS resuelto para www.google.com: {resolved_ip}")
        except socket.error as err:
            self.mostrar_resultado(f"Error al resolver www.google.com: {err}")

    def verificar_conexion_http(self):
        """
        Verifica la conexión HTTP/HTTPS a un sitio web.
        """
        self.mostrar_resultado("Verificando conexión HTTP...")
        try:
            start_time = time.time()
            response = requests.get("https://www.google.com", timeout=5)
            latency = time.time() - start_time
            if response.status_code == 200:
                self.mostrar_resultado(f"Conexión exitosa a https://www.google.com con una latencia de {latency:.2f} segundos.")
            else:
                self.mostrar_resultado(f"Conexión fallida a https://www.google.com con código de estado {response.status_code}.")
        except requests.ConnectionError:
            self.mostrar_resultado("No se pudo conectar a https://www.google.com. Verifica tu conexión a internet.")
        except requests.Timeout:
            self.mostrar_resultado("Tiempo de espera agotado para la conexión a https://www.google.com.")

def inicio_de_test():
    root = tk.Tk()
    app = NetworkTestApp(root)
    root.mainloop()
