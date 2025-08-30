from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from forms import ProductoForm, EditarProductoForm
from inventario import Inventario
from producto import Producto
import os

# Inicialización de la aplicación Flask para Amazonía Market
app = Flask(__name__)

# Configuración de clave secreta (en producción usar variables de entorno)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-amazonia-market-2025')

# Protección CSRF para toda la aplicación
csrf = CSRFProtect(app)

# Instancia del inventario (gestión de productos)
inventario = Inventario()

# Ruta principal - Página de inicio
@app.route('/')
def index():
    """Muestra la página principal de Amazonía Market"""
    return render_template('index.html', title='Inicio - Amazonía Market')

# Ruta Acerca de - Información del supermercado
@app.route('/about')
def about():
    """Muestra la página 'Acerca de' con información del supermercado"""
    return render_template('about.html', title='Acerca de - Amazonía Market')

# Ruta Inventario - Gestión de productos
@app.route('/inventario', methods=['GET', 'POST'])
def mostrar_inventario():
    """
    Muestra el inventario de productos con funcionalidad de búsqueda.
    POST: Busca productos por nombre
    GET: Muestra todos los productos
    """
    form = ProductoForm()  # Formulario para CSRF token
    productos = []

    if request.method == 'POST':
        # Búsqueda por nombre (case insensitive)
        nombre_busqueda = request.form.get('nombre', '').strip()
        if nombre_busqueda:
            productos = inventario.buscar_por_nombre(nombre_busqueda)
        else:
            productos = inventario.obtener_productos()
    else:
        productos = inventario.obtener_productos()

    return render_template('inventario.html', 
                         title='Inventario - Amazonía Market', 
                         productos=productos, 
                         form=form)

# Ruta Agregar Producto - Formulario de nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    """Maneja el formulario para agregar nuevos productos al inventario"""
    form = ProductoForm()

    if form.validate_on_submit():
        # Crear nuevo producto con datos del formulario
        nuevo_producto = Producto(
            codigo=form.codigo.data.strip(),
            nombre=form.nombre.data.strip(),
            cantidad=form.cantidad.data,
            precio=float(form.precio.data)
        )
        inventario.agregar_producto(nuevo_producto)
        return redirect(url_for('mostrar_inventario'))

    return render_template('agregar_producto.html', 
                         title='Agregar Producto - Amazonía Market', 
                         form=form)

# Ruta Editar Producto - Formulario de edición
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    """Maneja la edición de productos existentes"""
    producto = inventario.productos.get(codigo)
    if not producto:
        return "Producto no encontrado", 404

    form = EditarProductoForm(obj=producto)

    if form.validate_on_submit():
        # Actualizar producto con nuevos datos
        producto.nombre = form.nombre.data.strip()
        producto.cantidad = form.cantidad.data
        producto.precio = float(form.precio.data)
        inventario.actualizar_producto(producto)
        return redirect(url_for('mostrar_inventario'))

    return render_template('editar_producto.html', 
                         title='Editar Producto - Amazonía Market', 
                         form=form, 
                         producto=producto)

# Ruta Eliminar Producto - Eliminación segura (POST only)
@app.route('/eliminar/<codigo>', methods=['POST'])
def eliminar_producto(codigo):
    """Elimina un producto del inventario (solo por POST)"""
    inventario.eliminar_producto(codigo)
    return redirect(url_for('mostrar_inventario'))

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)