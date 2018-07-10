from flask_io import FlaskIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dictalchemy import DictableModel
from sqlalchemy.ext.declarative import declarative_base
from flask_apidoc import ApiDoc

Base = declarative_base(cls=DictableModel)
db = SQLAlchemy()
io = FlaskIO()
doc = ApiDoc()
login_manager = LoginManager()
