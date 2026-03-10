import tkinter as tk
import requests

# ===============================
# CONFIGURACION
# ===============================
API_URL = "http://187.33.146.109/partido/actualizar"

SECUENCIA = [0, 15, 30, 40]

idx_a = 0
idx_b = 0

def siguiente_punto(idx_atacante, idx_defensor):
    nuevo = idx_atacante + 1
    if nuevo <= 3 and idx_defensor <= 2:
        return nuevo, idx_defensor, False
    if nuevo >= 4 and idx_defensor < 3:
        return 0, 0, True
    if nuevo == 4 and idx_defensor == 3:
        return 4, 3, False
    if idx_atacante == 4:
        return 0, 0, True
    if idx_defensor == 4:
        return 3, 3, False
    return nuevo, idx_defensor, False

def idx_a_texto(idx):
    if idx == 4:
        return "AD"
    return str(SECUENCIA[idx])

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

def actualizar_interfaz():
    label_a.config(text=idx_a_texto(idx_a))
    label_b.config(text=idx_a_texto(idx_b))
    enviar_datos()

def suma_a():
    global idx_a, idx_b
    idx_a, idx_b, juego = siguiente_punto(idx_a, idx_b)
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
    idx_b, idx_a, juego = siguiente_punto(idx_b, idx_a)
    if juego:
        print("Juego para B!")
    actualizar_interfaz()

def resta_b():
    global idx_b
    if idx_b > 0:
        idx_b -= 1
    actualizar_interfaz()

# ===============================
# INTERFAZ GRAFICA
# ===============================
ventana = tk.Tk()
ventana.title("MARCADOR PADEL")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

tk.Label(ventana, text="MARCADOR PADEL",
         font=("Arial", 20, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=10)

frame = tk.Frame(ventana, bg="#1e1e1e")
frame.pack(pady=20)

label_a = tk.Label(frame, text="0",
                   font=("Arial", 60, "bold"),
                   fg="#00ffcc", bg="#1e1e1e", width=4)
label_a.grid(row=0, column=0, padx=60)

label_b = tk.Label(frame, text="0",
                   font=("Arial", 60, "bold"),
                   fg="#ff4d4d", bg="#1e1e1e", width=4)
label_b.grid(row=0, column=1, padx=60)

botones = tk.Frame(ventana, bg="#1e1e1e")
botones.pack(pady=20)

tk.Button(botones, text="+ A", command=suma_a,  width=10, height=2,
          font=("Arial", 12, "bold"), bg="#007755", fg="white", cursor="hand2").grid(row=0, column=0, padx=10)
tk.Button(botones, text="- A", command=resta_a, width=10, height=2,
          font=("Arial", 12, "bold"), bg="#555555", fg="white", cursor="hand2").grid(row=0, column=1, padx=10)
tk.Button(botones, text="+ B", command=suma_b,  width=10, height=2,
          font=("Arial", 12, "bold"), bg="#992222", fg="white", cursor="hand2").grid(row=0, column=2, padx=10)
tk.Button(botones, text="- B", command=resta_b, width=10, height=2,
          font=("Arial", 12, "bold"), bg="#555555", fg="white", cursor="hand2").grid(row=0, column=3, padx=10)

def cerrar():
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar)
ventana.mainloop()
