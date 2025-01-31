# app/config/check.py

from app.config.ssl_config_loader import SSLConfigLoader
from app.config.certificate_reader import CertificateReader
from app.config.ssl_verifier import SSLVerifier

# Validadores
from app.config.validators.expiration_validator import ExpirationValidator
from app.config.validators.signature_validator import SignatureValidator
from app.config.validators.san_validator import SANValidator

from app.utils.logging.logger_configurator import LoggerConfigurator

logger = LoggerConfigurator().configure()

def main():
    logger.info("🚀 Iniciando verificación de certificados SSL.")

    # 1. Cargar configuración
    config_loader = SSLConfigLoader()
    config_loader.validate()

    ssl_cert = config_loader.ssl_cert
    ssl_key = config_loader.ssl_key
    expected_hostname = config_loader.expected_hostname

    # 2. Leer el certificado
    reader = CertificateReader()
    certificate = reader.load_certificate(ssl_cert)

    # Log del issuer
    logger.info(f"🔍 Emisor del certificado: {certificate.issuer}")

    # 3. Crear el verificador con los validadores necesarios
    verifier = SSLVerifier(validators=[
        ExpirationValidator(),
        SignatureValidator(),
        SANValidator(expected_hostname=expected_hostname)
    ])

    # 4. Ejecutar validaciones
    all_valid = verifier.verify(certificate)
    if not all_valid:
        logger.error("❌ La verificación de los certificados falló.")
        # Aquí decides si continuar o detener la ejecución
        raise SystemExit("Error: El certificado no pasó todas las validaciones.")

    logger.info("✅ La verificación de los certificados finalizó sin errores.")

if __name__ == "__main__":
    main()
