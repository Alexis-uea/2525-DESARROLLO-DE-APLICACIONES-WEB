import sqlite3
from producto import Producto

class Inventario:
    def __init__(self, db_name='inventario.db'):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Diccionario para tener acceso rápido a los productos en memoria
        self.productos = {}

        # Crear tabla si no existe
        self.crear_tabla()

        # Cargar productos existentes desde la base de datos
        self.cargar_productos()

    def crear_tabla(self):
        # Crear tabla producto si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS producto (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def cargar_productos(self):
        # Cargar productos desde la base de datos al diccionario
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    def agregar_producto(self, producto):
        # Agregar producto a la base de datos y al diccionario
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    def actualizar_producto(self, producto):
        # Actualizar producto en la base de datos y en memoria
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        # Eliminar producto de la base de datos y del diccionario
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    def obtener_productos(self):
        # Devolver lista de productos para usar en las vistas
        return list(self.productos.values())
