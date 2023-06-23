import logging
import os

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from logging.handlers import RotatingFileHandler


jwt = JWTManager()

# init SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
