from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(environment: str):
    app = Flask(__name__)
    app.config.from_object(f'config.{environment.capitalize()}Config')

    # db initialisation
    from .models import Project, Service, Endpoint, Link, Journey
    db.init_app(app)
    create_db(app)

    # Blueprint registration
    from .index import index_bp
    app.register_blueprint(index_bp)

    return app

def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()