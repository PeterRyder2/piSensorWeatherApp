from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
app = Flask(__name__)


# DATABASE STUFF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db =SQLAlchemy(app)
api = Api (app)

from app import routes