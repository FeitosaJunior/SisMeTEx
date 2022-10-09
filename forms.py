from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, StringField


class InfoForm(FlaskForm):
    startdate = DateField('Data início', format='%Y-%m-%d',
                          validators=(DataRequired(),))
    enddate = DateField('Data final', format='%Y-%m-%d',
                        validators=(DataRequired(),))
    station = StringField('Estação', validators=(DataRequired(),))
    submit = SubmitField('Enviar')
