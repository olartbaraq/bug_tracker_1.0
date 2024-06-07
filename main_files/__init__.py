#!/usr/bin env python3


# Copyright (c) Akanbi Mubaraq Olatunde. Aspiring back-end developer


"""
Some important modules are to be imported to make the flask-sqlalchemy work
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bugtracker3.db"
    app.config["SECRET_KEY"] = "277aca85092d962dda58178e"

    db.init_app(app)
    # bcrypt.init_app(app)
    # login_manager.init_app(app)

    # login_manager.login_view = "sign_in"
    # login_manager.login_message_category = "info"

    from .all_routes import bp  # Import the blueprint

    app.register_blueprint(bp)  # Register the blueprint

    return app
