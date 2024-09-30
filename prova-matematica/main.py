from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route("/")
def index():
    return render_template("indexCalc.html")  # Adjust this if you have a main homepage

# Route for triangle calculation (GET)
@app.route("/calculo_triangulo", methods=["GET"])
def calcular_triangulo():
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    c = request.args.get("c", type=int)

    triangle_type = None
    if a and b and c:
        if a == b == c:
            triangle_type = 'Equilátero'
        elif a == b or b == c or a == c:
            triangle_type = 'Isósceles'
        else:
            triangle_type = 'Escaleno'

    return render_template("calculo_triangulo.html", triangle_type=triangle_type)

# Route for média de notas calculation (POST)
@app.route("/calc_media_notas", methods=["POST"])
def calcular_media():
    nota1 = request.form.get("nota1", type=float)
    nota2 = request.form.get("nota2", type=float)
    nota3 = request.form.get("nota3", type=float)
    nota4 = request.form.get("nota4", type=float)

    media = None
    if nota1 and nota2 and nota3 and nota4:
        media = (nota1 + nota2 + nota3 + nota4) / 4

    return render_template("calc_media_notas.html", media=media)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
