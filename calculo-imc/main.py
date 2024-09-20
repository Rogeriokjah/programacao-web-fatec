from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('imc.html')

@app.route('/calcular_imc_post', methods=['POST'])
def calcular_imc_post():
    altura = float(request.form['txt_altura'])
    peso = float(request.form['txt_peso'])
    imc = round(peso / (altura**2),2)
    if (imc < 18.5):
        classificado = 'Magreza'
    elif (imc >= 18.5 and imc <25):
        classificado = "Normal"
    elif (imc >= 25 and imc <30):
        classificado = 'Sobrepeso'
    elif(imc >=30 and imc < 40):
        classificado = "Obesidade"
    elif(imc >= 40):
        classificado = 'Balofo'
    return render_template('imc.html', imc=imc, classificado=classificado)

@app.route('/calcular_imc_get', methods=['GET']) # Get deixa os parametros expostos na URL. CUIDADO!
def calcular_imc_get():
    args = request.args
    altura = float(args.get('txt_altura'))
    peso = float(args.get('txt_peso'))
    imc = round(peso / (altura**2),2)
    return render_template('imc.html', imc=imc)

app.run(debug=True)