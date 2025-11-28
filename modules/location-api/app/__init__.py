from flask import Flask
from flask_cors import CORS

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object("app.config")
    
    CORS(app)

    from app.routes import api
    api.init_app(app)

    return app
