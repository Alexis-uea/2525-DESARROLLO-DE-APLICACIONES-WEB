from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, nombre, email, password, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol  # Nuevo campo

    def es_admin(self):
        return self.rol == 'admin'
