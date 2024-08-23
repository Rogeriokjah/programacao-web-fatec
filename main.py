from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contato')
def contact():
    return render_template("contact.html")

@app.route('/servicos')
def services():
    return render_template("services.html")

@app.route('/sobre')
def about():
    return render_template("about.html")

app.run(debug=True)