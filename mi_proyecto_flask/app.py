from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect  # Para proteger los formularios con tokens CSRF
from forms import ProductoForm, EditarProductoForm  # Importamos los formularios
from inventario import Inventario
from producto import Producto

# Crear instancia de la app Flask
app = Flask(__name__)

# Clave secreta necesaria para proteger formularios con Flask-WTF
app.config['SECRET_KEY'] = 'clave-super-secreta-123'

# Inicializar CSRFProtect para proteger toda la app contra ataques CSRF
csrf = CSRFProtect(app)

# Instancia de Inventario para manipular la base de datos
inventario = Inventario()

# Página principal
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# Página Acerca de
@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')

# Mostrar inventario y buscar productos
@app.route('/inventario', methods=['GET', 'POST'])
def mostrar_inventario():
    form = ProductoForm()  # Creamos un formulario para la búsqueda (aunque no se use directamente)
    productos = []

    if request.method == 'POST':
        # Obtener el nombre ingresado para buscar
        nombre_busqueda = request.form.get('nombre', '').strip()

        # Validar que el campo no esté vacío y buscar
        if nombre_busqueda:
            productos = inventario.buscar_por_nombre(nombre_busqueda)
        else:
            productos = inventario.obtener_productos()
    else:
        productos = inventario.obtener_productos()

    # Renderizar plantilla con lista de productos y el formulario para CSRF token
    return render_template('inventario.html', title='Inventario', productos=productos, form=form)

# Agregar nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm()

    # Validar el formulario cuando se envía
    if form.validate_on_submit():
        # Crear nuevo producto con datos del formulario
        nuevo_producto = Producto(
            codigo=form.codigo.data.strip(),
            nombre=form.nombre.data.strip(),
            cantidad=form.cantidad.data,
            precio=float(form.precio.data)  # Convertir Decimal a float para SQLite
        )
        inventario.agregar_producto(nuevo_producto)

        # Redirigir a la página del inventario
        return redirect(url_for('mostrar_inventario'))

    # Mostrar formulario para agregar
    return render_template('agregar_producto.html', title='Agregar Producto', form=form)

# Editar producto existente
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    producto = inventario.productos.get(codigo)
    if not producto:
        return "Producto no encontrado", 404

    # Rellenar formulario con datos actuales del producto
    form = EditarProductoForm(obj=producto)

    if form.validate_on_submit():
        # Actualizar atributos del producto con datos del formulario
        producto.nombre = form.nombre.data.strip()
        producto.cantidad = form.cantidad.data
        producto.precio = float(form.precio.data)

        # Guardar cambios en la base de datos
        inventario.actualizar_producto(producto)

        # Redirigir al inventario
        return redirect(url_for('mostrar_inventario'))

    # Mostrar formulario con datos para editar
    return render_template('editar_producto.html', title='Editar Producto', form=form, producto=producto)

# Eliminar producto (POST con CSRF)
@app.route('/eliminar/<codigo>', methods=['POST'])
def eliminar_producto(codigo):
    inventario.eliminar_producto(codigo)
    return redirect(url_for('mostrar_inventario'))

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
