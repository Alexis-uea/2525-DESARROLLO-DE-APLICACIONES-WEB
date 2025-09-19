from models import db, Producto

class Inventario:
    """
    - Usa un diccionario {id: Producto} para accesos O(1).
    - Mantiene un set con nombres en minúsculas para validar duplicados rápidamente.
    - Devuelve listas ordenadas usando list/tuplas según convenga.
    """
    def __init__(self, productos_dict=None):
        self.productos = productos_dict or {}  # dict[int, Producto]
        self.nombres = set(p.nombre.lower() for p in self.productos.values())

    @classmethod
    def cargar_desde_bd(cls):
        productos = Producto.query.all()              # -> list[Producto]
        productos_dict = {p.id: p for p in productos} # dict por id
        return cls(productos_dict)

    # --- CRUD ---
    def agregar(self, nombre: str, cantidad: int, precio: float) -> Producto:
        if nombre.lower() in self.nombres:
            raise ValueError('Ya existe un producto con ese nombre.')
        p = Producto(nombre=nombre.strip(), cantidad=int(cantidad), precio=float(precio))
        db.session.add(p)
        db.session.commit()
        self.productos[p.id] = p
        self.nombres.add(p.nombre.lower())
        return p

    def eliminar(self, id: int) -> bool:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        self.productos.pop(id, None)
        self.nombres.discard(p.nombre.lower())
        return True

    def actualizar(self, id: int, nombre=None, cantidad=None, precio=None) -> Producto | None:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return None
        if nombre is not None:
            nuevo = nombre.strip()
            if nuevo.lower() != p.nombre.lower() and nuevo.lower() in self.nombres:
                raise ValueError('Ya existe otro producto con ese nombre.')
            self.nombres.discard(p.nombre.lower())
            p.nombre = nuevo
            self.nombres.add(p.nombre.lower())
        if cantidad is not None:
            p.cantidad = int(cantidad)
        if precio is not None:
            p.precio = float(precio)
        db.session.commit()
        self.productos[p.id] = p
        return p

    # --- Consultas con colecciones ---
    def buscar_por_nombre(self, q: str):
        q = q.lower()
        # list comprehension: filtra del dict de cache
        return sorted([p for p in self.productos.values() if q in p.nombre.lower()],
                      key=lambda x: x.nombre)

    def listar_todos(self):
        return sorted(self.productos.values(), key=lambda x: x.nombre)
