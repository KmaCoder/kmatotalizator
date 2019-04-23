from flask_user import roles_required
from flask import Blueprint, render_template, url_for, redirect, flash

from app.forms.AdminForms import *
from app.db.db_repo import database_repo

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@roles_required('admin')
def main_page():
    return render_template('pages/adminka/admin_main.html')


@admin_blueprint.route('/admin/draws', methods=['GET', 'POST'])
@roles_required('admin')
def draws():
    form = AdminCreateDrawForm()
    if form.validate_on_submit():
        draw = database_repo.create_draw(draw_name=form.name.data, draw_date=form.date.data)
        flash(f"Draw #{draw.id} created successfully", "success")
    draws_list = database_repo.get_all_draws()
    return render_template('pages/adminka/admin_draws.html', form=form, draws=draws_list)


@admin_blueprint.route('/admin/draws/<draw_id>', methods=['GET', 'POST'])
@roles_required('admin')
def draw_edit(draw_id):
    form = AdminCreateEventForm()
    draw = database_repo.get_draw_by_id(draw_id)
    if form.validate_on_submit():
        event = database_repo.create_event(event_name=form.name.data, draw=draw)
        flash(f"Event #{event.id} created successfully", "success")
    return render_template('pages/adminka/admin_draw_edit.html', form=form, draw=draw)
