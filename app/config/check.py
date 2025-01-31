"""
Path: check.py
"""

import os
import datetime
from dotenv import load_dotenv
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

def main():
    """
    Verifica el estado de los certificados SSL basados
    en las variables de entorno definidas en .env
    """
    
    logger.info("Iniciando verificación de certificados SSL.")
    
    # Cargar las variables de entorno
    load_dotenv()
    
    # Obtener las rutas de los certificados
    ssl_cert = os.getenv("SSL_CERT")
    ssl_key = os.getenv("SSL_KEY")
    
    # Verificación básica: comprobar si las variables están definidas
    if not ssl_cert:
        logger.error("La variable de entorno SSL_CERT no está definida.")
        raise SystemExit("Error: La variable de entorno SSL_CERT no está definida.")
    if not ssl_key:
        logger.error("La variable de entorno SSL_KEY no está definida.")
        raise SystemExit("Error: La variable de entorno SSL_KEY no está definida.")
    
    logger.debug(f"Certificado SSL: {ssl_cert}")
    logger.debug(f"Clave privada SSL: {ssl_key}")
    
    # Verificar si los archivos de certificado y llave existen
    if not os.path.isfile(ssl_cert):
        logger.error(f"No se encontró el archivo de certificado en la ruta '{ssl_cert}'.")
        raise SystemExit(f"Error: No se encontró el archivo de certificado en la ruta '{ssl_cert}'.")
    if not os.path.isfile(ssl_key):
        logger.error(f"No se encontró la llave privada en la ruta '{ssl_key}'.")
        raise SystemExit(f"Error: No se encontró la llave privada en la ruta '{ssl_key}'.")
    
    logger.info("Certificados encontrados. Procediendo con la verificación.")
    
    # Cargar y analizar el certificado
    try:
        with open(ssl_cert, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        logger.debug("Certificado cargado correctamente.")
    except Exception as e:
        logger.error(f"No se pudo leer el certificado. Detalles: {e}")
        raise SystemExit(f"Error: No se pudo leer el certificado. Detalles: {e}")
    
    # Verificar la fecha de expiración
    not_after = cert.not_valid_after_utc
    now = datetime.datetime.now(datetime.timezone.utc)  # Convertir a zona horaria UTC

    logger.info(f"📅 Fecha de expiración del certificado: {not_after}")

    if now > not_after:
        logger.error("El certificado ha expirado.")
        raise SystemExit("Error: El certificado ha expirado.")
    else:
        days_to_expire = (not_after - now).days
        if days_to_expire < 15:
            logger.warning(f"⚠️ Advertencia: El certificado expira en {days_to_expire} día(s).")
        else:
            logger.info(f"✅ El certificado es válido. Expira en {days_to_expire} día(s).")

    logger.info("✅ La verificación de los certificados finalizó sin errores.")
