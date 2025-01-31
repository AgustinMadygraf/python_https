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

    try:
        check.main()  # Verifica certificados SSL
        logger.info("✅ Verificación de certificados SSL completada sin errores.")
    except SystemExit as e:
        logger.error(f"❌ Error en la validación del certificado SSL: {e}")
        logger.warning("⚠️ Continuando la ejecución a pesar del fallo en la verificación del certificado.")
        # Aquí, en lugar de 'sys.exit(1)', simplemente no hacemos nada
        # y permitimos que el servidor siga.
    except Exception as ex:
        logger.critical(f"🔥 Error inesperado en la verificación SSL: {ex}", exc_info=True)
        # Decide si deseas terminar o continuar:
        # sys.exit(1)  # o lo dejas comentado si prefieres que no se cierre.

    logger.info("⚙️ Creando aplicación Flask.")
    app = create_app()

    # Obtener configuración SSL
    SSL_CERT = os.getenv("SSL_CERT")
    SSL_KEY = os.getenv("SSL_KEY")

    if not SSL_CERT or not SSL_KEY:
        logger.critical("❌ No se encontraron los certificados SSL. El servidor no se iniciará.")
        # sys.exit(1) # De nuevo, podrías detener o no, según la lógica de tu negocio.
        return

    logger.info(f"🔐 Certificado SSL: {SSL_CERT}")
    logger.info(f"🔑 Clave SSL: {SSL_KEY}")

    try:
        logger.info("🚀 Iniciando servidor Flask con SSL...")
        app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT, SSL_KEY))
    except Exception as ex:
        logger.critical(f"🔥 Error inesperado al iniciar el servidor Flask: {ex}", exc_info=True)
        # sys.exit(1) # O continuar según tus necesidades
