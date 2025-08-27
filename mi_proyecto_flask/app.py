from flask import Flask, render_template, request, redirect, url_for
from inventario import Inventario
from producto import Producto

# Crear instancia de la aplicación Flask
app = Flask(__name__)

# Crear instancia del inventario que maneja la base de datos y los productos
inventario = Inventario()

# Ruta de la página principal
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# Ruta de la página "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')

# Ruta que muestra la lista de productos del inventario y permite búsqueda
@app.route('/inventario', methods=['GET', 'POST'])
def mostrar_inventario():
    if request.method == 'POST':
        # Buscar productos por nombre (ignorando mayúsculas)
        nombre = request.form.get('nombre', '')
        productos = inventario.buscar_por_nombre(nombre)
    else:
        productos = inventario.obtener_productos()
    
    return render_template('inventario.html', title='Inventario', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        # Obtener datos del formulario
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        # Crear un nuevo producto y agregarlo al inventario
        nuevo_producto = Producto(codigo, nombre, cantidad, precio)
        inventario.agregar_producto(nuevo_producto)

        # Redirigir a la página del inventario
        return redirect(url_for('mostrar_inventario'))

    # Si es GET, mostrar el formulario
    return render_template('agregar_producto.html', title='Agregar Producto')

# Ruta para editar un producto existente
@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    producto = inventario.productos.get(codigo)

    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        # Actualizar datos desde formulario
        producto.nombre = request.form['nombre']
        producto.cantidad = int(request.form['cantidad'])
        producto.precio = float(request.form['precio'])

        # Guardar cambios en la base de datos
        inventario.actualizar_producto(producto)
        return redirect(url_for('mostrar_inventario'))

    return render_template('editar_producto.html', title='Editar Producto', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<codigo>', methods=['POST'])
def eliminar_producto(codigo):
    inventario.eliminar_producto(codigo)
    return redirect(url_for('mostrar_inventario'))

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
