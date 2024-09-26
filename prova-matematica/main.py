from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculo2grau", methods=["GET", "POST"])
def equacao():
    if request.method=="POST": # Se checar o método, dá pra ter calculo e pagina em branco numa rota só (mas só quando for post mesmo)
        a = int(request.form["a"])
        b = int(request.form["b"])
        c = int(request.form["c"])
        delta = b**2 - 4*a*c
        x1 = (- b + delta**0.5) / (2*a)
        x2 = (- b - delta**0.5) / (2*a)
        return render_template("equacao.html", x1=x1, x2=x2) # Se o método é post, vai fazer o cálculo e passar as variáveis...
    
    return render_template("equacao.html")


@app.route("/fahrenheit", methods=["GET"])
def fahrenheit():
    return render_template("fahrenheit.html")

@app.route("/calc_fahrenheit")
def calc_fahrenheit():
    args = request.args
    celsius = int(args.get("celsius"))
    fhrt = (celsius * 9/5) + 32
    return render_template("calc_fahrenheit.html", fhrt=fhrt)


app.run(debug=True)