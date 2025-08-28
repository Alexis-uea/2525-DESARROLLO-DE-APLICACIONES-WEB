# Clase que representa un producto
class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo        # Código único
        self.nombre = nombre        # Nombre del producto
        self.cantidad = cantidad    # Cantidad disponible
        self.precio = precio        # Precio unitario
