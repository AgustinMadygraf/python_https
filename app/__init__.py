from flask import Flask
from flask_cors import CORS
from app.config import load_and_validate_config
from app.routes.main import main_bp

from flask_cors import CORS

def create_app():
    load_and_validate_config()
    app = Flask(__name__)

    # Permitir todas las solicitudes para pruebas (puedes restringir después)
    CORS(app, resources={r"/*": {"origins": ["https://madygraf.com"], "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

    app.register_blueprint(main_bp)
    return app
