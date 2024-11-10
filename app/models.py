from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        return True

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20))
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    senha = db.Column(db.String(100), nullable=False)
