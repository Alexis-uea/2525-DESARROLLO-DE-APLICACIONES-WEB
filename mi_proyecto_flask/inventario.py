# inventario.py
import sqlite3
from producto import Producto

class Inventario:
    """
    Clase para manejar el inventario usando colecciones y SQLite.
    Almacena productos en un diccionario para acceso rápido y persistencia en DB.
    """

    def __init__(self, db_name='inventario.db'):
        # Conexión a la base de datos SQLite
        # check_same_thread=False permite acceso a la BD desde diferentes threads (por Flask)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Diccionario para almacenar productos en memoria {codigo: Producto}
        self.productos = {}

        # Crear tabla en la BD si no existe
        self.crear_tabla()

        # Cargar productos existentes desde la BD al diccionario
        self.cargar_productos()

    def crear_tabla(self):
        """Crea la tabla 'producto' si no existe en la base de datos."""
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
        """
        Carga todos los productos guardados en la base de datos al diccionario.
        Esto permite acceso rápido y uso de colecciones para la gestión.
        """
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    def agregar_producto(self, producto):
        """
        Añade un nuevo producto tanto a la base de datos como al diccionario local.
        Parámetros:
            producto (Producto): objeto Producto a añadir.
        """
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()

        # Añadir al diccionario local para acceso rápido
        self.productos[producto.codigo] = producto

    def obtener_productos(self):
        """
        Devuelve una lista con todos los productos almacenados en el inventario.
        """
        return list(self.productos.values())
