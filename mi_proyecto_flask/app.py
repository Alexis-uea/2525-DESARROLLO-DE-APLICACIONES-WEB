# app.py – Aplicación Flask con conexión directa a MySQL (sin SQLAlchemy)

from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import conexion, cerrar_conexion
from forms import ProductoForm
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import Usuario
import mysql.connector
from flask import session


# -------------------- CONFIGURACIÓN GENERAL --------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # Cambia esto en producción por una clave segura

# -------------------- FLASK-LOGIN --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Página de login si el usuario no está autenticado

# Cargar usuario desde la base de datos
@login_manager.user_loader
def load_user(user_id):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, password, rol FROM usuarios WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cerrar_conexion(conn)
    if usuario:
        return Usuario(*usuario)
    return None

# Inyectar fecha actual en los templates (opcional)
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# -------------------- RUTAS PÚBLICAS --------------------

@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

# -------------------- CRUD DE PRODUCTOS --------------------

@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE %s", (f"%{q}%",))
    else:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
    productos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('products/list.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if not current_user.es_admin():
        flash("Solo administradores pueden crear productos.", "danger")
        return redirect(url_for('listar_productos'))

    form = ProductoForm()
    if form.validate_on_submit():
        conn = conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                (form.nombre.data, form.cantidad.data, float(form.precio.data))
            )
            conn.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('Error al guardar: ' + str(e))
        finally:
            cerrar_conexion(conn)
    return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear')

@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(pid):
    if not current_user.es_admin():
        flash("Solo administradores pueden editar productos.", "danger")
        return redirect(url_for('listar_productos'))

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE id = %s", (pid,))
    prod = cursor.fetchone()
    if not prod:
        cerrar_conexion(conn)
        return "Producto no encontrado", 404

    form = ProductoForm(data={'nombre': prod[1], 'cantidad': prod[2], 'precio': prod[3]})
    if form.validate_on_submit():
        try:
            cursor.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s",
                           (form.nombre.data, form.cantidad.data, form.precio.data, pid))
            conn.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('Error al actualizar: ' + str(e))
        finally:
            cerrar_conexion(conn)
    cerrar_conexion(conn)
    return render_template('products/form.html', title='Editar producto', form=form, modo='editar', pid=pid)

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(pid):
    if not current_user.es_admin():
        flash("Solo administradores pueden eliminar productos.", "danger")
        return redirect(url_for('listar_productos'))

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (pid,))
    if cursor.rowcount > 0:
        conn.commit()
        flash('Producto eliminado correctamente.', 'success')
    else:
        flash('Producto no encontrado.', 'warning')
    cerrar_conexion(conn)
    return redirect(url_for('listar_productos'))

# -------------------- FUNCIONES DE COMPRA --------------------

