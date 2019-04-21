from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_user import UserManager

from app.db.db_repo import database_repo
from app.forms.UserForms import UserLoginForm, UserRegisterForm

user_blueprint = Blueprint('user', __name__)


# @user_blueprint.route('/login', methods=['GET', 'POST'])
# def user_login():
#     next_url = request.args.get('next')
#     if current_user.is_authenticated:
#         return redirect(next_url or url_for('game.main_page'))
#     else:
#         form = UserLoginForm()
#         if form.validate_on_submit():
#             user = database_repo.get_user(form.login.data)
#             login_user(user)
#             return redirect(next_url or url_for('game.main_page'))
#
#         return render_template('pages/login_page.html', form=form)
#
#
# @user_blueprint.route('/register', methods=['GET', 'POST'])
# def user_register():
#     form = UserRegisterForm(request.form)
#     if form.validate_on_submit():
#         user = database_repo.create_user(
#             login=form.login.data,
#             email=form.email.data,
#             password=form.password.data,
#             balance_initial=0
#         )
#         user_login(user)
#         return redirect(request.args.get('next') or url_for('game.main_page'))
#     return render_template('pages/register_page.html', form=form)
#
#
# @user_blueprint.route('/logout')
# @login_required
# def user_logout():
#     user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return redirect(url_for('index_blueprint.landing_page'))
