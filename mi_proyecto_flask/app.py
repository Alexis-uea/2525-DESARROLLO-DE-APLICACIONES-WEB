from flask import Flask, render_template, request, redirect, url_for
from inventario import Inventario
from producto import Producto

app = Flask(__name__)

# Crear instancia del inventario (conecta y carga productos de SQLite)
inventario = Inventario()

@app.route('/')
def index():
    """Ruta de la página principal (inicio)."""
    return render_template('index.html', title='Inicio')

@app.route('/about')
def about():
    """Ruta de la página Acerca de."""
    return render_template('about.html', title='Acerca de')

@app.route('/inventario')
def mostrar_inventario():
    """
    Muestra todos los productos del inventario.
    Obtiene la lista de productos desde el objeto inventario.
    """
    productos = inventario.obtener_productos()
    return render_template('inventario.html', title='Inventario', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    """
    Ruta para agregar un nuevo producto.
    - Si es GET, muestra el formulario para ingresar datos.
    - Si es POST, procesa el formulario y agrega el producto al inventario.
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        # Crear un nuevo objeto Producto
        nuevo_producto = Producto(codigo, nombre, cantidad, precio)

        # Agregar el producto al inventario (y BD)
        inventario.agregar_producto(nuevo_producto)

        # Redirigir a la página del inventario para mostrar los productos
        return redirect(url_for('mostrar_inventario'))

    # Método GET: mostrar el formulario para agregar producto
    return render_template('agregar_producto.html', title='Agregar Producto')

if __name__ == '__main__':
    # Ejecutar app Flask en modo debug para desarrollo
    app.run(debug=True)
