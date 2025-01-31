# app/config/ssl_verifier.py

from typing import List
from app.config.ssl_certificate import SSLCertificate
from app.config.validators.abstract_validator import AbstractValidator
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class SSLVerifier:
    """
    Orquesta el proceso de validación de un SSLCertificate 
    con múltiples validadores.
    """
    def __init__(self, validators: List[AbstractValidator] = None):
        self.validators = validators or []

    def add_validator(self, validator: AbstractValidator):
        self.validators.append(validator)

    def verify(self, certificate: SSLCertificate) -> bool:
        """
        Ejecuta cada validador en orden y retorna True 
        solo si todos pasan.
        """
        for validator in self.validators:
            if not validator.validate(certificate):
                logger.error(f"❌ Falló la validación: {validator.__class__.__name__}")
                return False
        logger.info("✅ Todas las validaciones han pasado exitosamente.")
        return True
