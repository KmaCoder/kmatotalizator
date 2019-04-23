from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

__all__ = ['AdminCreateDrawForm', 'AdminCreateEventForm']


class AdminCreateDrawForm(FlaskForm):
    name = StringField('Draw name', validators=[DataRequired()], render_kw={"placeholder": "Enter draw name:"})
    date = DateField('Bets accepted till date', validators=[DataRequired()], default=datetime.today, format='%Y-%m-%d',
                     render_kw={"placeholder": "Enter date:"})
    submit = SubmitField('Create')


class AdminCreateEventForm(FlaskForm):
    name = StringField('Event name', validators=[DataRequired()], render_kw={"placeholder": "Enter event name:"})
    submit = SubmitField('Create')
