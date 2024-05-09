from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from src.db.db_app import db
from src.exceptions import server_exceptions


class Cities(db.Model):
    city_id   = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    city_name = db.Column(db.String(128), nullable=False, unique=True)

    users = db.relationship('Users', backref='city', lazy=True)

class CarsBrand(db.Model):
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    brand_name = db.Column(db.String(256), nullable=True)

    model = db.relationship('CarsModel', backref='brand', lazy=True)

class CarsModel(db.Model):
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    model_id   = db.Column(db.Integer, db.ForeignKey('carsbrand.id'), nullable=True)
    model_name = db.Column(db.String(256), nullable=True)

    gens = db.relationship('CarsGens', backref='model', lazy=True)

class CarsGens(db.Model):
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    model_id   = db.Column(db.Integer, db.ForeignKey('carsmodel.id'), nullable=True)
    gen_name   = db.Column(db.String(256), nullable=True)

class Users(db.Model, UserMixin):
    user_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_user_id    = db.Column(db.Integer, nullable=True, unique=True)
    tg_username   = db.Column(db.String(128), nullable=True, unique=True)
    first_name    = db.Column(db.String(128), nullable=False)
    birth_date    = db.Column(db.DateTime, nullable=False)
    phone_number  = db.Column(db.String(12), nullable=False)
    user_email    = db.Column(db.String(128), nullable=False)
    user_password = db.Column(db.String(256), nullable=True)
    city_id       = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=True)

    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_hash(self, user_password):
        return check_password_hash(self.user_password, user_password)

    @staticmethod
    def get_current(phone):
        is_user = Users.query.filter_by(phone_number=phone).first()
        return is_user

    @staticmethod
    def create(first_name:    str,
               birthday:      str,
               phone_number:  str,
               user_email:    str,
               user_password: str,
               city_id:       Cities):
        try:

            new_user = Users(
                tg_user_id    = None,
                tg_username   = None,
                first_name    = first_name,
                birth_date    = birthday,
                phone_number  = phone_number,
                user_email    = user_email,
                user_password = user_password,
                city_id       = city_id.city_id
            )
            new_user.set_password(user_password)

            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            print(e)
            db.session.rollback()
            return server_exceptions(500, str(e))
        finally:
            db.session.close()

class Cars(db.Model):
    car_id   = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('carsbrand.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('carsmodel.id'), nullable=False)
    gen_id   = db.Column(db.Integer, db.ForeignKey('carsgen.id'), nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    user = db.relationship('Users', backref='cars', lazy=True)