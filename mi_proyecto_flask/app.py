from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect  # Protección CSRF para formularios
from forms import ProductoForm, EditarProductoForm  # Formularios con Flask-WTF
from inventario import Inventario
from producto import Producto

# Crear aplicación Flask
app = Flask(__name__)
# Clave secreta requerida por Flask-WTF para proteger los formularios
app.config['SECRET_KEY'] = 'clave-super-secreta-123'
# Habilitar protección CSRF en toda la app
csrf = CSRFProtect(app)

# Instancia del inventario
inventario = Inventario()

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# Página "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')

# Página del inventario, permite buscar o ver todos los productos
@app.route('/inventario', methods=['GET', 'POST'])
def mostrar_inventario():
    if request.method == 'POST':
        # Búsqueda por nombre
        nombre = request.form.get('nombre', '')
        productos = inventario.buscar_por_nombre(nombre)
    else:
        productos = inventario.obtener_productos()

    return render_template('inventario.html', title='Inventario', productos=productos)

# Agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm()  # Crear formulario

    if form.validate_on_submit():  # Validación con Flask-WTF
        nuevo_producto = Producto(
            codigo=form.codigo.data,
            nombre=form.nombre.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data
        )
        inventario.agregar_producto(nuevo_producto)
        return redirect(url_for('mostrar_inventario'))

    return render_template('agregar_producto.html', title='Agregar Producto', form=form)

# Editar un producto existente
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    producto = inventario.productos.get(codigo)
    if not producto:
        return "Producto no encontrado", 404

    form = EditarProductoForm(obj=producto)  # Cargar datos en el formulario

    if form.validate_on_submit():  # Validación y guardar cambios
        producto.nombre = form.nombre.data
        producto.cantidad = form.cantidad.data
        producto.precio = form.precio.data
        inventario.actualizar_producto(producto)
        return redirect(url_for('mostrar_inventario'))

    return render_template('editar_producto.html', title='Editar Producto', form=form, producto=producto)

# Eliminar producto con método POST (con CSRF)
@app.route('/eliminar/<codigo>', methods=['POST'])
def eliminar_producto(codigo):
    inventario.eliminar_producto(codigo)
    return redirect(url_for('mostrar_inventario'))

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
