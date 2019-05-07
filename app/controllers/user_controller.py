from flask import Blueprint, render_template, flash
from flask_login import current_user
from flask_user import login_required, UserManager

from app.forms.UserForms import UserBalanceReplenish, CustomEditUserProfileForm
from app.db.db_repo import database_repo

user_blueprint = Blueprint('user', __name__)


class CustomUserManager(UserManager):

    def customize(self, app):
        self.EditUserProfileForm = CustomEditUserProfileForm


@user_blueprint.route('/user/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = UserBalanceReplenish()

    if form.validate_on_submit():
        database_repo.update_user_balance(current_user, form.amount.data)
        flash(f"Your balance was successfully replenished (+{form.amount.data})", "success")

    return render_template('flask_user/custom_pages/balance.html', form=form)


@user_blueprint.route('/user/parlays', methods=['GET'])
@login_required
def parlays():
    parlays = current_user.parlays
    return render_template('flask_user/custom_pages/parlays.html', parlays=parlays)
