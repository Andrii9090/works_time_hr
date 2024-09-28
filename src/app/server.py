from flask import Flask
from flask_cors import CORS

from app import config

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['FLASK_APP'] = config.FLASK_APP
app.config['DEBUG'] = config.DEBUG
app.config['SQLALCHEMY_ECHO'] = config.DEBUG

