from flask import Flask, render_template, request, redirect, url_for
import os
import json
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ruta base absoluta para manejar archivos sin errores
basedir = os.path.abspath(os.path.dirname(__file__))

# Crear carpetas necesarias para almacenar datos y base de datos
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'datos'), exist_ok=True)

# Configuración base de datos SQLite (ruta absoluta)
db_path = os.path.join(basedir, 'database', 'usuarios.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Usuario para la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

# Crear tablas al iniciar la app
with app.app_context():
    db.create_all()

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Mostrar formulario para ingreso de datos
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

# Recibir datos del formulario y guardarlos en TXT, JSON, CSV y SQLite
@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():
    nombre = request.form['nombre']
    edad = request.form['edad']

    # Guardar en TXT
    txt_path = os.path.join(basedir, 'datos', 'datos.txt')
    with open(txt_path, 'a', encoding='utf-8') as f:
        f.write(f"{nombre},{edad}\n")

    # Guardar en JSON
    json_path = os.path.join(basedir, 'datos', 'datos.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                datos_json = json.load(f)
            except json.JSONDecodeError:
                datos_json = []
    else:
        datos_json = []

    datos_json.append({'nombre': nombre, 'edad': edad})
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(datos_json, f, indent=4, ensure_ascii=False)

    # Guardar en CSV
    csv_path = os.path.join(basedir, 'datos', 'datos.csv')
    write_header = not os.path.exists(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['nombre', 'edad'])
        writer.writerow([nombre, edad])

    # Guardar en SQLite
    usuario = Usuario(nombre=nombre, edad=int(edad))
    db.session.add(usuario)
    db.session.commit()

    # Redirigir a página de éxito sin datos (muestra mensaje)
    return redirect(url_for('resultado'))

# Mostrar mensaje de éxito tras guardar datos
@app.route('/resultado')
def resultado():
    return render_template('resultados.html', datos=None, tipo=None)

# Leer y mostrar datos desde TXT
@app.route('/leer_txt')
def leer_txt():
    txt_path = os.path.join(basedir, 'datos', 'datos.txt')
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            datos = f.readlines()
    except FileNotFoundError:
        datos = ["Archivo TXT no encontrado."]
    return render_template('resultados.html', datos=datos, tipo='TXT')

# Leer y mostrar datos desde JSON
@app.route('/leer_json')
def leer_json():
    json_path = os.path.join(basedir, 'datos', 'datos.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = [{"nombre": "Archivo JSON no encontrado o vacío.", "edad": ""}]
    return render_template('resultados.html', datos=datos, tipo='JSON')

# Leer y mostrar datos desde CSV
@app.route('/leer_csv')
def leer_csv():
    csv_path = os.path.join(basedir, 'datos', 'datos.csv')
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            datos = list(reader)
    except FileNotFoundError:
        datos = [["Archivo CSV no encontrado."]]
    return render_template('resultados.html', datos=datos, tipo='CSV')

# Leer y mostrar datos desde SQLite
@app.route('/leer_sqlite')
def leer_sqlite():
    usuarios = Usuario.query.all()
    return render_template('resultados.html', datos=usuarios, tipo='SQLite')

if __name__ == '__main__':
    app.run(debug=True)
