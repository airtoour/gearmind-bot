from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from src.db.config import db
from src.exceptions import server_exceptions


class Cities(db.Model):
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    city_name = db.Column(db.String(128), nullable=False, unique=True)


class Prod_groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    group_name = db.Column(db.String(128), nullable=False, unique=True)


class Cars(db.Model):
    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    prod_group_id = db.Column(db.Integer, db.ForeignKey('prod_groups.group_id'), nullable=False)
    car_name = db.Column(db.String(128), nullable=False)
    car_year = db.Column(db.Integer, nullable=False)


class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_user_id = db.Column(db.Integer, nullable=True, unique=True)
    tg_username = db.Column(db.String(128), nullable=True, unique=True)
    first_name = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    user_email = db.Column(db.String(128), nullable=False)
    user_password = db.Column(db.String(256), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=True)
    card_id = db.Column(db.Integer, nullable=True)
    is_vip = db.Column(db.String(1), default='N', nullable=True)

    def set_password(self, user_password):
        self.user_password = generate_password_hash(user_password)

    def check_hash(self, user_password):
        return check_password_hash(self.user_password, user_password)

    @staticmethod
    def get_current(email):
        is_user = Users.query.filter_by(user_email=email).first()
        return is_user

    @staticmethod
    def create(cls,
               first_name: str,
               phone_number: str,
               user_email: str,
               user_password: str):
        try:
            new_user = cls(tg_user_id=None,
                           tg_username=None,
                           first_name=first_name,
                           phone_number=phone_number,
                           user_email=user_email,
                           user_password=user_password,
                           city_id=None,
                           car_id=None,
                           card_id=None,
                           is_vip=None)
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
