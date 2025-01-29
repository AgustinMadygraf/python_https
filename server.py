"""
Path: server.py

"""

import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Obtener valores desde las variables de entorno
STATIC_FOLDER = os.getenv("STATIC_FOLDER")
SSL_CERT = os.getenv("SSL_CERT")
SSL_KEY = os.getenv("SSL_KEY")

app = Flask(__name__, static_folder=STATIC_FOLDER)

@app.route("/")
def home():
    return "¡Servidor Flask corriendo en HTTPS en el puerto 443!"

# Servir el index.html
@app.route("/estatuto/dist/")
def estatuto():
    return send_from_directory(STATIC_FOLDER, "index.html")

# Servir archivos estáticos (CSS, JS, imágenes, etc.)
@app.route("/estatuto/dist/<path:filename>")
def estatuto_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT, SSL_KEY))
