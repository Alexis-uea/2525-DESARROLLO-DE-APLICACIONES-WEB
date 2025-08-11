from flask import Flask

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return '¡Hola! Esta es la página principal.'

# Ruta dinámica para mostrar mensaje personalizado
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'¡Hola, {nombre}! Bienvenido a la página.'

if __name__ == '__main__':
    
     # Ejecuta la aplicación en el puerto 5000
    app.run(debug=True)