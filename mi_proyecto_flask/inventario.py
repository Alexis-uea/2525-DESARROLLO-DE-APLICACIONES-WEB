import sqlite3
from producto import Producto

class Inventario:
    """
    Clase que gestiona el inventario de productos.
    Utiliza SQLite para persistencia y un diccionario para acceso rápido.
    """

    def __init__(self, db_name='inventario.db'):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Diccionario para almacenar productos en memoria: {codigo: Producto}
        self.productos = {}

        # Crear tabla si no existe
        self.crear_tabla()

        # Cargar productos existentes desde la base de datos
        self.cargar_productos()

    def crear_tabla(self):
        """
        Crea la tabla 'producto' si no existe en la base de datos.
        """
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
        Carga productos desde la base de datos al diccionario en memoria.
        """
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    def agregar_producto(self, producto):
        """
        Agrega un nuevo producto al inventario y a la base de datos.
        """
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    def actualizar_producto(self, producto):
        """
        Actualiza un producto existente en la base de datos y en memoria.
        """
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        """
        Elimina un producto del inventario y de la base de datos usando su código.
        """
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    def obtener_productos(self):
        """
        Devuelve todos los productos almacenados en el inventario como lista.
        """
        return list(self.productos.values())

    def buscar_por_nombre(self, nombre_busqueda):
        """
        Busca productos cuyo nombre contenga el texto especificado (ignorando mayúsculas).
        Retorna una lista de coincidencias parciales.
        """
        resultado = []
        for producto in self.productos.values():
            if nombre_busqueda.lower() in producto.nombre.lower():
                resultado.append(producto)
        return resultado
