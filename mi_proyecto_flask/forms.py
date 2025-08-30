from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    """
    Formulario para agregar nuevos productos a Amazonía Market
    Incluye validaciones para todos los campos requeridos
    """
    # Código de producto (único, obligatorio)
    codigo = StringField('Código de Producto', 
                        validators=[
                            DataRequired(message="El código del producto es obligatorio"),
                            Length(min=3, max=20, message="El código debe tener entre 3 y 20 caracteres")
                        ])
    
    # Nombre del producto (obligatorio)
    nombre = StringField('Nombre del Producto', 
                        validators=[
                            DataRequired(message="El nombre del producto es obligatorio"),
                            Length(min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres")
                        ])
    
    # Cantidad en stock (entero positivo)
    cantidad = IntegerField('Cantidad en Stock', 
                           validators=[
                               DataRequired(message="La cantidad es obligatoria"),
                               NumberRange(min=0, message="La cantidad no puede ser negativa")
                           ])
    
    # Precio (decimal positivo)
    precio = DecimalField('Precio ($)', 
                         places=2,
                         validators=[
                             DataRequired(message="El precio es obligatorio"),
                             NumberRange(min=0, message="El precio no puede ser negativo")
                         ])
    
    # Botón de submit
    submit = SubmitField('Agregar Producto')

class EditarProductoForm(FlaskForm):
    """
    Formulario para editar productos existentes
    No incluye el campo código (no editable)
    """
    nombre = StringField('Nombre del Producto', 
                        validators=[
                            DataRequired(message="El nombre del producto es obligatorio"),
                            Length(min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres")
                        ])
    
    cantidad = IntegerField('Cantidad en Stock', 
                           validators=[
                               DataRequired(message="La cantidad es obligatoria"),
                               NumberRange(min=0, message="La cantidad no puede ser negativa")
                           ])
    
    precio = DecimalField('Precio ($)', 
                         places=2,
                         validators=[
                             DataRequired(message="El precio es obligatorio"),
                             NumberRange(min=0, message="El precio no puede ser negativo")
                         ])
    
    submit = SubmitField('Guardar Cambios')