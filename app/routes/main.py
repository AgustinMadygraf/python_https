"""
Path: app/routes/main.py

"""

from flask import Blueprint, send_from_directory
import os

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
def home():
    return "¡Servidor Flask corriendo en HTTPS en el puerto 443!"

@main_bp.route("/estatuto/dist/")
@main_bp.route("/estatuto/")
def estatuto():
    static_folder = os.getenv("STATIC_FOLDER")
    return send_from_directory(static_folder, "index.html")

@main_bp.route("/estatuto/dist/<path:filename>")
def estatuto_static(filename):
    static_folder = os.getenv("STATIC_FOLDER")
    return send_from_directory(static_folder, filename)
