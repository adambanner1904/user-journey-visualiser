from flask import Flask, render_template # type: ignore


def create_app():
    app = Flask(__name__)

    from .controller import bp
    app.register_blueprint(bp)

    return app
    