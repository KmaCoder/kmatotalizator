from flask import Blueprint, render_template
from flask_user import roles_required, login_required
from app.db.db_repo import database_repo


game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
@login_required
def toto_play():
    draws = database_repo.get_pending_draws()
    return render_template('pages/play/toto_football.html', draws=draws)
