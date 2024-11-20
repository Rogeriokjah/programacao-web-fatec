from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Disciplina, Curso, Professor, Aluno, Usuario, curso_disciplina
from forms import DisciplinaForm, CursoForm, ProfessorForm, AlunoForm
from config import Config
from sqlalchemy import text
import logging

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

    if request.method == 'POST':
        # Atualizar o nome do curso
        curso.nome = request.form.get('nome')

        # Atualizar as disciplinas associadas
        disciplinas_ids = request.form.get('disciplinas', '')
        if disciplinas_ids:
            # Converter IDs para inteiros
            disciplinas_ids = [int(d_id) for d_id in disciplinas_ids.split(",") if d_id]
            # Consultar as disciplinas selecionadas
            disciplinas = Disciplina.query.filter(Disciplina.id.in_(disciplinas_ids)).all()
            curso.disciplinas = disciplinas
        else:
            curso.disciplinas = []  # Remove todas as associações

        try:
            db.session.commit()
            flash("Curso atualizado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar curso: {str(e)}", "danger")

        return redirect(url_for('listar_cursos'))

    # Retornar os dados em JSON para preencher o modal
    if request.method == 'GET':
        disciplinas = [{"id": d.id, "nome": d.nome, "carga_horaria": d.carga_horaria} for d in curso.disciplinas]
        return jsonify({
            "id": curso.id,
            "nome": curso.nome,
            "disciplinas": disciplinas
        })


@app.route('/buscar_cursos', methods=['GET'])
@login_required
def buscar_cursos():
    query = request.args.get('query', '').strip()
    limite = 7  # Limitar a 7 registros
    cursos = Curso.query.filter(Curso.nome.ilike(f"%{query}%")).limit(limite).all()
    return jsonify([{"id": curso.id, "nome": curso.nome} for curso in cursos])

@app.route('/buscar_curso', methods=['GET'])
@login_required
def buscar_curso():
    curso_id = request.args.get('id', type=int)
    curso = Curso.query.get_or_404(curso_id)
    disciplinas = [{"id": d.id, "nome": d.nome, "carga_horaria": d.carga_horaria} for d in curso.disciplinas]
    
    return jsonify({
        "id": curso.id,
        "nome": curso.nome,
        "disciplinas": disciplinas
    })
    
    

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
@login_required
def buscar_professor():
    professor_id = request.args.get('id', type=int)
    professor = Professor.query.get_or_404(professor_id)
    disciplinas = [{"id": d.id, "nome": d.nome, "carga_horaria": d.carga_horaria} for d in professor.disciplinas]
    
    return jsonify({
        "id": professor.id,
        "nome": professor.nome,
        "telefone": professor.telefone,
        "usuario": professor.usuario,
        "disciplinas": disciplinas
    })
   
    
@app.route('/adicionar_professor', methods=['POST'])
def adicionar_professor():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    disciplinas_ids = request.form.get('disciplinas')

    professor = Professor(nome=nome, telefone=telefone, usuario=usuario, senha=senha)

    if disciplinas_ids:
        disciplinas_ids = [int(d_id) for d_id in disciplinas_ids.split(",")]
        professor.disciplinas = Disciplina.query.filter(Disciplina.id.in_(disciplinas_ids)).all()

    db.session.add(professor)
    db.session.commit()

    return redirect(url_for('listar_professores'))


@app.route('/editar_professor/<int:id>', methods=['POST'])
def editar_professor(id):
    professor = Professor.query.get_or_404(id)

    professor.nome = request.form.get('nome')
    professor.telefone = request.form.get('telefone')
    professor.usuario = request.form.get('usuario')
    professor.senha = request.form.get('senha')
    disciplinas_ids = request.form.get('disciplinas')

    if disciplinas_ids:
        disciplinas_ids = [int(d_id) for d_id in disciplinas_ids.split(",")]
        professor.disciplinas = Disciplina.query.filter(Disciplina.id.in_(disciplinas_ids)).all()
    else:
        professor.disciplinas = []  # Remove todas as disciplinas vinculadas

    db.session.commit()
    return redirect(url_for('listar_professores'))

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

@app.route('/editar_aluno/<int:id>', methods=['POST'])
@login_required
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    try:
        # Captura os dados do formulário
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        endereco = request.form.get('endereco')
        curso_id = request.form.get('curso')

        # Atualiza os campos do aluno
        aluno.nome = nome
        aluno.cpf = cpf
        aluno.usuario = usuario
        aluno.senha = senha
        aluno.endereco = endereco
        aluno.curso_id = curso_id if curso_id else None

        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao atualizar aluno: {e}", "danger")

    return redirect(url_for('listar_alunos'))

@app.route('/alunos/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash("Aluno excluído com sucesso!", "success")
    return redirect(url_for('listar_alunos'))

@app.route('/alunos/excluir_selecionados', methods=['POST'])
@login_required
def excluir_alunos_selecionados():
    data = request.get_json()
    ids = data.get('alunos_ids', [])

    # Log para depuração
    app.logger.info(f"IDs recebidos para exclusão: {ids}")

    if ids:
        try:
            # Tentar excluir os alunos com os IDs fornecidos
            deleted = Aluno.query.filter(Aluno.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()

            # Log de sucesso
            app.logger.info(f"Registros excluídos com sucesso: {deleted}")

            flash(f"{len(ids)} aluno(s) excluído(s) com sucesso!", "success")
            return jsonify({"success": True})
        except Exception as e:
            # Log em caso de erro
            app.logger.error(f"Erro ao excluir alunos: {str(e)}")
            db.session.rollback()
            flash(f"Erro ao excluir os alunos: {str(e)}", "danger")
            return jsonify({"success": False, "error": str(e)})
    else:
        # Log caso nenhum ID seja enviado
        app.logger.warning("Nenhum aluno selecionado para exclusão.")
        flash("Nenhum aluno selecionado para exclusão.", "warning")
        return jsonify({"success": False, "message": "Nenhum aluno selecionado."})


@app.route('/buscar_aluno', methods=['GET'])
@login_required
def buscar_aluno():
    aluno_id = request.args.get('id', type=int)
    if not aluno_id:
        return jsonify({"error": "ID do aluno não fornecido"}), 400

    aluno = db.session.query(
        Aluno.id, Aluno.nome, Aluno.cpf, Aluno.endereco, Aluno.senha, Aluno.usuario, Aluno.curso_id, Curso.nome.label('curso_nome')
    ).outerjoin(Curso, Aluno.curso_id == Curso.id).filter(Aluno.id == aluno_id).first()

    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    return jsonify({
        "id": aluno.id,
        "nome": aluno.nome,
        "cpf": aluno.cpf,
        "endereco": aluno.endereco,
        "senha": aluno.senha,
        "usuario": aluno.usuario,
        "curso_id": aluno.curso_id,
        "curso_nome": aluno.curso_nome
    })


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
    return jsonify([{'id': d.id, 'nome': d.nome, 'carga_horaria': d.carga_horaria} for d in disciplinas])

@app.route('/buscar_disciplina', methods=['GET'])
@login_required
def buscar_disciplina():
    disciplina_id = request.args.get('id', type=int)
    disciplina = Disciplina.query.get_or_404(disciplina_id)
    return jsonify({
        "id": disciplina.id,
        "nome": disciplina.nome,
        "carga_horaria": disciplina.carga_horaria
    })
   
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
