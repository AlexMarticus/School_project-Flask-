from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField
from wtforms.validators import DataRequired


class MakeUnAdmin(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class MakeAdmin(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
