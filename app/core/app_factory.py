"""
Path: app/core/app_factory.py
Este archivo contiene la función create_app() para inicializar y configurar la aplicación Flask.
"""

from flask import Flask
from flask_cors import CORS
from app.config_main import load_and_validate_config
from app.routes.main import main_bp
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar logger
logger = LoggerConfigurator().configure()

def create_app():
    " Crea una instancia de la aplicación Flask y la configura "
    logger.info("🛠 Creando instancia de Flask...")

    try:
        # Cargar configuración y validaciones iniciales
        logger.info("🔍 Cargando y validando configuración de la aplicación.")
        load_and_validate_config()
    except Exception as e:
        logger.critical(f"❌ Error en la configuración de la aplicación: {e}", exc_info=True)
        raise

    # Crear la aplicación Flask
    app = Flask(__name__)
    logger.info("✅ Aplicación Flask creada correctamente.")

    # Configurar CORS
    logger.info("🌐 Configurando CORS para la aplicación.")
    CORS(app, resources={r"/*": {"origins": ["https://madygraf.com", "http://localhost:8081"], "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

    # Registrar blueprints
    logger.info("🔗 Registrando blueprints en la aplicación.")
    app.register_blueprint(main_bp)

    logger.info("🚀 Aplicación Flask lista para ejecutarse.")
    return app
