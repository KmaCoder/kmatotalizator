from flask_user import roles_required
from flask import Blueprint, render_template, flash, request, jsonify, redirect

from app.exceptions.db_exceptions import DrawEventsOverflowException
from app.forms.AdminForms import *
from app.db.db_repo import database_repo

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@roles_required('admin')
def main_page():
    return redirect("/admin/draws")


@admin_blueprint.route('/admin/draws', methods=['GET', 'POST'])
@roles_required('admin')
def draws():
    form = AdminCreateDrawForm()
    if form.validate_on_submit():
        draw = database_repo.create_draw(draw_name=form.name.data)
        if form.add_random_events.data:
            database_repo.add_random_events_to_draw(draw=draw, date=form.date.data)
            flash(f"Random events added to draw", "success")
        flash(f"Draw #{draw.id} created successfully", "success")

    draws_list = database_repo.get_all_draws()
    return render_template('pages/adminka/admin_draws.html', form=form, draws=draws_list)


@admin_blueprint.route('/admin/draws/<draw_id>', methods=['GET', 'POST'])
@roles_required('admin')
def draw_edit(draw_id):
    form = AdminCreateEventForm()
    draw = database_repo.get_draw_by_id(draw_id)
    possible_outcomes = database_repo.get_all_possible_outcomes()
    if form.validate_on_submit():
        try:
            event = database_repo.create_event(event_name=form.name.data, event_datetime=form.date.data, draw=draw)
            flash(f"Event #{event.id} created successfully", "success")
        except DrawEventsOverflowException:
            flash(f"You are trying to add to many events: maximum {draw.events_amount}", "error")
    return render_template('pages/adminka/admin_draw_edit.html', form=form, draw=draw,
                           possible_outcomes=possible_outcomes)


@admin_blueprint.route('/admin/event/<event_id>/update_outcome', methods=['POST'])
@roles_required('admin')
def update_outcome(event_id):
    outcome_id = request.get_json()['outcome_id']
    database_repo.update_event_outcome(outcome_id=outcome_id, event_id=event_id)
    return jsonify({"message": f"Outcome successfully updated for event #{event_id}"})


@admin_blueprint.route('/admin/draws/<draw_id>/distribute', methods=['GET'])
@roles_required('admin')
def test_distribute(draw_id):
    database_repo._distribute_pool(database_repo.get_draw_by_id(draw_id))
    return "test_distribute"
