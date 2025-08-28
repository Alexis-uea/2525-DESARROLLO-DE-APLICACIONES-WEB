import sqlite3
from producto import Producto  # Importamos la clase Producto para crear objetos producto

class Inventario:
    def __init__(self, db_name='inventario.db'):
        """
        Inicializa la conexión a la base de datos SQLite y carga los productos en memoria.
        """
        # Conectarse a la base de datos SQLite. check_same_thread=False permite usar en diferentes hilos (Flask).
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.productos = {}  # Diccionario para almacenar productos en memoria, clave = código
        
        self.crear_tabla()    # Crear tabla si no existe
        self.cargar_productos()  # Cargar productos existentes desde la base de datos

    def crear_tabla(self):
        """
        Crea la tabla 'producto' si no existe.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS producto (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()  # Guardar cambios en la base de datos

    def cargar_productos(self):
        """
        Carga todos los productos de la base de datos a memoria (diccionario).
        """
        self.cursor.execute('SELECT * FROM producto')
        for codigo, nombre, cantidad, precio in self.cursor.fetchall():
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    def agregar_producto(self, producto):
        """
        Inserta un nuevo producto en la base de datos y lo agrega al diccionario en memoria.
        """
        self.cursor.execute('''
            INSERT INTO producto (codigo, nombre, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        
        # Agregar a memoria
        self.productos[producto.codigo] = producto

    def actualizar_producto(self, producto):
        """
        Actualiza los datos de un producto existente en la base de datos y memoria.
        """
        self.cursor.execute('''
            UPDATE producto
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        
        # Actualizar en memoria
        self.productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        """
        Elimina un producto por código tanto en la base de datos como en memoria.
        """
        self.cursor.execute('DELETE FROM producto WHERE codigo = ?', (codigo,))
        self.conn.commit()
        
        # Eliminar de memoria
        self.productos.pop(codigo, None)

    def obtener_productos(self):
        """
        Devuelve una lista con todos los productos en memoria.
        """
        return list(self.productos.values())

    def buscar_por_nombre(self, nombre_busqueda):
        """
        Busca productos cuyo nombre contenga la cadena 'nombre_busqueda' (case insensitive).
        """
        return [
            producto for producto in self.productos.values()
            if nombre_busqueda.lower() in producto.nombre.lower()
        ]
