from flask_wtf import FlaskForm
from wtforms import (IntegerField, FloatField, StringField, EmailField,
                     PasswordField, DateField, SubmitField, SelectField)
from wtforms.validators import DataRequired, InputRequired, Length, Email


class SignUpForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    bday = DateField('Дата рождения', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(8, 32)])

    submit = SubmitField('Регистрация')


class LoginForm(FlaskForm):
    phone = StringField('Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[InputRequired()])

    submit = SubmitField('Войти')
