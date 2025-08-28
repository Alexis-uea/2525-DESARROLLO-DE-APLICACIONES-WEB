from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# Formulario para agregar producto
class ProductoForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Agregar')

# Formulario para editar (sin código)
class EditarProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar cambios')
