from flask import Flask

app = Flask(__name__)

@app.route('/') # Devido ao decorador, a função abaixo será executada automaticamente ao chegar nesta rota.
def route1():
    return "Rota principal"

@app.route('/rota')
def route2():
    return "Rota secundária"

app.run(debug=True)