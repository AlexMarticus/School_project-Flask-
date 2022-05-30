from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired


class ChangeLessons(FlaskForm):
    class_ = StringField('class', validators=[DataRequired()])
    day = StringField('day')
    date = DateField('date')

    mon1 = StringField('1mon')
    mon2 = StringField('2mon')
    mon3 = StringField('3mon')
    mon4 = StringField('4mon')
    mon5 = StringField('5mon')
    mon6 = StringField('6mon')
    mon7 = StringField('7mon')

    tue1 = StringField('1tue')
    tue2 = StringField('2tue')
    tue3 = StringField('3tue')
    tue4 = StringField('4tue')
    tue5 = StringField('5tue')
    tue6 = StringField('6tue')
    tue7 = StringField('7tue')

    wed1 = StringField('1wed')
    wed2 = StringField('2wed')
    wed3 = StringField('3wed')
    wed4 = StringField('4wed')
    wed5 = StringField('5wed')
    wed6 = StringField('6wed')
    wed7 = StringField('7wed')

    thu1 = StringField('1thu')
    thu2 = StringField('2thu')
    thu3 = StringField('3thu')
    thu4 = StringField('4thu')
    thu5 = StringField('5thu')
    thu6 = StringField('6thu')
    thu7 = StringField('7thu')

    fri1 = StringField('1fri')
    fri2 = StringField('2fri')
    fri3 = StringField('3fri')
    fri4 = StringField('4fri')
    fri5 = StringField('5fri')
    fri6 = StringField('6fri')
    fri7 = StringField('7fri')

    sat1 = StringField('1sat')
    sat2 = StringField('2sat')
    sat3 = StringField('3sat')
    sat4 = StringField('4sat')
    sat5 = StringField('5sat')
    sat6 = StringField('6sat')
    sat7 = StringField('7sat')

    is_constant = BooleanField('Постоянное расписание')
    submit = SubmitField('Подтвердить')
