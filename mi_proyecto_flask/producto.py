# Clase que representa un producto del inventario
class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo        # Código único
        self.nombre = nombre        # Nombre del producto
        self.cantidad = cantidad    # Unidades disponibles
        self.precio = precio        # Precio por unidad
