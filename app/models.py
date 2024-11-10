from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def ensure_table_exists():
        if not inspect(db.engine).has_table('usuarios'):
            db.create_all()

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

    @staticmethod
    def ensure_table_exists():
        if not inspect(db.engine).has_table('disciplinas'):
            db.create_all()

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplinas = db.relationship('Disciplina', secondary='curso_disciplina')

    @staticmethod
    def ensure_table_exists():
        if not inspect(db.engine).has_table('cursos'):
            db.create_all()

# Tabelas de associação para relacionamentos muitos-para-muitos
curso_disciplina = db.Table('curso_disciplina',
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id')),
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplinas.id'))
)

professor_disciplina = db.Table('professor_disciplina',
    db.Column('professor_id', db.Integer, db.ForeignKey('professores.id')),
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplinas.id'))
)

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20))
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    disciplinas = db.relationship('Disciplina', secondary=professor_disciplina)

    @staticmethod
    def ensure_table_exists():
        if not inspect(db.engine).has_table('professores'):
            db.create_all()

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    senha = db.Column(db.String(100), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    curso = db.relationship('Curso')

    @staticmethod
    def ensure_table_exists():
        if not inspect(db.engine).has_table('alunos'):
            db.create_all()
