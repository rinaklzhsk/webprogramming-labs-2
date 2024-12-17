from flask import Blueprint, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')


