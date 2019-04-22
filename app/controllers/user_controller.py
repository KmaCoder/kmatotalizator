from flask import Blueprint, render_template, flash
from flask_login import current_user
from flask_user import login_required

from app.forms.UserForms import UserBalanceReplenish
from app.db.db_repo import database_repo

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/user/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = UserBalanceReplenish()

    if form.validate_on_submit():
        database_repo.update_user_balance(current_user, form.amount.data)
        flash(f"Your balance was successfully replenished (+{form.amount.data})", "success")

    return render_template('flask_user/custom_pages/balance.html', form=form)
