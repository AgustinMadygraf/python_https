# app/config/certificate_reader.py

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from app.utils.logging.logger_configurator import LoggerConfigurator
from app.config.ssl_certificate import SSLCertificate

logger = LoggerConfigurator().configure()

class CertificateReader:
    """
    Clase encargada de cargar un certificado desde un archivo PEM
    y encapsularlo en un SSLCertificate.
    """
    def load_certificate(self, ssl_cert_path: str) -> SSLCertificate:
        try:
            with open(ssl_cert_path, 'rb') as cert_file:
                cert_data = cert_file.read()
                cert = x509.load_pem_x509_certificate(cert_data, default_backend())
                logger.info("✅ Certificado SSL cargado correctamente.")
                return SSLCertificate(cert)
        except Exception as e:
            logger.error(f"❌ No se pudo leer el certificado. Detalles: {e}")
            raise SystemExit(f"Error: No se pudo leer el certificado. Detalles: {e}")
