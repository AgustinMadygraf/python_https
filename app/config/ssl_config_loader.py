
# app/config/ssl_config_loader.py

import os
from dotenv import load_dotenv
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class SSLConfigLoader:
    """
    Clase responsable de cargar la configuración SSL desde
    variables de entorno.
    """
    def __init__(self, env_file: str = '.env'):
        load_dotenv(env_file)
        self.ssl_cert = os.getenv("SSL_CERT")
        self.ssl_key = os.getenv("SSL_KEY")
        self.expected_hostname = os.getenv("EXPECTED_HOSTNAME", "madygraf.local")

    def validate(self) -> None:
        """
        Verifica que se hayan especificado las variables de entorno 
        y que los archivos existan.
        """
        if not self.ssl_cert or not self.ssl_key:
            msg = "Faltan variables de entorno: SSL_CERT o SSL_KEY."
            logger.error(f"❌ {msg}")
            raise SystemExit(f"Error: {msg}")

        if not os.path.isfile(self.ssl_cert):
            msg = f"No se encontró el archivo de certificado en '{self.ssl_cert}'."
            logger.error(f"❌ {msg}")
            raise SystemExit(f"Error: {msg}")

        if not os.path.isfile(self.ssl_key):
            msg = f"No se encontró la clave privada en '{self.ssl_key}'."
            logger.error(f"❌ {msg}")
            raise SystemExit(f"Error: {msg}")

        logger.info("✅ Configuración SSL validada correctamente.")
