import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_APP = os.getenv('FLASK_APP')
DEBUG = os.getenv('DEBUG')
