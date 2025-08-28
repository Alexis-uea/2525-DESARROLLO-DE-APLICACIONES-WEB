import sqlite3
from producto import Producto

class Inventario:
    def __init__(self, db_name='inventario.db'):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Diccionario en memoria para manejar productos
        self.productos = {}

        # Crear tabla si no existe y cargar productos
        self.crear_tabla()
        self.cargar_productos()

    # Crear tabla de productos si aún no existe
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

    # Cargar productos existentes desde la base de datos
    def cargar_productos(self):
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    # Agregar nuevo producto a la base de datos y memoria
    def agregar_producto(self, producto):
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (
            producto.codigo,
            producto.nombre,
            producto.cantidad,
            float(producto.precio)  # Convertimos Decimal a float para evitar error con SQLite
        ))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Actualizar un producto existente
    def actualizar_producto(self, producto):
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (
            producto.nombre,
            producto.cantidad,
            float(producto.precio),  # También convertimos aquí
            producto.codigo
        ))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Eliminar producto de la base de datos y memoria
    def eliminar_producto(self, codigo):
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    # Obtener todos los productos en lista
    def obtener_productos(self):
        return list(self.productos.values())

    # Buscar productos por nombre (ignorando mayúsculas/minúsculas)
    def buscar_por_nombre(self, nombre_busqueda):
        return [
            producto for producto in self.productos.values()
            if nombre_busqueda.lower() in producto.nombre.lower()
        ]
