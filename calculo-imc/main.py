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
        classificado = "Abaixo do peso"
        img_route = "./static/images/abaixoPeso.png"
    elif (imc >= 18.5 and imc < 25):
        classificado = "Normal"
        img_route = "./static/images/normal.png"
    elif (imc >= 25 and imc <30):
        classificado = "Acima do peso"
        img_route = "./static/images/acimapeso.png"
    elif(imc >=30 and imc < 40):
        classificado = "Sobre peso"
        img_route = "./static/images/sobrePeso.png"
    elif(imc >= 40):
        classificado = "Super obeso"
        img_route = "./static/images/obeso.png"
    return render_template('imc.html', imc=imc, classificado=classificado, img_route=img_route)

@app.route('/calcular_imc_get', methods=['GET']) # Get deixa os parametros expostos na URL. CUIDADO!
def calcular_imc_get():
    args = request.args
    altura = float(args.get('txt_altura'))
    peso = float(args.get('txt_peso'))
    imc = round(peso / (altura**2),2)
    return render_template('imc.html', imc=imc)

app.run(debug=True)