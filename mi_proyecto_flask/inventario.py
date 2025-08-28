import sqlite3
from producto import Producto

class Inventario:
    def __init__(self, db_name='inventario.db'):
        # Conectarse a la base de datos SQLite
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.productos = {}  # Diccionario en memoria
        self.crear_tabla()
        self.cargar_productos()

    # Crear tabla si no existe
    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS producto (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    # Cargar productos desde la base de datos
    def cargar_productos(self):
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    # Agregar producto nuevo
    def agregar_producto(self, producto):
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Actualizar datos de un producto
    def actualizar_producto(self, producto):
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Eliminar producto
    def eliminar_producto(self, codigo):
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    # Obtener todos los productos
    def obtener_productos(self):
        return list(self.productos.values())

    # Buscar productos por nombre (insensible a mayúsculas)
    def buscar_por_nombre(self, nombre_busqueda):
        return [
            producto for producto in self.productos.values()
            if nombre_busqueda.lower() in producto.nombre.lower()
        ]
