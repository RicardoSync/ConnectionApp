import tkinter as tk
from tkinter import messagebox, ttk
import speedtest
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

def medir_ancho_de_banda(progress_bar, status_label):
    try:
        status_label.config(text="Realizando prueba de velocidad. Por favor, espere...")
        progress_bar.start(10)  # Iniciar la barra de progreso

        st = speedtest.Speedtest()
        st.download()
        progress_bar['value'] = 50  # Actualizar la barra de progreso
        st.upload()
        progress_bar['value'] = 100  # Actualizar la barra de progreso
        resultados = st.results.dict()

        download_speed = resultados["download"] / 1_000_000  # Convertir a Mbps
        upload_speed = resultados["upload"] / 1_000_000  # Convertir a Mbps

        status_label.config(text="Prueba completada.")
        progress_bar.stop()  # Detener la barra de progreso

        # Mostrar los resultados en una gráfica
        mostrar_grafica(download_speed, upload_speed)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al medir el ancho de banda: {str(e)}")
        progress_bar.stop()
        status_label.config(text="Error en la prueba.")

def mostrar_grafica(download_speed, upload_speed):
    # Crear una nueva ventana para la gráfica
    grafica_ventana = tk.Toplevel()
    grafica_ventana.title("Resultados de Ancho de Banda")

    fig, ax = plt.subplots()
    
    # Gráfica de barras
    bars = ax.bar(["Download", "Upload"], [download_speed, upload_speed], color=["blue", "green"])
    ax.set_ylabel("Velocidad (Mbps)")
    ax.set_title("Velocidades de Descarga y Subida")

    # Agregar valores sobre las barras
    for bar, value in zip(bars, [download_speed, upload_speed]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 2, f"{value:.2f} Mbps", 
                ha='center', va='bottom', fontweight='bold', color='white')

    # Agregar la gráfica a la ventana de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=grafica_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

    grafica_ventana.mainloop()

def iniciar_medicion(progress_bar, status_label):
    # Crear un hilo para que la interfaz no se congele durante la medición
    hilo = threading.Thread(target=medir_ancho_de_banda, args=(progress_bar, status_label))
    hilo.start()

def crear_interfaz():
    root = tk.Tk()
    root.title("Medidor de Ancho de Banda")

    status_label = tk.Label(root, text="Presiona el botón para iniciar la prueba.")
    status_label.pack(pady=10)

    medir_btn = tk.Button(root, text="Medir Ancho de Banda", command=lambda: iniciar_medicion(progress_bar, status_label))
    medir_btn.pack(pady=20)

    # Barra de progreso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    root.mainloop()

