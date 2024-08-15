import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping a IP")

        self.pinging = False
        self.ping_thread = None
        self.ping_data = []

        # Crear y colocar widgets
        tk.Label(root, text="Ingrese la IP:").pack(padx=10, pady=5)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack(padx=10, pady=5)

        self.ping_button = tk.Button(root, text="Iniciar Ping", command=self.start_ping)
        self.ping_button.pack(padx=10, pady=5)

        self.stop_button = tk.Button(root, text="Detener", command=self.stop_ping, state=tk.DISABLED)
        self.stop_button.pack(padx=10, pady=5)

        self.update_button = tk.Button(root, text="Actualizar Gráfica", command=self.update_graph, state=tk.DISABLED)
        self.update_button.pack(padx=10, pady=5)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=60)
        self.output_text.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.figure = plt.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.update_graph()

    def ping_ip(self, ip):
        # Determinar el comando de ping según el sistema operativo
        if platform.system() == "Windows":
            command = ["ping", ip]
        else:  # Asumir que es Linux
            command = ["ping", "-c", "4", ip]

        self.ping_data = []
        self.pinging = True

        try:
            # Ejecutar el comando ping
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(process.stdout.readline, ''):
                if not self.pinging:
                    process.terminate()
                    break
                self.output_text.insert(tk.END, line)
                self.output_text.yview(tk.END)

                # Analizar tiempos de respuesta
                if platform.system() == "Windows":
                    if "time=" in line:
                        time_str = line.split("time=")[-1].split("ms")[0]
                        self.ping_data.append(float(time_str))
                else:
                    if "time=" in line:
                        time_str = line.split("time=")[-1].split(" ")[0]
                        self.ping_data.append(float(time_str))

            self.update_graph()

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

        finally:
            self.pinging = False
            self.stop_button.config(state=tk.DISABLED)
            self.ping_button.config(state=tk.NORMAL)
            self.update_button.config(state=tk.NORMAL)

    def start_ping(self):
        ip = self.ip_entry.get()
        if not ip:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una IP.")
            return

        self.output_text.delete(1.0, tk.END)  # Limpiar el área de texto
        self.pinging = True
        self.ping_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.DISABLED)
        self.ping_thread = threading.Thread(target=self.ping_ip, args=(ip,), daemon=True)
        self.ping_thread.start()

    def stop_ping(self):
        self.pinging = False

    def update_graph(self):
        self.ax.clear()
        if not self.ping_data:
            self.ax.set_title("No se recibieron datos de ping")
        else:
            self.ax.plot(self.ping_data, marker='o', linestyle='-', color='b')
            ip = self.ip_entry.get()
            self.ax.set_title(f"Estadísticas de Ping para {ip}")
            self.ax.set_xlabel("Número de paquete")
            self.ax.set_ylabel("Tiempo de respuesta (ms)")
            self.ax.grid(True)

        self.canvas.draw()

def iniciar_tarea():
    # Crear y ejecutar la aplicación
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()
