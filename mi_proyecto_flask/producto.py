# producto.py

class Producto:
    """
    Clase que representa un producto en el inventario.
    Contiene atributos básicos como código (ID), nombre, cantidad y precio.
    """

    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo      # ID único del producto
        self.nombre = nombre      # Nombre del producto
        self.cantidad = cantidad  # Cantidad disponible en inventario
        self.precio = precio      # Precio unitario del producto
