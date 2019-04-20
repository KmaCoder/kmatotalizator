from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user, login_manager

from app.db.database import db
from app.db.db_repo import database_repo
from app.forms.UserForms import UserLoginForm, UserRegisterForm

user_blueprint = Blueprint('user', __name__)


# @login_manager.user_loader
# def load_user(user_id):
#     return database_repo.get_user(user_id)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next')
    if current_user.is_authenticated:
        return redirect(next_url or url_for('game.main_page'))
    else:
        form = UserLoginForm()
        if form.validate_on_submit():
            user = database_repo.get_user(form.login)
            login_user(user)
            return redirect(next_url or url_for('game.main_page'))
        return render_template('pages/login_page.html', form=form)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm(request.form)
    if form.validate_on_submit():
        user = database_repo.create_user(
            login=form.login.data,
            email=form.email.data,
            password=form.password.data,
            balance_initial=0
        )
        db.session.add(user)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('game.main_page'))
    return render_template('pages/register_page.html')


@user_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index_blueprint.landing_page'))
