import logging

from flask import Flask, render_template # type: ignore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    from .index import index_bp
    app.register_blueprint(index_bp)
    # from .controllers.ujv import ujv
    # from .controllers.projects import projects
    # app.register_blueprint(ujv)
    # app.register_blueprint(projects)

    return app
    