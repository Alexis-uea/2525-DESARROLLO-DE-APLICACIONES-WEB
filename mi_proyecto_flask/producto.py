class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        """
        Inicializa un objeto Producto.

        :param codigo: Código único del producto (string)
        :param nombre: Nombre del producto (string)
        :param cantidad: Cantidad disponible (int)
        :param precio: Precio unitario (float)
        """
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        """
        Representación del objeto Producto para facilitar depuración.
        """
        return f"<Producto {self.codigo} - {self.nombre} - Cantidad: {self.cantidad} - Precio: {self.precio:.2f}>"
