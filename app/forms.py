from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class DisciplinaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    carga_horaria = IntegerField('Carga Horária', validators=[DataRequired()])

class CursoForm(FlaskForm):
    nome = StringField('Nome do Curso', validators=[DataRequired()])
    disciplinas = SelectMultipleField('Disciplinas', choices=[])

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[Length(max=20)])
    usuario = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])

class AlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11)])
    endereco = StringField('Endereço', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
