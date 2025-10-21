import os

class Config:
    SECRET_KEY = 'clave123'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///minicore.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
