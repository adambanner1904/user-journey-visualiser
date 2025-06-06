import os.path

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(environment: str):
    app = Flask(__name__)
    app.config.from_object(f'config.{environment.capitalize()}Config')

    create_index(app)

    # db initialisation
    from .models import Project, Service, Endpoint, Link, Journey
    db.init_app(app)
    create_db(app)

    # Blueprint registration
    from .projects import projects
    app.register_blueprint(projects, url_prefix="/projects")

    return app


def create_index(app):
    @app.route("/")
    def index():
        return render_template('index.html')


def create_db(app: Flask) -> None:
    if not os.path.exists(f"instance/{app.config['DB_PATH']}"):
        with app.app_context():
            db.create_all()
