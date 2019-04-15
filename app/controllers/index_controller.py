from flask import Blueprint, render_template

index = Blueprint('index', __name__)


@index.route('/')
def main_page():
    return render_template('pages/index.html')


@index.route('/login')
def login_page():
    return render_template('pages/login_page.html')


@index.route('/register')
def register_page():
    return render_template('pages/register_page.html')
