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
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("cadastrar-usuario.html")


@app.route("/cadastrar-usuario", methods=['POST'])
def cadastrar():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Inserindo no BD:
        query = "INSERT INTO joaovictor_tbusuario (nome, email, senha) VALUES (%s, %s, %s)"
        valores = (name, email, password)
        meu_cursor.execute(query, valores)
        conn.commit() # Commitando o insert no banco de dados
        return redirect(url_for('index'))


app.run(debug=True)