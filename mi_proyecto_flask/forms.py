from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# Formulario para agregar un nuevo producto
class ProductoForm(FlaskForm):
    # Código del producto: campo de texto obligatorio
    codigo = StringField('Código', validators=[DataRequired(message="El código es obligatorio")])
    
    # Nombre del producto: campo de texto obligatorio
    nombre = StringField('Nombre', validators=[DataRequired(message="El nombre es obligatorio")])
    
    # Cantidad: campo numérico entero, obligatorio y al menos 0 (puedes cambiar a 1 si prefieres)
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria"),
        NumberRange(min=0, message="La cantidad debe ser cero o mayor")
    ])
    
    # Precio: campo decimal con 2 decimales, obligatorio y mínimo 0
    precio = DecimalField('Precio', places=2, validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0, message="El precio debe ser cero o mayor")
    ])
    
    # Botón para enviar el formulario
    submit = SubmitField('Agregar')

# Formulario para editar producto (no se edita el código)
class EditarProductoForm(FlaskForm):
    # Nombre del producto (editable)
    nombre = StringField('Nombre', validators=[DataRequired(message="El nombre es obligatorio")])
    
    # Cantidad editable, con misma validación que arriba
    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria"),
        NumberRange(min=0, message="La cantidad debe ser cero o mayor")
    ])
    
    # Precio editable
    precio = DecimalField('Precio', places=2, validators=[
        DataRequired(message="El precio es obligatorio"),
        NumberRange(min=0, message="El precio debe ser cero o mayor")
    ])
    
    # Botón para enviar el formulario
    submit = SubmitField('Guardar cambios')
