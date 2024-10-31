from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import mysql.connector # pip install mysql-connector-python
import os

load_dotenv() # Pegando variáveis de ambiente
app = Flask(__name__)

# Testando conexão com o banco de dados
try:
    conn = mysql.connector.connect(user=os.getenv('MYSQL_USER'),password=os.getenv('MYSQL_PASSWORD'),host=os.getenv('MYSQL_HOST'),port=os.getenv('MYSQL_PORT'),database=os.getenv('MYSQL_DATABASE'))
except:
    raise Exception("Ocorreu um erro ao se conectar com o banco de dados.")

# SELECT ALL de teste
meu_cursor = conn.cursor()

meu_cursor.execute("SELECT * FROM joaovictor_tbusuario;")
rows = meu_cursor.fetchall()
for row in rows:
    print(row)


# Rota Principal
@app.route('/', methods=['GET'])
def index():
    return render_template("cadastrar-cliente.html")


@app.route("/cadastrar-cliente", methods=['POST'])
def cadastrar_cliente():
    name = request.form['name']
    cpf = request.form['cpf']
    rg = request.form['rg']
    address = request.form['address']
    neighborhood = request.form['neighborhood']
    city = request.form['city']
    cep = request.form['cep']

    # Inserindo no BD:
    query = "INSERT INTO joaovictor_tbcliente (nome, cpf, rg, endereco, bairro, cidade, cep) VALUES (%s, %s, %s,%s, %s, %s,%s)"
    valores = (name, cpf, rg, address, neighborhood, city, cep)
    meu_cursor.execute(query, valores)
    conn.commit() # Commitando o insert no banco de dados
    return redirect(url_for('index'))

@app.route("/cadastrar-usuario", methods=['GET'])
def cadastrar_usuario():
    return render_template("cadastrar-usuario.html")

@app.route("/cad-usuario", methods=['POST'])
def insert_on_database(): # FIXME
    username = request.form['username']
    password = request.form['password']
    query = f"INSERT INTO joaovictor_tbusuario(username, senha) VALUES ('{username}','{password}')"
    meu_cursor.execute(query)
    conn.commit()

    return render_template('cadastrar-usuario.html', inseriu=True)


@app.route("/listar-usuarios", methods=['GET'])
def list_users():
    query = f"SELECT * FROM joaovictor_tbusuario"
    meu_cursor.execute(query)
    retorno = meu_cursor.fetchall()
    return render_template("listar-usuarios.html", users=retorno if retorno else None)

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login-post", methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT USERNAME, SENHA FROM joaovictor_tbusuario WHERE USERNAME = '{username}' AND SENHA = '{password}'"
    meu_cursor.execute(query)
    retorno = meu_cursor.fetchall() # Pegar o conteúdo da query
    # print(meu_cursor.rowcount) # Método alternativo de verificação: row count retorna 0 se não encontrou nada, se encontrou algo, retorna 1.
    if retorno:
        return "Deu certo"
    else:
        return "Você não possui cadastro no sistema"

app.run(debug=True)