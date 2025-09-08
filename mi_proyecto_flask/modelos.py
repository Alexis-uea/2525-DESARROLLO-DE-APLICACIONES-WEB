from flask_sqlalchemy import SQLAlchemy

# Inicializa la extensión SQLAlchemy para usarla en toda la app
db = SQLAlchemy()


# -------------------------------------------------------
# Modelo: Producto
# Representa un producto del inventario
# -------------------------------------------------------

class Producto(db.Model):
    __tablename__ = 'productos'  # Nombre explícito de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    nombre = db.Column(db.String(120), unique=True, nullable=False)  # Nombre del producto (único)
    cantidad = db.Column(db.Integer, nullable=False, default=0)  # Stock disponible
    precio = db.Column(db.Float, nullable=False, default=0.0)  # Precio unitario

    def __repr__(self):
        """Representación legible del objeto para debugging."""
        return f'<Producto {self.id} {self.nombre}>'

    def to_tuple(self):
        """Devuelve una tupla con los datos del producto."""
        return (self.id, self.nombre, self.cantidad, self.precio)

    def to_dict(self):
        """Devuelve un diccionario con los datos del producto."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }


# -------------------------------------------------------
# Modelo: Cliente
# Representa un cliente que realiza compras
# -------------------------------------------------------

class Cliente(db.Model):
    __tablename__ = 'clientes'  # Nombre explícito de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    nombre = db.Column(db.String(120), nullable=False)  # Nombre del cliente
    direccion = db.Column(db.String(200), nullable=False)  # Dirección postal
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)  # Email (único)

    def __repr__(self):
        """Representación legible del objeto para debugging."""
        return f'<Cliente {self.id} {self.nombre}>'

    def to_tuple(self):
        """Devuelve una tupla con los datos del cliente."""
        return (self.id, self.nombre, self.direccion, self.correo_electronico)

    def to_dict(self):
        """Devuelve un diccionario con los datos del cliente."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'correo_electronico': self.correo_electronico
        }
