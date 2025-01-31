# app/config/validators/abstract_validator.py

from abc import ABC, abstractmethod
from app.config.ssl_certificate import SSLCertificate

class AbstractValidator(ABC):
    """
    Interfaz base para validaciones de certificados.
    """
    @abstractmethod
    def validate(self, certificate: SSLCertificate) -> bool:
        """
        Realiza la validación del certificado.
        Devuelve True si la validación pasa, False si falla.
        """
        pass
