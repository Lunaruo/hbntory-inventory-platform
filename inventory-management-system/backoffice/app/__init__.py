#!/usr/bin/env python3

from flask import Flask

from backoffice.routes.auth import auth_bp
from backoffice.routes.users import users_bp
from backoffice.routes.stock import stock_bp


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config["SECRET_KEY"] = "change_this_secret_key"

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(stock_bp)

    return app