from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import datetime
from modelos import db, Producto, Cliente
from formularios import ProductoForm, ClienteForm
from inventario import Inventario
from persistencia import (
    guardar_productos_txt, leer_productos_txt,
    guardar_productos_json, leer_productos_json,
    guardar_productos_csv, leer_productos_csv
)
from sqlalchemy.exc import IntegrityError
import os

# ---------------------------------------------
# Configuración de la aplicación Flask
# ---------------------------------------------

app = Flask(__name__)

# Define la ruta base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuración de la base de datos SQLite en la carpeta 'instance'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'inventario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave secreta para formularios y sesiones (¡cambiar en producción!)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Inicializa SQLAlchemy con la app
db.init_app(app)

# Context processor para tener acceso a la hora actual en los templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Crea las tablas y carga inventario desde BD al iniciar
with app.app_context():
    db.create_all()
    inventario = Inventario.cargar_desde_bd()


# ---------------------------------------------
# Rutas de la aplicación
# ---------------------------------------------

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# Página con opciones para leer/guardar archivos
@app.route('/leer-datos')
def leer_datos():
    return render_template('leer_datos.html', title='Leer datos')

# Página de bienvenida simple
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

# Página "Acerca de"
@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')


# ---------------------------------------------
# Gestión de Productos
# ---------------------------------------------

@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    productos = inventario.buscar_por_nombre(q) if q else inventario.listar_todos()
    return render_template('productos/lista.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        try:
            inventario.agregar(
                nombre=form.nombre.data.strip(),
                cantidad=form.cantidad.data,
                precio=form.precio.data
            )
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except ValueError as e:
            form.nombre.errors.append(str(e))
    return render_template('productos/formulario.html', title='Nuevo producto', form=form, modo='crear')

@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
def editar_producto(pid):
    producto = Producto.query.get_or_404(pid)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        try:
            inventario.actualizar(
                id=pid,
                nombre=form.nombre.data.strip(),
                cantidad=form.cantidad.data,
                precio=form.precio.data
            )
            flash('Producto actualizado.', 'success')
            return redirect(url_for('listar_productos'))
        except ValueError as e:
            form.nombre.errors.append(str(e))
    return render_template('productos/formulario.html', title='Editar producto', form=form, modo='editar')

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
def eliminar_producto(pid):
    ok = inventario.eliminar(pid)
    flash('Producto eliminado.' if ok else 'Producto no encontrado.', 'info' if ok else 'warning')
    return redirect(url_for('listar_productos'))


# ---------------------------------------------
# Gestión de Clientes
# ---------------------------------------------

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template('clientes/lista.html', title='Clientes', clientes=clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def crear_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            nombre=form.nombre.data.strip(),
            direccion=form.direccion.data.strip(),
            correo_electronico=form.correo_electronico.data.strip()
        )
        db.session.add(nuevo_cliente)
        try:
            db.session.commit()
            flash('Cliente agregado correctamente.', 'success')
            return redirect(url_for('listar_clientes'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: el correo electrónico ya existe.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('clientes/formulario.html', title='Nuevo cliente', form=form, modo='crear')

@app.route('/clientes/<int:cid>/editar', methods=['GET', 'POST'])
def editar_cliente(cid):
    cliente = Cliente.query.get_or_404(cid)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nombre = form.nombre.data.strip()
        cliente.direccion = form.direccion.data.strip()
        cliente.correo_electronico = form.correo_electronico.data.strip()
        try:
            db.session.commit()
            flash('Cliente actualizado correctamente.', 'success')
            return redirect(url_for('listar_clientes'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: el correo electrónico ya existe.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error inesperado: {str(e)}', 'danger')
    return render_template('clientes/formulario.html', title='Editar cliente', form=form, modo='editar')


# ---------------------------------------------
# Guardar productos en archivos (TXT, JSON, CSV)
# ---------------------------------------------

@app.route('/productos/txt/guardar', methods=['POST'])
def guardar_txt():
    productos = [p.to_dict() for p in Producto.query.all()]
    guardar_productos_txt(productos)
    flash('Productos guardados en TXT', 'success')
    return redirect(url_for('listar_productos'))

@app.route('/productos/json/guardar', methods=['POST'])
def guardar_json():
    productos = [p.to_dict() for p in Producto.query.all()]
    guardar_productos_json(productos)
    flash('Productos guardados en JSON', 'success')
    return redirect(url_for('listar_productos'))

@app.route('/productos/csv/guardar', methods=['POST'])
def guardar_csv():
    productos = [p.to_dict() for p in Producto.query.all()]
    guardar_productos_csv(productos)
    flash('Productos guardados en CSV', 'success')
    return redirect(url_for('listar_productos'))


# ---------------------------------------------
# Mostrar contenido crudo de archivos
# ---------------------------------------------

def leer_archivo_como_html(ruta, tipo):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except FileNotFoundError:
        contenido = f"⚠️ Archivo {os.path.basename(ruta)} no encontrado."

    return f"""
    <html>
        <head>
            <title>Contenido {tipo.upper()}</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>📄 Contenido crudo desde archivo {tipo.upper()}</h1>
            <pre style="background:#f9f9f9; padding:1em; border:1px solid #ccc;">{contenido}</pre>
            <p><a href="{url_for('leer_datos')}">⬅️ Volver</a></p>
        </body>
    </html>
    """

@app.route('/productos/txt/cargar')
def cargar_txt():
    ruta = os.path.join(basedir, 'instance', 'productos.txt')
    return leer_archivo_como_html(ruta, 'txt')

@app.route('/productos/json/cargar')
def cargar_json():
    ruta = os.path.join(basedir, 'instance', 'productos.json')
    return leer_archivo_como_html(ruta, 'json')

@app.route('/productos/csv/cargar')
def cargar_csv():
    ruta = os.path.join(basedir, 'instance', 'productos.csv')
    return leer_archivo_como_html(ruta, 'csv')


# ---------------------------------------------
# Ejecutar la aplicación
# ---------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
# Nota: En producción, usar un servidor WSGI como Gunicorn o uWSGI