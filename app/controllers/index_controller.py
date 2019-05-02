from flask import Blueprint, render_template, redirect

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def landing_page():
    # return render_template('pages/index.html')
    return redirect("/play")

