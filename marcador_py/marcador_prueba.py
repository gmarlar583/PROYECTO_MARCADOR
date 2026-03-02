import tkinter as tk
import requests

# ===============================
# CONFIGURACION
# ===============================

API_URL = "http://187.33.146.109/partido/actualizar"

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
# FUNCIONES BOTONES VIRTUALES
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
# INTERFAZ GRAFICA
# ===============================

ventana = tk.Tk()
ventana.title("SIMULADOR MARCADOR PÁDEL")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

titulo = tk.Label(ventana, text="SIMULADOR MARCADOR",
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

# Botones virtuales
botones = tk.Frame(ventana, bg="#1e1e1e")
botones.pack(pady=20)

tk.Button(botones, text="+ A", command=suma_a, width=10).grid(row=0, column=0, padx=10)
tk.Button(botones, text="- A", command=resta_a, width=10).grid(row=0, column=1, padx=10)
tk.Button(botones, text="+ B", command=suma_b, width=10).grid(row=0, column=2, padx=10)
tk.Button(botones, text="- B", command=resta_b, width=10).grid(row=0, column=3, padx=10)

ventana.mainloop()