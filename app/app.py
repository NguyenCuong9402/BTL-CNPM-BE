# -*- coding: utf-8 -*-


from flask import Flask

from flask_cors import CORS


from app.extensions import jwt, migrate, ma
from app.api import v1 as api_v1
from app.settings import DevConfig
from app.models import db


def create_app():
    """
    Init App
    :return:
    """
    config_object = DevConfig
    app = Flask(__name__, static_url_path="", static_folder="./files")
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    return app


def register_extensions(app):
    """
    Init extension
    :param app:
    :return:
    """
    db.app = app
    db.init_app(app)  # SQLAlchemy
    jwt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.user.api, url_prefix='/api/v1/user')









