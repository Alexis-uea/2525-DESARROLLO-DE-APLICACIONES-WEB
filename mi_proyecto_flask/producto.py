class Producto:
    """
    Clase que representa un producto de Amazonía Market
    Contiene toda la información de un producto del supermercado
    """
    
    def __init__(self, codigo, nombre, cantidad, precio):
        """
        Inicializa un nuevo producto
        
        Args:
            codigo (str): Código único identificador (SKU)
            nombre (str): Nombre descriptivo del producto
            cantidad (int): Stock disponible
            precio (float): Precio de venta al público
        """
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        """
        Representación string del producto para debugging
        """
        return (f"<Producto {self.codigo} - {self.nombre} - "
                f"Stock: {self.cantidad} - Precio: ${self.precio:.2f}>")