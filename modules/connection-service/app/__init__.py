from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object("app.config")
    
    db.init_app(app)
    CORS(app)

    from app.routes import api
    api.init_app(app)

    return app
