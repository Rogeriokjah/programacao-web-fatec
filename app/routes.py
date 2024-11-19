from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Disciplina, Curso, Professor, Aluno, Usuario, curso_disciplina
from forms import DisciplinaForm, CursoForm, ProfessorForm, AlunoForm
from config import Config
from sqlalchemy import text

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

@app.route('/disciplinas', methods=['GET'])
@login_required
def listar_disciplinas():
    form = DisciplinaForm()
    limite = request.args.get('limite', 10, type=int)  # Define um limite padrão de 10
    disciplinas = Disciplina.query.limit(limite).all()
    #disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas, form=form, active_page='disciplinas')

@app.route('/disciplinas/criar', methods=['POST'])
@login_required
def criar_disciplina():
    form = DisciplinaForm()
    if form.validate_on_submit():
        nova_disciplina = Disciplina(nome=form.nome.data, carga_horaria=form.carga_horaria.data)
        db.session.add(nova_disciplina)
        db.session.commit()
        flash("Disciplina adicionada com sucesso!", "success")
        return redirect(url_for('listar_disciplinas'))
    else:
        flash("Erro ao adicionar a disciplina. Verifique os dados e tente novamente.", "danger")
        return redirect(url_for('listar_disciplinas'))

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
        return redirect(url_for('listar_disciplinas'))
    return render_template('editar_disciplina.html', form=form, disciplina=disciplina)

@app.route('/disciplinas/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    db.session.delete(disciplina)
    db.session.commit()
    flash("Disciplina excluída com sucesso!", "success")
    return redirect(url_for('listar_disciplinas'))

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

@app.route('/cursos', methods=['GET'])
@login_required
def listar_cursos():
    form = CursoForm()
    form.disciplinas.choices = [(d.id, d.nome) for d in Disciplina.query.all()]
    if form.validate_on_submit():
        novo_curso = Curso(nome=form.nome.data)
        db.session.add(novo_curso)
        db.session.commit()
        flash("Curso adicionado com sucesso!", "success")
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos, form=form, active_page='cursos')

@app.route('/adicionar_curso', methods=['POST'])
@login_required
def adicionar_curso():
    nome_curso = request.form.get('nome')
    disciplinas_ids = request.form.get('disciplinas', '')

    # Converte IDs separados por vírgulas em uma lista de inteiros
    disciplinas_ids = [int(d_id) for d_id in disciplinas_ids.split(",") if d_id]

    novo_curso = Curso(nome=nome_curso)
    db.session.add(novo_curso)
    db.session.commit()

    if disciplinas_ids:
        disciplinas = Disciplina.query.filter(Disciplina.id.in_(disciplinas_ids)).all()
        novo_curso.disciplinas.extend(disciplinas)
        db.session.commit()

    flash("Curso adicionado com sucesso!", "success")
    return redirect(url_for('listar_cursos'))

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_curso(id):
    curso = Curso.query.get_or_404(id)
    form = CursoForm(obj=curso)

    if request.method == 'POST':
        # Atualiza o nome do curso
        curso.nome = form.nome.data

        # Remove todas as disciplinas relacionadas ao curso
        db.session.execute(curso_disciplina.delete().where(curso_disciplina.c.curso_id == id))
        
        # Adiciona as disciplinas selecionadas novamente
        disciplinas_ids = request.form.getlist('disciplinas')
        for disciplina_id in disciplinas_ids:
            db.session.execute(curso_disciplina.insert().values(curso_id=id, disciplina_id=int(disciplina_id)))
        
        db.session.commit()
        flash("Curso atualizado com sucesso!", "success")
        return redirect(url_for('listar_cursos'))

    disciplinas_selecionadas = [d.id for d in curso.disciplinas]
    return render_template('editar_curso.html', curso=curso, form=form, disciplinas_selecionadas=disciplinas_selecionadas)

@app.route('/buscar_cursos', methods=['GET'])
@login_required
def buscar_cursos():
    query = request.args.get('query', '').strip()
    limite = 7  # Limitar a 7 registros
    cursos = Curso.query.filter(Curso.nome.ilike(f"%{query}%")).limit(limite).all()
    return jsonify([{"id": curso.id, "nome": curso.nome} for curso in cursos])

