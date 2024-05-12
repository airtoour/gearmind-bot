from flask_login import UserMixin
from src.db.db_app import db


class Users(db.Model, UserMixin):
    user_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_user_id    = db.Column(db.Integer, nullable=True, unique=True)
    tg_username   = db.Column(db.String(128), nullable=True, unique=True)
    first_name    = db.Column(db.String(128), nullable=False)
    phone_number  = db.Column(db.String(12), nullable=False, unique=True)
    city_name     = db.Column(db.String(128), nullable=True)

    @staticmethod
    def get_current(tg_user_id):
        is_user = Users.query.filter_by(tg_user_id=int(tg_user_id)).first()
        return is_user

    @classmethod
    def create(
            cls,
            tg_user_id:    int,
            tg_username:   str,
            first_name:    str,
            phone_number:  str,
            city_name:     str):
        try:
            new_user = cls(
                tg_user_id   = tg_user_id,
                tg_username  = tg_username,
                first_name   = first_name,
                phone_number = phone_number,
                city_name    = city_name
            )
            db.session.add(new_user)
            db.session.commit()

            return new_user
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()


class Cars(db.Model):
    car_id     = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    brand_name = db.Column(db.String(128), nullable=False)
    model_name = db.Column(db.String(128), nullable=False)
    gen_name   = db.Column(db.String(128), nullable=False)
    year       = db.Column(db.Integer, nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('Users', backref='cars', lazy=True)

    @staticmethod
    def car_register(brand: str, model: str, gen: str, year: int, tg_user_id: str):
        user = Users.get_current(tg_user_id)

        try:
            user_car = Cars(
                brand_name = brand,
                model_name = model,
                gen_name   = gen,
                year       = year,
                user_id    = user.user_id
            )
            db.session.add(user_car)
            db.session.commit()
            print('Машина успешно зарегистрирована в базе данных!')
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
