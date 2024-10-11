from flask import Flask, render_template, request
from dotenv import load_dotenv
import mysql.connector # pip install mysql-connector-python
import os

load_dotenv() # Pegando variáveis de ambiente
app = Flask(__name__)

# Testando conexão com o banco de dados
try:
    conn = mysql.connector.connect(
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        database=os.getenv('MYSQL_DATABASE')
    )
except:
    print("Ocorreu um erro ao se conectar com o banco de dados.")
if conn and conn.is_connected():
    with conn.cursor() as cursor:
        result = cursor.execute("SELECT * FROM joaovictor_tbusuario;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    conn.close()

# Rota Principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        return render_template("cadastrar-usuario.html")
    return render_template("cadastrar-usuario.html")


app.run(debug=True)