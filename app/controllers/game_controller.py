from flask import Blueprint, render_template, request, jsonify
from flask_user import login_required, current_user

from app.exceptions.controller_exceptions import PlaceBetException
from app.db.db_repo import database_repo

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/play')
def toto_play():
    draws = database_repo.get_pending_draws()
    return render_template('pages/play/toto_football.html', draws=draws)


@game_blueprint.route('/play/<draw_id>')
@login_required
def draw_play(draw_id):
    draw = database_repo.get_draw_by_id(draw_id)
    possible_outcomes = database_repo.get_all_possible_outcomes()
    return render_template('pages/play/toto_football_placebet.html', draw=draw, possible_outcomes=possible_outcomes)


@game_blueprint.route('/play/placebet', methods=['POST'])
@login_required
def place_bet():
    json = request.get_json()
    amount = json['info']['amount']
    if amount == '':
        raise PlaceBetException(message="Provide bet amount data")

    events_data = json['events']

    database_repo.place_bet(amount=amount, events_data=events_data, user=current_user)
    return jsonify({"message": "Bet placed successfully"})


@game_blueprint.errorhandler(PlaceBetException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
