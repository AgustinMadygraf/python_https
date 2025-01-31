# app/config/validators/san_validator.py

from app.config.validators.abstract_validator import AbstractValidator
from app.config.ssl_certificate import SSLCertificate
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class SANValidator(AbstractValidator):
    """
    Verifica que el dominio esperado se encuentre en la extensión SAN.
    """
    def __init__(self, expected_hostname: str):
        self.expected_hostname = expected_hostname

    def validate(self, certificate: SSLCertificate) -> bool:
        san_list = certificate.get_san_list()
        if not san_list:
            logger.error("❌ El certificado no contiene una extensión SAN.")
            return False

        if self.expected_hostname not in san_list:
            logger.error(f"❌ El certificado no incluye '{self.expected_hostname}' en el SAN.")
            return False

        logger.info(f"✅ El certificado es válido para '{self.expected_hostname}' (SAN: {san_list})")
        return True
