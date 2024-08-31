import tkinter as tk
from tkinter import ttk, messagebox
import paramiko

class MikroTikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colas de MikroTik")

        self.create_widgets()

    def create_widgets(self):
        # Configuración de la ventana principal
        tk.Label(self.root, text="IP del Router MikroTik:").pack(padx=10, pady=5)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack(padx=10, pady=5)

        tk.Label(self.root, text="Usuario:").pack(padx=10, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(padx=10, pady=5)

        tk.Label(self.root, text="Contraseña:").pack(padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack(padx=10, pady=5)

        self.connect_button = tk.Button(self.root, text="Conectar y Mostrar Colas", command=self.connect_and_show)
        self.connect_button.pack(padx=10, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Target", "Max Limit", "Burst Limit", "Burst Threshold", "Priority"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Target", text="Target")
        self.tree.heading("Max Limit", text="Max Limit")
        self.tree.heading("Burst Limit", text="Burst Limit")
        self.tree.heading("Burst Threshold", text="Burst Threshold")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def connect_and_show(self):
        ip = self.ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Crear la conexión SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            
            # Ejecutar el comando para obtener las colas
            command = '/queue simple print detail'
            stdin, stdout, stderr = ssh.exec_command(command)

            # Leer la salida del comando
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if error:
                messagebox.showerror("Error", f"Error en el comando SSH:\n{error}")
                ssh.close()
                return

            # Mostrar salida en la consola para depuración
            print("Salida del comando SSH:\n", output)

            # Procesar la salida
            queues = self.parse_queues(output)
            
            # Mostrar los datos procesados en la consola para depuración
            print("Datos procesados:\n", queues)
            
            # Limpiar datos existentes en el TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos en el TreeView
            for queue in queues:
                self.tree.insert("", tk.END, values=(queue.get("Name", ""),
                                                     queue.get("Target", ""),
                                                     queue.get("Max Limit", ""),
                                                     queue.get("Burst Limit", ""),
                                                     queue.get("Burst Threshold", ""),
                                                     queue.get("Priority", "")))
            
            ssh.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al router MikroTik.\n{e}")

    def parse_queues(self, output):
        queues = []
        lines = output.splitlines()
        queue = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("Flags:"):
                continue  # Ignorar la línea de flags
            
            if line.startswith(" "):  # Línea que contiene datos de cola
                if 'name=' in line:
                    queue['Name'] = line.split("name=")[-1].split()[0].strip().strip('"')
                elif 'target=' in line:
                    queue['Target'] = line.split("target=")[-1].split()[0].strip()
                elif 'max-limit=' in line:
                    queue['Max Limit'] = line.split("max-limit=")[-1].split()[0].strip()
                elif 'burst-limit=' in line:
                    queue['Burst Limit'] = line.split("burst-limit=")[-1].split()[0].strip()
                elif 'burst-threshold=' in line:
                    queue['Burst Threshold'] = line.split("burst-threshold=")[-1].split()[0].strip()
                elif 'priority=' in line:
                    queue['Priority'] = line.split("priority=")[-1].split()[0].strip()
            elif line == "":  # Fin del registro de una cola
                if queue:
                    queues.append(queue)
                    queue = {}  # Resetear el diccionario para la siguiente cola
        
        # Añadir la última cola si existe
        if queue:
            queues.append(queue)
        
        return queues

# Crear y ejecutar la aplicación
root = tk.Tk()
app = MikroTikApp(root)
root.mainloop()
