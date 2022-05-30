from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddEvents(FlaskForm):
    date_time_place = StringField('Дата/время/место', validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    responsible = StringField('Ответственные', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
