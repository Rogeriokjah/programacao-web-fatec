from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Tabela de associação entre Curso e Disciplina
curso_disciplina = db.Table('curso_disciplina',
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplinas.id'), primary_key=True)
)

# Tabela de associação entre Professor e Disciplina
professor_disciplina = db.Table('professor_disciplina',
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplinas.id'), primary_key=True),
    db.Column('professor_id', db.Integer, db.ForeignKey('professores.id'), primary_key=True)
)

# Tabela de associação entre Aluno e Curso
aluno_curso = db.Table('aluno_curso',
    db.Column('aluno_id', db.Integer, db.ForeignKey('alunos.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    disciplinas = relationship('Disciplina', secondary=curso_disciplina, backref='cursos')

    @hybrid_property
    def carga_horaria_total(self):
        return sum(disciplina.carga_horaria for disciplina in self.disciplinas)
class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20))
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    disciplinas = relationship('Disciplina', secondary=professor_disciplina, backref='professores')

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    senha = db.Column(db.String(100), nullable=False)
    curso = relationship('Curso', secondary=aluno_curso, backref='alunos')
