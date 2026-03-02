from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ----------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "padeluser",
    "password": "PadelSeguro123",
    "database": "padel"
}

# ----------------------------
# RUTA RAÍZ PARA TEST
# ----------------------------
@app.route("/")
def home():
    return "API Marcador Pádel funcionando correctamente"

# ----------------------------
# ACTUALIZAR MARCADOR
# ----------------------------
@app.route("/partido/actualizar", methods=["POST"])
def actualizar():
    data = request.get_json()

    # Verificar que se recibió JSON
    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    # Verificar que están los campos obligatorios
    if "equipo_a" not in data or "equipo_b" not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    equipo_a = data["equipo_a"]
    equipo_b = data["equipo_b"]

    conexion = None
    try:
        # Conectar a la base de datos y actualizar el marcador
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE marcador SET equipo_a=%s, equipo_b=%s WHERE id=1",
            (equipo_a, equipo_b)
        )
        conexion.commit()
        return jsonify({"mensaje": "Marcador actualizado correctamente"})

    except Error as e:
        # Devolver el error de base de datos
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar conexión siempre al finalizar
        if conexion is not None and conexion.is_connected():
            cursor.close()
            conexion.close()

# ----------------------------
# CONSULTAR ESTADO
# ----------------------------
@app.route("/partido/estado", methods=["GET"])
def estado():
    conexion = None
    try:
        # Conectar a la base de datos y obtener el marcador actual
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute("SELECT equipo_a, equipo_b FROM marcador WHERE id=1")
        resultado = cursor.fetchone()

        # Devolver el marcador si existe
        if resultado:
            return jsonify({
                "equipo_a": resultado[0],
                "equipo_b": resultado[1]
            })
        else:
            return jsonify({"error": "No se encontró el marcador"}), 404

    except Error as e:
        # Devolver el error de base de datos
        return jsonify({"error": str(e)}), 500

    finally:
        # Cerrar conexión siempre al finalizar
        if conexion is not None and conexion.is_connected():
            cursor.close()
            conexion.close()