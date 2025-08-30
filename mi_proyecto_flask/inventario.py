import sqlite3
from producto import Producto

class Inventario:
    """
    Clase para gestionar el inventario de Amazonía Market
    Maneja persistencia en base de datos SQLite y operaciones CRUD
    """
    
    def __init__(self, db_name='amazonia_market.db'):
        """
        Inicializa la conexión con la base de datos y carga productos en memoria
        
        Args:
            db_name (str): Nombre del archivo de base de datos SQLite
        """
        # Conexión a SQLite con soporte para múltiples hilos (necesario para Flask)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.productos = {}  # Diccionario en memoria para rápido acceso
        
        self.crear_tabla()      # Crear tabla si no existe
        self.cargar_productos() # Cargar productos desde BD a memoria

    def crear_tabla(self):
        """Crea la tabla de productos en la base de datos si no existe"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                codigo TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def cargar_productos(self):
        """Carga todos los productos desde la base de datos a memoria"""
        self.cursor.execute('SELECT * FROM productos')
        for fila in self.cursor.fetchall():
            codigo, nombre, cantidad, precio = fila
            self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)

    def agregar_producto(self, producto):
        """
        Agrega un nuevo producto a la base de datos y al inventario en memoria
        
        Args:
            producto (Producto): Objeto Producto a agregar
        """
        try:
            self.cursor.execute('''
                INSERT INTO productos (codigo, nombre, cantidad, precio)
                VALUES (?, ?, ?, ?)
            ''', (producto.codigo, producto.nombre, producto.cantidad, producto.precio))
            self.conn.commit()
            self.productos[producto.codigo] = producto
        except sqlite3.IntegrityError:
            raise ValueError("El código de producto ya existe")

    def actualizar_producto(self, producto):
        """
        Actualiza un producto existente en la base de datos y memoria
        
        Args:
            producto (Producto): Producto con datos actualizados
        """
        self.cursor.execute('''
            UPDATE productos 
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE codigo = ?
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.codigo))
        self.conn.commit()
        self.productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        """
        Elimina un producto por su código
        
        Args:
            codigo (str): Código del producto a eliminar
        """
        self.cursor.execute('DELETE FROM productos WHERE codigo = ?', (codigo,))
        self.conn.commit()
        self.productos.pop(codigo, None)

    def obtener_productos(self):
        """
        Retorna lista de todos los productos en el inventario
        
        Returns:
            list: Lista de objetos Producto
        """
        return list(self.productos.values())

    def buscar_por_nombre(self, nombre_busqueda):
        """
        Busca productos cuyo nombre contenga el texto especificado (case insensitive)
        
        Args:
            nombre_busqueda (str): Texto a buscar en los nombres
            
        Returns:
            list: Lista de productos que coinciden con la búsqueda
        """
        return [
            producto for producto in self.productos.values()
            if nombre_busqueda.lower() in producto.nombre.lower()
        ]

    def __del__(self):
        """Cierra la conexión a la base de datos cuando el objeto es destruido"""
        self.conn.close()