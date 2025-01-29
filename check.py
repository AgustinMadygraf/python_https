# check.py

import os
import sys
import datetime
from dotenv import load_dotenv
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def main():
    """
    Verifica el estado de los certificados SSL basados
    en las variables de entorno definidas en .env
    """
    
    # Cargar las variables de entorno
    load_dotenv()
    
    # Obtener las rutas de los certificados
    ssl_cert = os.getenv("SSL_CERT")
    ssl_key = os.getenv("SSL_KEY")
    
    # Verificación básica: comprobar si las variables están definidas
    if not ssl_cert:
        print("Error: La variable de entorno SSL_CERT no está definida.")
        sys.exit(1)
    if not ssl_key:
        print("Error: La variable de entorno SSL_KEY no está definida.")
        sys.exit(1)
    
    # Verificar si los archivos de certificado y llave existen
    if not os.path.isfile(ssl_cert):
        print(f"Error: No se encontró el archivo de certificado en la ruta '{ssl_cert}'.")
        sys.exit(1)
    if not os.path.isfile(ssl_key):
        print(f"Error: No se encontró la llave privada en la ruta '{ssl_key}'.")
        sys.exit(1)
    
    # Cargar y analizar el certificado
    try:
        with open(ssl_cert, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    except Exception as e:
        print(f"Error: No se pudo leer el certificado. Detalles: {e}")
        sys.exit(1)
    
    # Verificar la fecha de expiración
    not_after = cert.not_valid_after_utc  # Fecha con zona horaria UTC
    now = datetime.datetime.now(datetime.timezone.utc)  # Convertir a zona horaria UTC

    if now > not_after:
        print("Error: El certificado ha expirado.")
        sys.exit(1)
    else:
        # Podés implementar una lógica para advertir si el certificado está cerca de expirar
        days_to_expire = (not_after - now).days
        if days_to_expire < 15:
            print(f"Advertencia: El certificado expira en {days_to_expire} día(s).")
        else:
            print(f"El certificado es válido. Expira en {days_to_expire} día(s).")
    
    print("La verificación de los certificados finalizó sin errores.")

if __name__ == "__main__":
    main()
