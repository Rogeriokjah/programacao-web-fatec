from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # Devido ao decorador, a função abaixo será executada automaticamente ao chegar nesta rota.
def home():
    return render_template("index.html", variavel="Oieeee", subtitulo="Variável no Jinja") # render_template pega arquivos da pasta "templates"

@app.route('/page2')
def page2():
    return render_template("page2.html", user="João", happy=True, num=20)


app.run(debug=True) # ao definir debug como True, a aplicação será recarregada sempre que uma alteração ocorrer