@app.route('/cursos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_curso(id):
    curso = Curso.query.get_or_404(id)
    try:
        db.session.delete(curso)
        db.session.commit()
        flash("Curso excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o curso: {str(e)}", "danger")
    return redirect(url_for('listar_cursos'))

@app.route('/cursos/excluir_selecionados', methods=['POST'])
@login_required
def excluir_cursos_selecionados():
    data = request.get_json()
    ids = data.get('curso_ids', [])
    
    if ids:
        try:
            # Deleta os cursos selecionados
            Curso.query.filter(Curso.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
            flash(f"{len(ids)} curso(s) excluído(s) com sucesso!", "success")
            return jsonify({"success": True})
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao excluir os cursos: {str(e)}", "danger")
            return jsonify({"success": False, "error": str(e)})
    else:
        flash("Nenhum curso selecionado para exclusão.", "warning")
        return jsonify({"success": False, "message": "Nenhum curso selecionado."})


@app.route('/professores', methods=['GET'])
def listar_professores():
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores)

@app.route('/buscar_professor', methods=['GET'])
def buscar_professor():
    professor_id = request.args.get('id')
    professor = Professor.query.get(professor_id)
    if professor:
        return jsonify({
            "id": professor.id,
            "nome": professor.nome,
            "telefone": professor.telefone,
            "usuario": professor.usuario
        })
    return jsonify({"error": "Professor não encontrado"}), 404

@app.route('/adicionar_professor', methods=['POST'])
def adicionar_professor():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    disciplinas_ids = request.form.get('disciplinas', '')
    novo_professor = Professor(nome=nome, telefone=telefone, usuario=usuario, senha=senha)
    db.session.add(novo_professor)
    db.session.commit()
    
    disciplinas_ids = [int(d_id) for d_id in disciplinas_ids.split(",") if d_id]
    if disciplinas_ids:
        disciplinas = Disciplina.query.filter(Disciplina.id.in_(disciplinas_ids)).all()
    novo_professor.disciplinas.extend(disciplinas)
    db.session.commit()
    flash("Curso adicionado com sucesso!", "success")
    return redirect(url_for('listar_professores'))
    #return jsonify({"message": "Professor adicionado com sucesso!"})

@app.route('/editar_professor/<int:professor_id>', methods=['POST'])
def editar_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({"error": "Professor não encontrado"}), 404
    professor.nome = request.form.get("nome")
    professor.telefone = request.form.get("telefone")
    professor.usuario = request.form.get("usuario")
    db.session.commit()
    return jsonify({"message": "Professor atualizado com sucesso!"})

@app.route('/professores/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_professor(id):
    professor = Professor.query.get_or_404(id)
    try:
        db.session.delete(professor)
        db.session.commit()
        flash("Professor excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o Professor: {str(e)}", "danger")
    return redirect(url_for('listar_professores'))

@app.route('/professores/excluir_selecionados', methods=['POST'])
@login_required
def excluir_professores_selecionados():
    data = request.get_json()
    ids = data.get('professores_ids', [])
    
    if ids:
        try:
            # Deleta os Professores selecionados
            Professor.query.filter(Professor.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
            flash(f"{len(ids)} Professor(es) excluído(s) com sucesso!", "success")
            return jsonify({"success": True})
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao excluir o(s) Professor(es): {str(e)}", "danger")
            return jsonify({"success": False, "error": str(e)})
    else:
        flash("Nenhum professor selecionado para exclusão.", "warning")
        return jsonify({"success": False, "message": "Nenhum curso selecionado."})

@app.route('/alunos', methods=['GET'])
@login_required
def listar_alunos():
    alunos = db.session.query(
        Aluno.id, Aluno.nome, Aluno.cpf, Aluno.endereco, Curso.nome.label('curso_nome')
    ).outerjoin(Curso, Aluno.curso_id == Curso.id).all()
    print("Alunos encontrados:", alunos)  # Depuração para verificar os dados retornados
    return render_template('alunos.html', alunos=alunos)

@app.route('/adicionar_aluno', methods=['POST'])
@login_required
def adicionar_aluno():
    form = AlunoForm()

    # Debug para ver os dados recebidos
    print("Dados recebidos no formulário:", request.form)

    # Validações individuais
    erros = []
    if not form.nome.data:
        erros.append("O campo Nome é obrigatório.")
    if not form.cpf.data:
        erros.append("O campo CPF é obrigatório.")
    if not form.usuario.data:
        erros.append("O campo Usuário é obrigatório.")
    if not form.senha.data:
        erros.append("O campo Senha é obrigatório.")

    if erros:
        for erro in erros:
            flash(erro, "danger")
        return redirect(url_for('listar_alunos'))

    # Dados válidos - Criar novo aluno
    try:
        novo_aluno = Aluno(
            nome=form.nome.data,
            cpf=form.cpf.data,
            endereco=form.endereco.data or None,  # Permitir `NULL`
            usuario=form.usuario.data,
            senha=form.senha.data,
            curso_id=form.curso.data or None  # Permitir `NULL`
        )
        db.session.add(novo_aluno)
        db.session.commit()
        flash("Aluno adicionado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar o aluno: {e}")
        flash(f"Erro ao salvar o aluno: {e}", "danger")

    return redirect(url_for('listar_alunos'))

app.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoForm(obj=disciplina)
    if form.validate_on_submit():
        aluno.nome=form.nome.data,
        aluno.cpf=form.cpf.data,
        aluno.endereco=form.endereco.data,
        aluno.senha=form.senha.data,
        aluno.curso_id=form.curso.data
        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
        return redirect(url_for('listar_alunos'))
    return render_template('alunos.html', form=form, aluno=aluno)

@app.route('/alunos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash("Aluno excluído com sucesso!", "success")
    return redirect(url_for('listar_alunos'))

@app.route('/buscar_disciplinas', methods=['GET'])
@login_required
def buscar_disciplinas():
    query = request.args.get('query', '')
    exclude = request.args.get('exclude', '')
    limite = request.args.get('limite', 5, type=int)  # Define um limite padrão de 5

    # Converte exclude em uma lista de inteiros
    exclude_ids = list(map(int, exclude.split(','))) if exclude else []

    # Filtra as disciplinas com o nome correspondente e exclui as já selecionadas
    disciplinas = Disciplina.query.filter(
        Disciplina.nome.like(f"%{query}%"),
        ~Disciplina.id.in_(exclude_ids)
    ).limit(limite).all()

    # Retorna as disciplinas no formato JSON
    return jsonify([{'id': d.id, 'nome': d.nome} for d in disciplinas])

if __name__ == "__main__":
    app.run(debug=True)
