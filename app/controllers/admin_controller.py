from flask_user import roles_required
from flask import Blueprint, render_template, url_for, redirect

from app.db.db_repo import database_repo

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@roles_required('admin')
def main_page():
    return render_template('pages/adminka/admin_main.html')


@admin_blueprint.route('/admin/create_draw', methods=['POST'])
@roles_required('admin')
def create_draw():
    database_repo.create_user()
    return redirect(url_for('admin.main_page'))
