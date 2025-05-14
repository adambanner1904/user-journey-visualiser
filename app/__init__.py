import logging

from flask import Flask, render_template # type: ignore


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'sentearntnqu19304'
    from .controllers.ujv import ujv
    from .controllers.projects import projects
    app.register_blueprint(ujv)
    app.register_blueprint(projects)

    logging.getLogger('werkzeug').setLevel(logging.WARN)

    return app
    