@app.route('/productos/<int:pid>/comprar', methods=['POST'])
@login_required
def comprar_producto(pid):
    if current_user.es_admin():
        flash('Los administradores no pueden comprar productos.', 'warning')
        return redirect(url_for('listar_productos'))

    try:
        cantidad = int(request.form.get('cantidad', 1))
        if cantidad < 1:
            raise ValueError
    except ValueError:
        flash('Cantidad inválida.', 'danger')
        return redirect(url_for('listar_productos'))

    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, cantidad AS disponible FROM productos WHERE id = %s", (pid,))
    producto = cursor.fetchone()

    if not producto:
        cerrar_conexion(conn)
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))

    if producto['disponible'] < cantidad:
        cerrar_conexion(conn)
        flash(f'Solo quedan {producto["disponible"]} unidades.', 'warning')
        return redirect(url_for('listar_productos'))

    try:
        cursor.execute(
            "INSERT INTO compras (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)",
            (current_user.id, pid, cantidad)
        )
        cursor.execute(
            "UPDATE productos SET cantidad = cantidad - %s WHERE id = %s",
            (cantidad, pid)
        )
        conn.commit()
        flash(f'Compra realizada: {cantidad} unidad(es) de "{producto["nombre"]}".', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al registrar la compra: {str(e)}', 'danger')
    finally:
        cerrar_conexion(conn)

    return redirect(url_for('listar_productos'))

@app.route('/mis-compras')
@login_required
def mis_compras():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, p.nombre AS producto, c.cantidad, c.fecha
        FROM compras c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
        ORDER BY c.fecha DESC
    """, (current_user.id,))
    compras = cursor.fetchall()
    cerrar_conexion(conn)
    return render_template('compras/mis_compras.html', compras=compras)

# -------------------- DASHBOARD --------------------

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.es_admin():
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM compras")
        total_compras = cursor.fetchone()[0]

        cerrar_conexion(conn)

        return render_template('dashboard.html',
                               nombre=current_user.nombre,
                               es_admin=True,
                               total_productos=total_productos,
                               total_usuarios=total_usuarios,
                               total_compras=total_compras)

    # Usuario normal
    return render_template('dashboard.html',
                           nombre=current_user.nombre,
                           es_admin=False)

# -------------------- AUTENTICACIÓN --------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, email, password, rol FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cerrar_conexion(conn)

        if usuario and check_password_hash(usuario[3], password):
            user = Usuario(*usuario)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
                           (nombre, email, password, 'user'))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cerrar_conexion(conn)

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#carrito de compras
# Añadir producto al carrito
@app.route('/agregar_al_carrito/<int:pid>', methods=['POST'])
@login_required
def agregar_al_carrito(pid):
    try:
        cantidad = int(request.form.get('cantidad', 1))
        if cantidad < 1:
            raise ValueError
    except ValueError:
        flash('Cantidad inválida.', 'danger')
        return redirect(url_for('listar_productos'))

    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, precio, cantidad FROM productos WHERE id = %s", (pid,))
    producto = cursor.fetchone()
    cerrar_conexion(conn)

    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))

    if producto['cantidad'] < cantidad:
        flash(f'Solo quedan {producto["cantidad"]} unidades disponibles.', 'warning')
        return redirect(url_for('listar_productos'))

    carrito = session.get('carrito', {})

    if str(pid) in carrito:
        carrito[str(pid)]['cantidad'] += cantidad
    else:
        carrito[str(pid)] = {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': float(producto['precio']),
            'cantidad': cantidad
        }

    session['carrito'] = carrito
    flash(f'Se agregaron {cantidad} unidad(es) de "{producto["nombre"]}" al carrito.', 'success')
    return redirect(url_for('listar_productos'))


# Mostrar carrito
@app.route('/carrito')
@login_required
def carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('carrito.html', carrito=carrito, total=total)


# Eliminar producto del carrito
@app.route('/carrito/eliminar/<int:producto_id>')
@login_required
def eliminar(producto_id):
    carrito = session.get('carrito', {})
    pid = str(producto_id)
    if pid in carrito:
        carrito.pop(pid)
        session['carrito'] = carrito
        flash('Producto eliminado del carrito.', 'success')
    else:
        flash('Producto no encontrado en el carrito.', 'warning')
    return redirect(url_for('carrito'))


# Vaciar carrito
@app.route('/carrito/vaciar')
@login_required
def vaciar():
    session['carrito'] = {}
    flash('Carrito vaciado.', 'success')
    return redirect(url_for('carrito'))

@app.route('/carrito/comprar', methods=['POST'])
@login_required
def comprar_carrito():
    if current_user.es_admin():
        flash('Los administradores no pueden comprar productos.', 'warning')
        return redirect(url_for('listar_productos'))

    carrito = session.get('carrito', {})
    if not carrito:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('carrito'))

    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # Validar disponibilidad de cada producto antes de comprar
    for pid_str, item in carrito.items():
        pid = int(pid_str)
        cursor.execute("SELECT cantidad FROM productos WHERE id = %s", (pid,))
        producto_db = cursor.fetchone()
        if not producto_db:
            cerrar_conexion(conn)
            flash(f'El producto "{item["nombre"]}" no existe.', 'danger')
            return redirect(url_for('carrito'))
        if producto_db['cantidad'] < item['cantidad']:
            cerrar_conexion(conn)
            flash(f'Solo quedan {producto_db["cantidad"]} unidades disponibles de "{item["nombre"]}".', 'warning')
            return redirect(url_for('carrito'))

    # Si todo está ok, insertar compras y actualizar inventario
    try:
        for pid_str, item in carrito.items():
            pid = int(pid_str)
            cantidad = item['cantidad']

            cursor.execute(
                "INSERT INTO compras (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)",
                (current_user.id, pid, cantidad)
            )
            cursor.execute(
                "UPDATE productos SET cantidad = cantidad - %s WHERE id = %s",
                (cantidad, pid)
            )
        conn.commit()
        session['carrito'] = {}  # Vaciar carrito al completar compra
        flash('Compra realizada con éxito.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al realizar la compra: {str(e)}', 'danger')
    finally:
        cerrar_conexion(conn)

    return redirect(url_for('listar_productos'))


# -------------------- MAIN --------------------

if __name__ == '__main__':
    app.run(debug=True)
# -------------------- FIN DEL CÓDIGO --------------------