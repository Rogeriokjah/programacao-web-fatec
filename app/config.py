# config.py
class Config:
    DATABASE_NAME = 'cadastro'
    DATABASE_URL = '127.0.0.1'
    DATABASE_PORT = 3306
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''  # Se houver senha, insira-a aqui
    CLIENT_KEY = 'sua_chave_de_cliente'
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}?ssl=true'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sua_chave_secreta'
