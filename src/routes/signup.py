from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, LoginManager

from src.models.models import Users
from src.db.db_app import app

signup_bp = Blueprint('signup', __name__, template_folder='templates/auth', static_folder='static')

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(name):
    return Users.query.get(name)


@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    message = ""

    if request.method == 'POST':
        name = request.form.get('name')
        bday = request.form.get('bday')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        is_user = Users.get_current(phone)

        try:
            if is_user:
                message = 'Пользователь уже существует, попробуйте снова!'
                return render_template('signup.html', message=message)
            else:
                if password == confirm_password:
                    new_user = Users.create(
                        first_name=name,
                        birthday=bday,
                        phone_number=phone,
                        user_email=email,
                        user_password=password
                    )
                    login_user(new_user)
                else:
                    message = 'Пароли не совпадают, попробуйте ещё раз!'

                return redirect(url_for('main.index'))
        except Exception as e:
            app.logger.error(str(e))

    return render_template('signup.html', message=message)
