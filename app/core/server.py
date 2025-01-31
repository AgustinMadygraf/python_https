"""
Path: app/core/server.py
Este archivo configura el servidor Flask y ejecuta la verificación de certificados SSL antes de iniciarlo.
"""

import os
import sys
from app.core.app_factory import create_app
from app.config import check
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar logger
logger = LoggerConfigurator().configure()

def start_server():
    """Inicia el servidor Flask con SSL."""
    logger.info("🔄 Iniciando servidor Flask con verificación de certificados SSL.")

    # Ejecutar validación de certificados antes de levantar el servidor
    try:
        check.main()  # Verifica certificados SSL
        logger.info("✅ Verificación de certificados SSL completada sin errores.")
    except SystemExit as e:
        logger.error(f"❌ Error en la validación del certificado SSL: {e}")
        sys.exit(1)
    except Exception as ex:
        logger.critical(f"🔥 Error inesperado en la verificación SSL: {ex}", exc_info=True)
        sys.exit(1)

    logger.info("⚙️ Creando aplicación Flask.")
    app = create_app()

    # Obtener configuración SSL
    SSL_CERT = os.getenv("SSL_CERT")
    SSL_KEY = os.getenv("SSL_KEY")

    if not SSL_CERT or not SSL_KEY:
        logger.critical("❌ No se encontraron los certificados SSL. El servidor no se iniciará.")
        sys.exit(1)

    logger.info(f"🔐 Certificado SSL: {SSL_CERT}")
    logger.info(f"🔑 Clave SSL: {SSL_KEY}")

    try:
        logger.info("🚀 Iniciando servidor Flask con SSL...")
        app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT, SSL_KEY))
    except Exception as ex:
        logger.critical(f"🔥 Error inesperado al iniciar el servidor Flask: {ex}", exc_info=True)
        sys.exit(1)
