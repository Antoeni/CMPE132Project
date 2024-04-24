import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_mapping(
    SECRET_KEY = 'secret password',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'website.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

#This will create the data base and login, for when we call routes
db = SQLAlchemy(app)
login = LoginManager(app)


login.login_view = 'login'

from website import routes


