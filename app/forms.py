# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length

class DisciplinaForm(FlaskForm):
    nome = StringField('Nome da Disciplina', validators=[DataRequired(), Length(max=50)])
    carga_horaria = IntegerField('Carga Horária', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class CursoForm(FlaskForm):
    nome_curso = StringField('Nome do Curso', validators=[DataRequired(), Length(max=100)])
    disciplinas = SelectMultipleField('Disciplinas', coerce=int)
    submit = SubmitField('Cadastrar')

class ProfessorForm(FlaskForm):
    nome = StringField('Nome do Professor', validators=[DataRequired(), Length(max=50)])
    telefone = StringField('Telefone', validators=[Length(max=20)])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(max=20)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    disciplinas = SelectMultipleField('Disciplinas', coerce=int)
    submit = SubmitField('Cadastrar')

class AlunoForm(FlaskForm):
    nome = StringField('Nome do Aluno', validators=[DataRequired(), Length(max=100)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=11)])
    endereco = StringField('Endereço', validators=[Length(max=200)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    curso = SelectMultipleField('Curso', coerce=int)
    submit = SubmitField('Cadastrar')
