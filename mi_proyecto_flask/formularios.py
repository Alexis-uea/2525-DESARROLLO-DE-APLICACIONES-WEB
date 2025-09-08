from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

# formularios para clientes.
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Guardar')
