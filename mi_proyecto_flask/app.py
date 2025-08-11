from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return '¡Hola! Esta es la página principal.'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'¡Hola, {nombre}! Bienvenido a la página.'

if __name__ == '__main__':
    app.run(debug=True)