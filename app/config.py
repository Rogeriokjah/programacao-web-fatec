# config.py
class Config:
    DATABASE_NAME = 'TrabalhoVollo'
    DATABASE_URL = '127.0.0.1'
    DATABASE_PORT = 3306
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''  # Insira sua senha, se necessário
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '7f2a5b8e69c24c39a3477e9402df3cb4'
