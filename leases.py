import tkinter as tk
from tkinter import ttk, messagebox
import paramiko

class MikroTikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clientes DHCP de MikroTik")

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

        self.connect_button = tk.Button(self.root, text="Conectar y Mostrar Clientes", command=self.connect_and_show)
        self.connect_button.pack(padx=10, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("IP", "MAC", "Host", "LeaseTime"), show='headings')
        self.tree.heading("IP", text="IP")
        self.tree.heading("MAC", text="MAC")
        self.tree.heading("Host", text="Host")
        self.tree.heading("LeaseTime", text="Lease Time")
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
            
            # Ejecutar el comando para obtener las leases DHCP
            command = '/ip dhcp-server lease print detail'
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
            leases = self.parse_leases(output)
            
            # Limpiar datos existentes en el TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insertar datos en el TreeView
            for lease in leases:
                self.tree.insert("", tk.END, values=(lease.get("IP", ""),
                                                     lease.get("MAC", ""),
                                                     lease.get("Host", ""),
                                                     lease.get("LeaseTime", "")))
            
            ssh.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al router MikroTik.\n{e}")

    def parse_leases(self, output):
        leases = []
        lease = {}
        for line in output.splitlines():
            if line.startswith(" "):  # Línea de detalles
                if 'address=' in line:
                    lease['IP'] = line.split("address=")[-1].split()[0].strip()
                elif 'mac-address=' in line:
                    lease['MAC'] = line.split("mac-address=")[-1].split()[0].strip()
                elif 'host-name=' in line:
                    lease['Host'] = line.split("host-name=")[-1].split()[0].strip('"')
                elif 'expires-after=' in line:
                    lease['LeaseTime'] = line.split("expires-after=")[-1].split()[0].strip()
            elif line.strip() == "":  # Fin del registro
                if lease:
                    leases.append(lease)
                    lease = {}
        
        # Añadir el último lease si existe
        if lease:
            leases.append(lease)
        
        return leases

def mostrar_leases():
    # Crear y ejecutar la aplicación
    root = tk.Tk()
    app = MikroTikApp(root)
    root.mainloop()

