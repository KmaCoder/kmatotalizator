from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_user import UserManager

from app.db.db_repo import database_repo
from app.forms.UserForms import UserLoginForm, UserRegisterForm

user_blueprint = Blueprint('user', __name__)
