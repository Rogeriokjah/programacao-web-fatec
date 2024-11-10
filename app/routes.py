from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from models import db, Disciplina, Curso, Professor, Aluno, Usuario
from forms import DisciplinaForm, CursoForm, ProfessorForm, AlunoForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configuração do SQLAlchemy
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def setup_database():
    with app.app_context():
        engine = db.engine
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS TrabalhoVollo DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;"))

        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['DATABASE_USER']}:{app.config['DATABASE_PASSWORD']}@localhost/TrabalhoVollo"
        
        db.create_all()

        if not Usuario.query.filter_by(username="Admin").first():
            admin_user = Usuario(username="Admin", password=generate_password_hash("Admin123Admin", method='pbkdf2:sha256'))
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário Admin criado com sucesso.")

setup_database()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].strip()
    user = Usuario.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        flash('Usuário ou senha incorretos. Tente novamente.')
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
    form = DisciplinaForm()
    if form.validate_on_submit():
        nova_disciplina = Disciplina(nome=form.nome.data, carga_horaria=form.carga_horaria.data)
        db.session.add(nova_disciplina)
        db.session.commit()
        flash("Disciplina adicionada com sucesso!", "success")
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas, form=form, active_page='disciplinas')

@app.route('/disciplinas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    form = DisciplinaForm(obj=disciplina)
    if form.validate_on_submit():
        disciplina.nome = form.nome.data
        disciplina.carga_horaria = form.carga_horaria.data
        db.session.commit()
        flash("Disciplina atualizada com sucesso!", "success")
        return redirect(url_for('disciplinas'))
    return render_template('editar_disciplina.html', form=form, disciplina=disciplina)

@app.route('/disciplinas/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    db.session.delete(disciplina)
    db.session.commit()
    flash("Disciplina excluída com sucesso!", "success")
    return redirect(url_for('disciplinas'))

@app.route('/disciplinas/excluir_selecionadas', methods=['POST'])
@login_required
def excluir_disciplinas_selecionadas():
    data = request.get_json()
    ids = data.get('disciplina_ids', [])
    if ids:
        Disciplina.query.filter(Disciplina.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        flash(f"{len(ids)} disciplinas excluídas com sucesso!", "success")
    else:
        flash("Nenhuma disciplina selecionada para exclusão.", "warning")
    return jsonify(success=True)

@app.route('/cursos', methods=['GET', 'POST'])
@login_required
def cursos():
    form = CursoForm()
    form.disciplinas.choices = [(d.id, d.nome) for d in Disciplina.query.all()]
    if form.validate_on_submit():
        novo_curso = Curso(nome=form.nome.data)
        db.session.add(novo_curso)
        db.session.commit()
        flash("Curso adicionado com sucesso!", "success")
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos, form=form, active_page='cursos')

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_curso(id):
    curso = Curso.query.get(id)
    form = CursoForm(obj=curso)
    if form.validate_on_submit():
        curso.nome = form.nome.data
        db.session.commit()
        flash("Curso atualizado com sucesso!", "success")
        return redirect(url_for('cursos'))
    return render_template('editar_curso.html', form=form, active_page='cursos')

@app.route('/cursos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_curso(id):
    curso = Curso.query.get(id)
    db.session.delete(curso)
    db.session.commit()
    flash("Curso excluído com sucesso!", "success")
    return redirect(url_for('cursos'))

@app.route('/cursos/excluir_selecionados', methods=['POST'])
@login_required
def excluir_cursos_selecionados():
    ids = request.json.get('curso_ids', [])
    Curso.query.filter(Curso.id.in_(ids)).delete(synchronize_session='fetch')
    db.session.commit()
    return jsonify({"success": True})


@app.route('/professores', methods=['GET', 'POST'])
@login_required
def professores():
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
        flash("Professor adicionado com sucesso!", "success")
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores, form=form, active_page='professores')

@app.route('/alunos', methods=['GET', 'POST'])
@login_required
def alunos():
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
        flash("Aluno adicionado com sucesso!", "success")
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos, form=form, active_page='alunos')

if __name__ == "__main__":
    app.run(debug=True)
