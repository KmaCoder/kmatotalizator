import hashlib

from flask_wtf import Form
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

from app.db.db_repo import database_repo


class UserLoginForm(Form):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate_on_submit(self):
        rv = Form.validate_on_submit(self)

        if not rv:
            return False

        user = database_repo.get_user(self.login.data)
        if user is None:
            self.login.errors.append("User with this login is not registered")
            return False

        if user.passhash != hashlib.sha3_256(self.password.data.encode()).hexdigest():
            self.password.errors.append("Password is wrong")
            return False

        return True


class UserRegisterForm(Form):
    login = StringField('Login', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        return True
