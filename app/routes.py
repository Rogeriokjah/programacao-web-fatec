# routes.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Disciplina, Curso, Professor, Aluno
from forms import DisciplinaForm, CursoForm, ProfessorForm, AlunoForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/api/init_db', methods=['POST'])
def init_db():
    with app.app_context():
        Disciplina.ensure_table_exists()
        Curso.ensure_table_exists()
        Professor.ensure_table_exists()
        Aluno.ensure_table_exists()
    return jsonify({"message": "Banco de dados e tabelas verificadas e criadas, se necessário."})

@app.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    Disciplina.ensure_table_exists()
    form = DisciplinaForm()
    if form.validate_on_submit():
        nova_disciplina = Disciplina(nome=form.nome.data, carga_horaria=form.carga_horaria.data)
        db.session.add(nova_disciplina)
        db.session.commit()
        return redirect(url_for('disciplinas'))
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas, form=form)

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    Curso.ensure_table_exists()
    Disciplina.ensure_table_exists()
    form = CursoForm()
    form.disciplinas.choices = [(d.id, d.nome) for d in Disciplina.query.all()]
    if form.validate_on_submit():
        novo_curso = Curso(nome=form.nome_curso.data)
        db.session.add(novo_curso)
        db.session.commit()
        return redirect(url_for('cursos'))
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos, form=form)

@app.route('/professores', methods=['GET', 'POST'])
def professores():
    Professor.ensure_table_exists()
    Disciplina.ensure_table_exists()
    form = ProfessorForm()
    form.disciplinas.choices = [(d.id, d.nome) for d in Disciplina.query.all()]
    if form.validate_on_submit():
        novo_professor = Professor(
            nome=form.nome.data,
            telefone=form.telefone.data,
            usuario=form.usuario.data,
            senha=form.senha.data
        )
        db.session.add(novo_professor)
        db.session.commit()
        return redirect(url_for('professores'))
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores, form=form)

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    Aluno.ensure_table_exists()
    Curso.ensure_table_exists()
    form = AlunoForm()
    form.curso.choices = [(c.id, c.nome) for c in Curso.query.all()]
    if form.validate_on_submit():
        novo_aluno = Aluno(
            nome=form.nome.data,
            cpf=form.cpf.data,
            endereco=form.endereco.data,
            senha=form.senha.data
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('alunos'))
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos, form=form)

# Bloco de execução principal
if __name__ == "__main__":
    app.run(debug=True)
