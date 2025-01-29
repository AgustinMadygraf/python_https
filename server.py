"""
Path: server.py

"""

import os
from app import create_app

if __name__ == "__main__":
    app = create_app()
    # Aquí llamamos a la configuración ya validada
    SSL_CERT = os.getenv("SSL_CERT")
    SSL_KEY = os.getenv("SSL_KEY")
    
    # Corremos la app con contexto SSL
    app.run(host="0.0.0.0", port=443, ssl_context=(SSL_CERT, SSL_KEY))
