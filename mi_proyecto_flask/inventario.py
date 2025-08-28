import sqlite3
from producto import Producto

# Clase que gestiona productos en memoria y en base de datos
class Inventario:
    def __init__(self, db_name='inventario.db'):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Diccionario de productos en memoria
        self.productos = {}

        self.crear_tabla()
        self.cargar_productos()

    # Crea la tabla si no existe
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

    # Carga productos de la base de datos al diccionario
    def cargar_productos(self):
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    # Agrega un producto nuevo
    def agregar_producto(self, producto):
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Actualiza un producto existente
    def actualizar_producto(self, producto):
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    # Elimina un producto
    def eliminar_producto(self, codigo):
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    # Devuelve todos los productos
    def obtener_productos(self):
        return list(self.productos.values())

    # Busca productos por nombre parcial (sin distinguir mayúsculas)
    def buscar_por_nombre(self, nombre_busqueda):
        return [
            producto for producto in self.productos.values()
            if nombre_busqueda.lower() in producto.nombre.lower()
        ]
