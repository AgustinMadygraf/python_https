"""
Path: app/config.py

"""

import os
from dotenv import load_dotenv

def load_and_validate_config():
    load_dotenv()
    
    # Verificamos variables de entorno requeridas
    required_vars = ["STATIC_FOLDER", "SSL_CERT", "SSL_KEY"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"La variable de entorno {var} no está definida o está vacía.")
    
    # Podríamos verificar aquí también que los archivos de certificados existan
    ssl_cert = os.getenv("SSL_CERT")
    ssl_key = os.getenv("SSL_KEY")
    if not (os.path.isfile(ssl_cert) and os.path.isfile(ssl_key)):
        raise FileNotFoundError("No se encontraron los archivos de certificado o llave privada.")
    
    # Si se necesita una verificación más profunda del certificado,
    # podríamos integrar librerías adicionales en un archivo de utilidades.
