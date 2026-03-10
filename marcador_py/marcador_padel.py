import tkinter as tk
import requests
import RPi.GPIO as GPIO

# ===============================
# CONFIGURACION
# ===============================
API_URL = "http://187.33.146.109/partido/actualizar"

# Pines GPIO (numeracion BCM)
PIN_SUMA_A   = 17   # Pulsador sumar  equipo A
PIN_SUMA_B   = 23   # Pulsador sumar  equipo B
PIN_RESTA_A  = 6    # Pulsador borrar equipo A  <- corregido
PIN_RESTA_B  = 25    # Pulsador borrar equipo B  <- corregido

# ===============================
# LOGICA DE PUNTUACION PADEL
# Los puntos van: 0 -> 15 -> 30 -> 40 -> juego
# Con deuce (40-40) y ventaja
# ===============================
SECUENCIA = [0, 15, 30, 40]

# Indice del punto actual de cada equipo (0=0pts, 1=15pts, 2=30pts, 3=40pts)
idx_a = 0
idx_b = 0

def siguiente_punto(idx_atacante, idx_defensor):
    """
    Calcula el nuevo estado tras ganar un punto.
    Devuelve (nuevo_idx_atacante, nuevo_idx_defensor, hubo_juego)
    """
    nuevo = idx_atacante + 1

    # Caso normal sin deuce posible
    if nuevo <= 3 and idx_defensor <= 2:
        return nuevo, idx_defensor, False

    # Llega a 40 y el otro no tiene 40 -> gana el juego
    if nuevo >= 4 and idx_defensor < 3:
        return 0, 0, True

    # Deuce: ambos en 40, el atacante sube a ventaja (indice 4)
    if nuevo == 4 and idx_defensor == 3:
        return 4, 3, False

    # Tenia ventaja y gana el punto -> gana el juego
    if idx_atacante == 4:
        return 0, 0, True

    # El defensor tenia ventaja, el atacante recupera -> vuelve a deuce
    if idx_defensor == 4:
        return 3, 3, False

    return nuevo, idx_defensor, False

def idx_a_texto(idx):
    """Convierte el indice interno a texto legible en pantalla."""
    if idx == 4:
        return "AD"
    return str(SECUENCIA[idx])

# ===============================
# CONFIGURACION GPIO
# ===============================
GPIO.cleanup()           # Limpia configuracion previa
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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
            "equipo_a": idx_a_texto(idx_a),
            "equipo_b": idx_a_texto(idx_b)
        }
        r = requests.post(API_URL, json=datos, timeout=2)
        print("Enviado:", datos, "Respuesta:", r.status_code)
    except Exception as e:
        print("Error conexion:", e)

# ===============================
# ACTUALIZAR INTERFAZ
# ===============================
def actualizar_interfaz():
    label_a.config(text=idx_a_texto(idx_a))
    label_b.config(text=idx_a_texto(idx_b))
    enviar_datos()

# ===============================
# FUNCIONES BOTONES
# ===============================
def suma_a():
    global idx_a, idx_b
     nuevo_a, nuevo_b, juego = siguiente_punto(idx_a, idx_b)
    idx_a = nuevo_a
    idx_b = nuevo_b
    if juego:
        print("Juego para A!")
    actualizar_interfaz()

def resta_a():
    global idx_a
    if idx_a > 0:
        idx_a -= 1
    actualizar_interfaz()

def suma_b():
    global idx_a, idx_b
    nuevo_b, nuevo_a, juego = siguiente_punto(idx_b, idx_a)
    idx_a = nuevo_a
    idx_b = nuevo_b
    if juego:
        print("Juego para B!")
    actualizar_interfaz()

def resta_b():
    global idx_b
    if idx_b > 0:
        idx_b -= 1
    actualizar_interfaz()

# ===============================
# CALLBACKS GPIO
# Los callbacks se ejecutan en un hilo distinto al de Tkinter,
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

# bouncetime=300 evita que un solo pulso se detecte varias veces
GPIO.add_event_detect(PIN_SUMA_A,  GPIO.FALLING, callback=cb_suma_a,  bouncetime=300)
GPIO.add_event_detect(PIN_SUMA_B,  GPIO.FALLING, callback=cb_suma_b,  bouncetime=300)
GPIO.add_event_detect(PIN_RESTA_A, GPIO.FALLING, callback=cb_resta_a, bouncetime=300)
GPIO.add_event_detect(PIN_RESTA_B, GPIO.FALLING, callback=cb_resta_b, bouncetime=300)

# ===============================
# INTERFAZ GRAFICA
# ===============================
ventana = tk.Tk()
ventana.title("MARCADOR PADEL")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

titulo = tk.Label(ventana, text="MARCADOR PADEL",
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
