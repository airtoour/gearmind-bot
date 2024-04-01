from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, LoginManager

from src.models.forms.forms import LoginForm
from src.models.models.models import Users
from src.db.config import app

login_bp = Blueprint('login', __name__, template_folder='templates')

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm

    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data

        is_user = Users.get_current(phone)

        try:
            if is_user:
                if is_user.check_hash(password):
                    login_user(is_user)

                    return redirect(url_for('main.index'))
                else:
                    message = ('Неправильно введены номер телефона или пароль.\n'
                               'Попробуйте снова!')
                    return render_template('login.html', message=message, form=form)
            else:
                message = 'Такого пользователя не существует!'
                return render_template('signup.html', message)
        except Exception as e:
            app.logger.error(str(e))

    return render_template('login.html', form=form)