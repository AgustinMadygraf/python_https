"""
Path: server.py
Este archivo es el punto de entrada del servidor Flask. Aquí se configura el logger y se inicia el servidor con verificación de certificados SSL.
"""

import os
import sys
import logging
from app import create_app
from app.utils.logging.logger_configurator import LoggerConfigurator

# Configurar logger
logger = LoggerConfigurator().configure()

logger.info("🔄 Iniciando servidor Flask con verificación de certificados SSL.")

# Importar y ejecutar check.py antes de levantar el servidor
try:
    import check
    logger.info("🔍 Ejecutando la verificación de certificados SSL.")
    check.main()  # Llama a la función de verificación de certificados
    logger.info("✅ Verificación de certificados SSL completada sin errores.")
except SystemExit as e:
    logger.error(f"❌ Error en la validación del certificado SSL: {e}")
    sys.exit(1)
except Exception as ex:
    logger.critical(f"🔥 Error inesperado en la verificación SSL: {ex}", exc_info=True)
    sys.exit(1)

if __name__ == "__main__":
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
