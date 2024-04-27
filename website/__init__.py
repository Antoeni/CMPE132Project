import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret password',
    SQLALCHEMY_DATABASE_URI='sqlite:///website.db'
)

#This will create the data base and login, for when we call routes
db = SQLAlchemy(app)
login = LoginManager(app)

login.login_view = 'login'
from website import routes


