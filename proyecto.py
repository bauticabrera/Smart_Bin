import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time

PUERTO = '/dev/ttyACM0'
BAUDIOS = 9600

try:
    arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
    time.sleep(2)  # Esperar reinicio de la placa
    print("Conexión serial establecida en", PUERTO)
except Exception as e:
    print(f"No se pudo abrir el puerto {PUERTO}: {e}")
    arduino = None


def enviar_comando(comando):
    """Envía cadenas de texto formateadas hacia el Arduino"""
    if arduino and arduino.is_open:
        try:
            mensaje = f"{comando}\n"
            arduino.write(mensaje.encode('utf-8'))
            print(f"Enviado a Arduino: {comando}")
        except Exception as e:
            print("Error al enviar comando:", e)
    else:
        print("Arduino no está conectado. Comando no enviado:", comando)

def abrir_tapa():
    enviar_comando("ABRIR")

def cerrar_tapa():
    enviar_comando("CERRAR")

def guardar_configuracion():
    dist = entry_dist.get().strip()
    limite = entry_limite.get().strip()
    
    if dist.isdigit() and limite.isdigit():
        enviar_comando(f"SET:{dist},{limite}")
        messagebox.showinfo("Configuración", "Nuevos parámetros enviados a la placa.")
    else:
        messagebox.showwarning("Error de Entrada", "Ingresá valores numéricos válidos.")


root = tk.Tk()
root.title("Smart Bin")
root.geometry("520x420")
root.resizable(False, False)

# Título Principal
lbl_titulo = tk.Label(root, text="Smart Bin", font=("Arial", 22, "bold"))
lbl_titulo.pack(pady=10)


frame_izq = tk.Frame(root)
frame_izq.pack(side="left", padx=20, pady=10, fill="both", expand=True)


lbl_llenado_txt = tk.Label(frame_izq, text="Nivel de llenado:", font=("Arial", 11, "bold"))
lbl_llenado_txt.pack(anchor="w")

frame_barra = tk.Frame(frame_izq)
frame_barra.pack(fill="x", pady=5)

bar_llenado = ttk.Progressbar(frame_barra, orient="horizontal", length=160, mode="determinate")
bar_llenado.pack(side="left", padx=5)

lbl_porcentaje = tk.Label(frame_barra, text="0%", font=("Arial", 11, "bold"))
lbl_porcentaje.pack(side="left")


lbl_estado_txt = tk.Label(frame_izq, text="Estado:", font=("Arial", 11, "bold"))
lbl_estado_txt.pack(anchor="w", pady=(15, 0))

lbl_estado_caja = tk.Label(frame_izq, text="Esperando datos...", relief="solid", bd=1, width=20, height=2, bg="white", font=("Arial", 10))
lbl_estado_caja.pack(anchor="w", pady=5)


lbl_led_txt = tk.Label(frame_izq, text="led RGB:", font=("Arial", 11, "bold"))
lbl_led_txt.pack(anchor="w", pady=(10, 0))

canvas_led = tk.Canvas(frame_izq, width=35, height=35, highlightthickness=0)
canvas_led.pack(anchor="w", pady=5)
circulo_led = canvas_led.create_oval(3, 3, 32, 32, fill="gray") 


frame_config = tk.LabelFrame(root, text="Configuracion", font=("Arial", 11, "bold"), padx=15, pady=15)
frame_config.pack(side="right", padx=20, pady=10, fill="y")

lbl_dist = tk.Label(frame_config, text="Distancia deteccion:")
lbl_dist.pack(anchor="w", pady=(5, 0))
entry_dist = tk.Entry(frame_config, width=15)
entry_dist.insert(0, "15") 
entry_dist.pack(pady=5)

lbl_limite = tk.Label(frame_config, text="Limite de llenado %:")
lbl_limite.pack(anchor="w", pady=(5, 0))
entry_limite = tk.Entry(frame_config, width=15)
entry_limite.insert(0, "80") 
entry_limite.pack(pady=5)

btn_guardar = tk.Button(frame_config, text="Guardar", width=10, command=guardar_configuracion)
btn_guardar.pack(pady=15)


frame_tapa = tk.LabelFrame(root, text="Control Tapa", font=("Arial", 11, "bold"), padx=15, pady=10)
frame_tapa.place(relx=0.5, rely=0.84, anchor="center")

btn_abrir = tk.Button(frame_tapa, text="Abrir", width=10, command=abrir_tapa)
btn_abrir.pack(side="left", padx=10)

btn_cerrar = tk.Button(frame_tapa, text="Cerrar", width=10, command=cerrar_tapa)
btn_cerrar.pack(side="left", padx=10)


def escuchar_arduino():
    """
    Espera tramas enviadas por Arduino con el formato:
    "PORCENTAJE,ESTADO,COLOR_LED" (Ej: "60,Nivel medio,yellow")
    """
    while True:
        if arduino and arduino.is_open:
            try:
                linea = arduino.readline().decode('utf-8').strip()
                if linea:
                    datos = linea.split(',')
                    if len(datos) == 3:
                        pct, estado, color_led = datos[0], datos[1], datos[2]

                        # Actualizar la interfaz Tkinter
                        bar_llenado['value'] = int(pct)
                        lbl_porcentaje.config(text=f"{pct}%")
                        lbl_estado_caja.config(text=estado)
                        canvas_led.itemconfig(circulo_led, fill=color_led)
            except Exception as e:
                print("Error de lectura serial:", e)
                break
        time.sleep(0.1)


if arduino:
    hilo = threading.Thread(target=escuchar_arduino, daemon=True)
    hilo.start()


root.mainloop()