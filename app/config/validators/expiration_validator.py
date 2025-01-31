# app/config/validators/expiration_validator.py

import datetime
from app.config.validators.abstract_validator import AbstractValidator
from app.config.ssl_certificate import SSLCertificate
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class ExpirationValidator(AbstractValidator):
    """
    Valida la fecha de expiración del certificado.
    """
    def __init__(self, min_days_valid: int = 15):
        self.min_days_valid = min_days_valid

    def validate(self, certificate: SSLCertificate) -> bool:
        not_after = certificate.not_valid_after.replace(tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)

        logger.info(f"📅 Fecha de expiración del certificado: {not_after}")
        if now > not_after:
            logger.error("❌ El certificado ha expirado.")
            return False

        days_to_expire = (not_after - now).days
        if days_to_expire < self.min_days_valid:
            logger.warning(f"⚠️ Advertencia: El certificado expira en {days_to_expire} días.")

        return True
