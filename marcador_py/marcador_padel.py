import RPi.GPIO as GPIO
import tkinter as tk
import requests
import threading
import time

# ===============================
# CONFIGURACION
# ===============================

SUMA_A = 17
RESTA_A = 22
SUMA_B = 27
RESTA_B = 23

API_URL = "http://IP_DEL_SERVIDOR/partido/actualizar"

puntos_a = 0
puntos_b = 0

# ===============================
# FUNCION PARA ENVIAR AL SERVIDOR
# ===============================

def enviar_datos():
    try:
        datos = {
            "equipo_a": puntos_a,
            "equipo_b": puntos_b
        }
        requests.post(API_URL, json=datos, timeout=2)
    except:
        print("No se pudo conectar con el servidor")

# ===============================
# ACTUALIZAR INTERFAZ
# ===============================

def actualizar_interfaz():
    label_a.config(text=str(puntos_a))
    label_b.config(text=str(puntos_b))
    enviar_datos()

# ===============================
# FUNCIONES BOTONES
# ===============================

def suma_a(channel):
    global puntos_a
    puntos_a += 1
    actualizar_interfaz()

def resta_a(channel):
    global puntos_a
    if puntos_a > 0:
        puntos_a -= 1
    actualizar_interfaz()

def suma_b(channel):
    global puntos_b
    puntos_b += 1
    actualizar_interfaz()

def resta_b(channel):
    global puntos_b
    if puntos_b > 0:
        puntos_b -= 1
    actualizar_interfaz()

# ===============================
# CONFIGURACION GPIO
# ===============================

GPIO.setmode(GPIO.BCM)

GPIO.setup(SUMA_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RESTA_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SUMA_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RESTA_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(SUMA_A, GPIO.FALLING, callback=suma_a, bouncetime=300)
GPIO.add_event_detect(RESTA_A, GPIO.FALLING, callback=resta_a, bouncetime=300)
GPIO.add_event_detect(SUMA_B, GPIO.FALLING, callback=suma_b, bouncetime=300)
GPIO.add_event_detect(RESTA_B, GPIO.FALLING, callback=resta_b, bouncetime=300)

# ===============================
# INTERFAZ GRAFICA
# ===============================

ventana = tk.Tk()
ventana.title("Marcador de Pádel")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

titulo = tk.Label(ventana, text="MARCADOR DE PÁDEL", 
                  font=("Arial", 24, "bold"),
                  bg="#1e1e1e",
                  fg="white")
titulo.pack(pady=20)

frame = tk.Frame(ventana, bg="#1e1e1e")
frame.pack(pady=20)

label_a = tk.Label(frame, text="0",
                   font=("Arial", 60, "bold"),
                   fg="#00ffcc",
                   bg="#1e1e1e")
label_a.grid(row=0, column=0, padx=60)

label_b = tk.Label(frame, text="0",
                   font=("Arial", 60, "bold"),
                   fg="#ff4d4d",
                   bg="#1e1e1e")
label_b.grid(row=0, column=1, padx=60)

# ===============================
# CIERRE LIMPIO
# ===============================

def cerrar():
    GPIO.cleanup()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar)

ventana.mainloop()