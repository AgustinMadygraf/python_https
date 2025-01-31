"""
Path: app/routes/main.py
"""

import os
import logging
from flask import Blueprint, send_from_directory, jsonify
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar logger
logger = LoggerConfigurator().configure()

# Definir blueprint
main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def home():
    logger.info("📢 Acceso a la ruta raíz '/'")
    return "¡Servidor Flask corriendo en HTTPS en el puerto 443!"

@main_bp.route("/estatuto/dist/")
@main_bp.route("/estatuto/")
def estatuto():
    static_folder = os.getenv("STATIC_FOLDER")
    if not static_folder:
        logger.error("❌ La variable STATIC_FOLDER no está definida en el entorno.")
        return jsonify({"error": "La configuración del servidor es incorrecta. Contacta al administrador."}), 500

    file_path = os.path.join(static_folder, "index.html")
    if not os.path.exists(file_path):
        logger.warning(f"⚠️ No se encontró el archivo index.html en {static_folder}.")
        return jsonify({"error": "El recurso solicitado no está disponible."}), 404

    logger.info(f"📂 Sirviendo 'index.html' desde {static_folder}")
    return send_from_directory(static_folder, "index.html")

@main_bp.route("/estatuto/dist/<path:filename>")
def estatuto_static(filename):
    static_folder = os.getenv("STATIC_FOLDER")
    if not static_folder:
        logger.error("❌ La variable STATIC_FOLDER no está definida en el entorno.")
        return jsonify({"error": "La configuración del servidor es incorrecta. Contacta al administrador."}), 500

    file_path = os.path.join(static_folder, filename)
    if not os.path.exists(file_path):
        logger.warning(f"⚠️ No se encontró el archivo {filename} en {static_folder}.")
        return jsonify({"error": "El recurso solicitado no está disponible."}), 404

    logger.info(f"📂 Sirviendo '{filename}' desde {static_folder}")
    return send_from_directory(static_folder, filename)
