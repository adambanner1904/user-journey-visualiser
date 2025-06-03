from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(environment: str):
    app = Flask(__name__)
    app.config.from_object(f'config.{environment.capitalize()}Config')

    db.init_app(app)

    from .index import index_bp
    app.register_blueprint(index_bp)

    return app
    