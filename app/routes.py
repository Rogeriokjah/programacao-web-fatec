from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Disciplina, Curso, Professor, Aluno, Usuario
from forms import DisciplinaForm, CursoForm, ProfessorForm, AlunoForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].strip()  # Remove espaços em branco no início e no fim
    
    print("Recebido do formulário - Usuário:", username, "Senha:", password)  # Debug da senha recebida

    # Busca o usuário no banco de dados
    user = Usuario.query.filter_by(username=username).first()

    if user:
        print("Usuário encontrado no banco de dados:", user.username)
        print("Senha armazenada no banco de dados:", user.password)  # Exibe a senha armazenada

        # Compara as senhas diretamente, sem hashing
        if user.password == password:
            print("Senha correta para o usuário:", username)  # Depuração para senha correta
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Senha incorreta para o usuário:", username)  # Depuração para senha incorreta
            flash('Senha incorreta. Tente novamente.')
    else:
        print("Usuário não encontrado:", username)  # Depuração para usuário não encontrado
        flash('Usuário não encontrado. Tente novamente.')

    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html')

@app.route('/disciplinas', methods=['GET', 'POST'])
@login_required
def disciplinas():
    Disciplina.ensure_table_exists()
    form = DisciplinaForm()
    if form.validate_on_submit():
        nova_disciplina = Disciplina(nome=form.nome.data, carga_horaria=form.carga_horaria.data)
        db.session.add(nova_disciplina)
        db.session.commit()
        return redirect(url_for('disciplinas'))
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas, form=form, active_page='disciplinas')

@app.route('/cursos', methods=['GET', 'POST'])
@login_required
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
    return render_template('cursos.html', cursos=cursos, form=form, active_page='cursos')

@app.route('/professores', methods=['GET', 'POST'])
@login_required
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
    return render_template('professores.html', professores=professores, form=form, active_page='professores')

@app.route('/alunos', methods=['GET', 'POST'])
@login_required
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
            senha=form.senha.data,
            curso_id=form.curso.data
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('alunos'))
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos, form=form, active_page='alunos')


if __name__ == "__main__":
    app.run(debug=True)
