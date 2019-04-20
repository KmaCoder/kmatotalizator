from flask import Blueprint, render_template
from flask_user import roles_required

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
@roles_required('player')
def toto_football_page():
    return render_template('pages/play/toto_football.html')
