# app/config/validators/signature_validator.py

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, ed448

from app.config.validators.abstract_validator import AbstractValidator
from app.config.ssl_certificate import SSLCertificate
from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

class SignatureValidator(AbstractValidator):
    """
    Valida la firma digital del certificado (self-signed).
    No detiene la ejecución, solo retorna False si es inválida.
    """
    def validate(self, certificate: SSLCertificate) -> bool:
        try:
            public_key = certificate.public_key

            if certificate.is_rsa():
                public_key.verify(
                    certificate.signature,
                    certificate.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    certificate.signature_hash_algorithm
                )
            elif certificate.is_ec():
                public_key.verify(
                    certificate.signature,
                    certificate.tbs_certificate_bytes,
                    ec.ECDSA(certificate.signature_hash_algorithm)
                )
            elif certificate.is_ed25519() or certificate.is_ed448():
                public_key.verify(
                    certificate.signature,
                    certificate.tbs_certificate_bytes
                )
            else:
                logger.warning("⚠️ Tipo de clave no reconocido para la verificación de la firma.")
                return True  # No lo consideramos error fatal

            logger.info("✅ La firma digital del certificado es válida.")
            return True
        
        except InvalidSignature:
            logger.error("❌ La firma digital del certificado no es válida.")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al validar la firma digital: {e}")
            return False
