import tkinter as tk
import requests
import RPi.GPIO as GPIO

# ===============================
# CONFIGURACION
# ===============================
API_URL = "http://187.33.146.109/partido/actualizar"

puntos_a = 0
puntos_b = 0

# Pines GPIO (numeracion BCM)
PIN_SUMA_A   = 17   # Pulsador sumar  equipo A
PIN_SUMA_B   = 27   # Pulsador sumar  equipo B
PIN_RESTA_A  = 22   # Pulsador borrar equipo A
PIN_RESTA_B  = 23   # Pulsador borrar equipo B

# ===============================
# CONFIGURACION GPIO
# ===============================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Todos los pines como entrada con resistencia pull-up interna
# El pulsador conecta el pin a GND cuando se pulsa
GPIO.setup(PIN_SUMA_A,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SUMA_B,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_RESTA_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_RESTA_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ===============================
# FUNCION PARA ENVIAR AL SERVIDOR
# ===============================
def enviar_datos():
    try:
        datos = {
            "equipo_a": puntos_a,
            "equipo_b": puntos_b
        }
        r = requests.post(API_URL, json=datos, timeout=2)
        print("Enviado:", datos, "Respuesta:", r.status_code)
    except Exception as e:
        print("Error conexión:", e)

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
def suma_a():
    global puntos_a
    puntos_a += 1
    actualizar_interfaz()

def resta_a():
    global puntos_a
    if puntos_a > 0:
        puntos_a -= 1
    actualizar_interfaz()

def suma_b():
    global puntos_b
    puntos_b += 1
    actualizar_interfaz()

def resta_b():
    global puntos_b
    if puntos_b > 0:
        puntos_b -= 1
    actualizar_interfaz()

# ===============================
# CALLBACKS GPIO (pulsadores fisicos)
# Los callbacks de GPIO se ejecutan en un hilo distinto al de Tkinter,
# por eso usamos ventana.after(0, ...) para llamar a las funciones
# de forma segura desde el hilo principal de la interfaz
# ===============================
def cb_suma_a(canal):
    ventana.after(0, suma_a)

def cb_suma_b(canal):
    ventana.after(0, suma_b)

def cb_resta_a(canal):
    ventana.after(0, resta_a)

def cb_resta_b(canal):
    ventana.after(0, resta_b)

# Asociamos cada pin a su callback
# bouncetime=300 evita que un solo pulso se detecte varias veces (efecto rebote)
GPIO.add_event_detect(PIN_SUMA_A,  GPIO.FALLING, callback=cb_suma_a,  bouncetime=300)
GPIO.add_event_detect(PIN_SUMA_B,  GPIO.FALLING, callback=cb_suma_b,  bouncetime=300)
GPIO.add_event_detect(PIN_RESTA_A, GPIO.FALLING, callback=cb_resta_a, bouncetime=300)
GPIO.add_event_detect(PIN_RESTA_B, GPIO.FALLING, callback=cb_resta_b, bouncetime=300)

# ===============================
# INTERFAZ GRAFICA
# ===============================
ventana = tk.Tk()
ventana.title("MARCADOR PÁDEL")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

titulo = tk.Label(ventana, text="MARCADOR PÁDEL",
                  font=("Arial", 20, "bold"),
                  bg="#1e1e1e",
                  fg="white")
titulo.pack(pady=10)

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

# Botones virtuales (siguen funcionando en pantalla)
botones = tk.Frame(ventana, bg="#1e1e1e")
botones.pack(pady=20)

tk.Button(botones, text="+ A", command=suma_a, width=10).grid(row=0, column=0, padx=10)
tk.Button(botones, text="- A", command=resta_a, width=10).grid(row=0, column=1, padx=10)
tk.Button(botones, text="+ B", command=suma_b, width=10).grid(row=0, column=2, padx=10)
tk.Button(botones, text="- B", command=resta_b, width=10).grid(row=0, column=3, padx=10)

# ===============================
# CERRAR LIMPIANDO GPIO
# ===============================
def cerrar():
    GPIO.cleanup()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar)

ventana.mainloop()
