from flask import Blueprint, render_template
from flask_user import roles_required, login_required

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
@login_required
def main_page():
    return render_template('pages/play/toto_football.html')
