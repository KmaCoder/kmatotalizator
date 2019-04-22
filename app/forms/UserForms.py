from flask_wtf import Form
from wtforms import PasswordField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

from app.db.db_repo import database_repo


class UserBalanceReplenish(Form):
    amount = IntegerField('Amount', validators=[DataRequired()], render_kw={"placeholder": "Top-up amount"})
    submit = SubmitField('Replenish')


# class UserLoginForm(Form):
#     login = StringField('Login', validators=[DataRequired()], render_kw={"placeholder": "Enter login"})
#     password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
#     submit = SubmitField('Login')
#
#     def __init__(self, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#
#     def validate_on_submit(self):
#         rv = Form.validate_on_submit(self)
#
#         if not rv:
#             return False
#
#         user = database_repo.get_user_by_id(self.login.data)
#         if user is None:
#             self.login.errors.append("User with this login is not registered")
#             return False
#
#         if user.passhash != hashlib.sha3_256(self.password.data.encode()).hexdigest():
#             self.password.errors.append("Password is wrong")
#             return False
#
#         return True
#
#
# class UserRegisterForm(Form):
#     login = StringField('Login', validators=[DataRequired()], render_kw={"placeholder": "Enter unique login"})
#     email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter your email"})
#     password = PasswordField('Password', validators=[DataRequired()],
#                              render_kw={"placeholder": "Enter your new password"})
#     submit = SubmitField('Register')
#
#     def validate(self):
#         rv = Form.validate(self)
#         if not rv:
#             return False
#         return True
