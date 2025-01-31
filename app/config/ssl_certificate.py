# app/config/ssl_certificate.py

import datetime
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, ed448
from cryptography.hazmat.primitives import hashes

class SSLCertificate:
    """
    Clase que encapsula los datos de un certificado X.509.
    """
    def __init__(self, cert: x509.Certificate):
        self._cert = cert

    @property
    def not_valid_after(self) -> datetime.datetime:
        return self._cert.not_valid_after

    @property
    def issuer(self) -> str:
        return self._cert.issuer.rfc4514_string()

    @property
    def signature(self) -> bytes:
        return self._cert.signature

    @property
    def tbs_certificate_bytes(self) -> bytes:
        return self._cert.tbs_certificate_bytes

    @property
    def signature_hash_algorithm(self) -> hashes.HashAlgorithm:
        return self._cert.signature_hash_algorithm
    
    @property
    def public_key(self):
        return self._cert.public_key()

    def get_san_list(self):
        """
        Devuelve la lista de SAN (Subject Alternative Names) como DNSName.
        """
        try:
            ext = self._cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            return ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            return []

    # Ejemplo de métodos para identificar tipo de clave
    def is_rsa(self) -> bool:
        return isinstance(self.public_key, rsa.RSAPublicKey)

    def is_ec(self) -> bool:
        return isinstance(self.public_key, ec.EllipticCurvePublicKey)

    def is_ed25519(self) -> bool:
        return isinstance(self.public_key, ed25519.Ed25519PublicKey)

    def is_ed448(self) -> bool:
        return isinstance(self.public_key, ed448.Ed448PublicKey)
