# Importamos las funciones necesarias de Flask
from flask import Flask, render_template

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta principal del sitio ('/') que carga la página de inicio
@app.route('/')
def index():
    # Renderiza el archivo index.html, enviando el título como variable
    return render_template('index.html', title='Inicio')

# Ruta secundaria '/about' que carga la página "Acerca de"
@app.route('/about')
def about():
    # Renderiza el archivo about.html, enviando el título como variable
    return render_template('about.html', title='Acerca de')

# Llama a la función app.run() solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    # Ejecuta la aplicación en modo de depuración (útil para desarrollo)
    app.run(debug=True)
