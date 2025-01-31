"""
Path: app/config.py
Este archivo contiene la función load_and_validate_config, que carga las variables de entorno y verifica que las requeridas estén definidas.
"""

import os
import logging
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar logger
logger = LoggerConfigurator().configure()

def load_and_validate_config():
    """
    Carga las variables de entorno y verifica que las requeridas estén definidas.
    Devuelve True si la configuración es válida, False si hay errores.
    """
    logger.info("🔍 Cargando variables de entorno desde el archivo .env.")
    load_dotenv()
    
    # Verificamos variables de entorno requeridas
    required_vars = ["STATIC_FOLDER", "SSL_CERT", "SSL_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.critical(f"❌ Faltan variables de entorno: {', '.join(missing_vars)}")
        return False

    # Validamos que los archivos de certificado y llave privada existan
    ssl_cert = os.getenv("SSL_CERT")
    ssl_key = os.getenv("SSL_KEY")

    logger.debug(f"🔐 Ruta del certificado SSL: {ssl_cert}")
    logger.debug(f"🔑 Ruta de la clave privada SSL: {ssl_key}")

    if not (ssl_cert and ssl_key and os.path.isfile(ssl_cert) and os.path.isfile(ssl_key)):
        logger.critical("❌ No se encontraron los archivos de certificado o llave privada. Verifica las rutas.")
        return False

    logger.info("✅ Configuración de entorno validada correctamente.")
    return True
